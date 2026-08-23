import asyncio
import json
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        errors = []
        page.on("console", lambda m: errors.append(f"console.{m.type}: {m.text}") if m.type in ("error", "warning") else None)
        page.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))
        await page.goto("http://127.0.0.1:8021/", wait_until="networkidle")
        await page.wait_for_timeout(500)

        report = {}

        # 1. Core presence
        report["title"] = await page.title()
        report["cards"] = await page.locator(".card").count()
        report["rail_pills"] = await page.locator(".rail-pill").count()
        report["seg_buttons"] = await page.locator(".seg-btn").count()
        report["count_label"] = await page.locator("#count-label").text_content()
        report["nsfw_switch"] = await page.locator("#nsfw-switch").get_attribute("aria-checked")

        # 2. Horizontal overflow at desktop
        report["doc_scrollwidth"] = await page.evaluate("document.documentElement.scrollWidth")
        report["doc_clientwidth"] = await page.evaluate("document.documentElement.clientWidth")

        # 3. First card metrics
        first = page.locator(".card").first
        box = await first.bounding_box()
        report["first_card_box"] = box
        report["first_card_radius"] = await first.evaluate("el => getComputedStyle(el).borderRadius")
        report["first_card_shadow"] = (await first.evaluate("el => getComputedStyle(el).boxShadow"))[:90]

        # 4. Contrast checks (foreground vs effective bg)
        import re as _re
        def _to_rgb(c):
            m = _re.search(r"rgba?\(([\d.]+),\s*([\d.]+),\s*([\d.]+)", c)
            if m:
                return tuple(float(m.group(i))/255 for i in (1,2,3))
            h = c.lstrip("#")
            if len(h) == 6:
                return tuple(int(h[i:i+2],16)/255 for i in (0,2,4))
            return None
        def lum(c):
            c = _to_rgb(c)
            if not c: return 0
            f = lambda v: v/12.92 if v <= 0.04045 else ((v+0.055)/1.055)**2.4
            r,g,b = (f(v) for v in c)
            return 0.2126*r+0.7152*g+0.0722*b
        def contrast(a,b):
            la, lb = lum(a), lum(b)
            if la < lb: la, lb = lb, la
            return (la+0.05)/(lb+0.05)
        def midgrad(cs):
            import statistics
            return "rgb(%d, %d, %d)" % tuple(round(statistics.fmean(ch)) for ch in zip(*cs))

        body_bg = await page.evaluate("getComputedStyle(document.body).backgroundColor")
        ctitle = await page.locator(".card-title").first.evaluate("el => getComputedStyle(el).color")
        csub = await page.locator(".card-sub").first.evaluate("el => getComputedStyle(el).color")
        cchip = await page.locator(".chip").first.evaluate("el => getComputedStyle(el).color")
        cstate_pend = await page.locator(".chip-state[data-state='pendiente']").first.evaluate("el => getComputedStyle(el).color")
        cstate_cur = await page.locator(".chip-state[data-state='en_curso']").first.evaluate("el => getComputedStyle(el).color")
        # Effective card body bg = mean of the card gradient stops
        card_stops = await page.evaluate("""
            () => {
                const el = document.querySelector('.card');
                const img = getComputedStyle(el).backgroundImage;
                const stops = [...img.matchAll(/#[0-9a-f]{6}/gi)].map(m => m[0]);
                if (stops.length) return stops;
                return [...img.matchAll(/rgba?\([^)]+\)/g)].map(m => m[0]);
            }
        """)
        card_bg = midgrad([_to_rgb(s) for s in card_stops])
        capture_bg = await page.evaluate("getComputedStyle(document.querySelector('.capture')).backgroundColor")
        ph_color = await page.locator(".capture-input").evaluate("el => getComputedStyle(el, '::placeholder').color")
        body_color = await page.evaluate("getComputedStyle(document.body).color")

        report["contrast_title_vs_cardbg"] = round(contrast(ctitle, card_bg), 2)
        report["contrast_sub_vs_cardbg"] = round(contrast(csub, card_bg), 2)
        report["contrast_chip_vs_cardbg"] = round(contrast(cchip, card_bg), 2)
        report["contrast_state_pend"] = round(contrast(cstate_pend, card_bg), 2)
        report["contrast_state_cur"] = round(contrast(cstate_cur, card_bg), 2)
        report["contrast_placeholder_vs_capture"] = round(contrast(ph_color, capture_bg), 2)
        report["contrast_body_vs_bg"] = round(contrast(body_color, body_bg), 2)

        # 5. Placeholder contrast
        ph = await page.locator(".capture-input").evaluate("el => getComputedStyle(el).getPropertyValue('--tw-placeholder-color') || getComputedStyle(el, '::placeholder').color")
        ph_input_bg = await page.evaluate("getComputedStyle(document.querySelector('.capture')).backgroundImage")

        # 6. NSFW: two blurred cards present
        report["nsfw_cards"] = await page.locator(".card.is-nsfw").count()
        nsfw_blur = await page.locator(".card.is-nsfw .card-cover").first.evaluate("el => getComputedStyle(el).filter")
        report["nsfw_cover_filter"] = nsfw_blur

        # 7. Empty state reachable
        await page.locator(".rail-pill[data-cat='comics']").click()
        await page.locator(".seg-btn[data-state='terminado']").click()
        await page.wait_for_timeout(200)
        report["empty_visible_after_comics_terminado"] = await page.locator("#empty-state").is_visible()
        report["empty_title"] = await page.locator("#empty-state h2").text_content()
        await page.locator(".seg-btn[data-state='todos']").click()
        await page.locator(".rail-pill[data-cat='todo']").click()
        await page.wait_for_timeout(200)

        # 8. State filter
        await page.locator(".seg-btn[data-state='terminado']").click()
        await page.wait_for_timeout(200)
        report["cards_after_terminado"] = await page.locator(".card").count()
        report["count_after_terminado"] = await page.locator("#count-label").text_content()
        await page.locator(".seg-btn[data-state='todos']").click()
        await page.wait_for_timeout(200)

        # 9. List view
        await page.locator("#view-list").click()
        await page.wait_for_timeout(200)
        report["list_class"] = await page.locator("#grid").get_attribute("class")
        report["cards_in_list"] = await page.locator(".card").count()
        await page.locator("#view-grid").click()
        await page.wait_for_timeout(200)

        # 10. Settings dialog
        await page.locator("#btn-settings").click()
        await page.wait_for_timeout(200)
        report["settings_open"] = await page.locator("#settings-dialog").evaluate("d => d.open")
        await page.keyboard.press("Escape")

        # 11. Capture results flow (mock API via route)
        await page.route("**/api/search?*", lambda route: route.fulfill(status=200, json=[
            {"api_id": "42", "title": "Inception", "year": "2010", "overview": "Un ladrón que roba ideas entra en los sueños."}
        ]))
        await page.locator("#capture-input").fill("Inception")
        await page.locator("#capture-cat-btn").click()
        await page.locator("[data-cat-pick='peliculas']").click()
        await page.wait_for_timeout(150)
        await page.locator("#capture-form").evaluate("f => f.requestSubmit()")
        await page.wait_for_timeout(500)
        report["results_rows"] = await page.locator(".result-row[data-save]").count()
        report["result_title"] = await page.locator(".result-row[data-save] .result-title").first.text_content()
        # pick it -> save (mock save)
        await page.route("**/api/save", lambda route: route.fulfill(status=200, json={
            "id": "tmdb_42", "title": "Inception", "original_title": "Inception", "release_date": "2010-07-16",
            "director": "Christopher Nolan", "duracion": 148, "genre": ["Acción", "Thriller"], "origin_country": ["US"]
        }))
        await page.locator(".result-row[data-save]").first.click()
        await page.wait_for_timeout(400)
        report["cards_after_save"] = await page.locator(".card").count()
        report["count_after_save"] = await page.locator("#count-label").text_content()
        await page.keyboard.press("Escape")

        report["console_errors"] = errors
        print(json.dumps(report, indent=2, ensure_ascii=False))
        await browser.close()

asyncio.run(main())
