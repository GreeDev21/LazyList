import asyncio
import json
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 390, "height": 844})
        errors = []
        page.on("console", lambda m: errors.append(f"console.{m.type}: {m.text}") if m.type in ("error", "warning") else None)
        page.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))
        await page.goto("http://127.0.0.1:8021/", wait_until="networkidle")
        await page.wait_for_timeout(500)

        report = {}

        # 1. No horizontal overflow
        report["doc_scrollwidth"] = await page.evaluate("document.documentElement.scrollWidth")
        report["doc_clientwidth"] = await page.evaluate("document.documentElement.clientWidth")
        report["overflowing"] = await page.evaluate(
            "document.documentElement.scrollWidth > document.documentElement.clientWidth"
        )

        # 2. Cards render and grid min width
        report["cards"] = await page.locator(".card").count()
        report["grid_cols"] = await page.locator("#grid").evaluate(
            "el => getComputedStyle(el).gridTemplateColumns.split(' ').length"
        )
        report["grid_min"] = await page.evaluate(
            "getComputedStyle(document.querySelector('#grid')).gridTemplateColumns.split(' ')[0]"
        )

        # 3. Capture layout: wrapped to row 2, cat hidden at 560
        report["capture_visible"] = await page.locator("#capture-shell").is_visible()
        report["capture_cat_visible"] = await page.locator("#capture-cat-btn").is_visible()
        capture_box = await page.locator("#capture-shell").bounding_box()
        report["capture_box"] = capture_box

        # 4. Rail scrolls horizontally without page overflow
        report["rail_overflow"] = await page.evaluate(
            "document.querySelector('.rail').scrollWidth > document.querySelector('.rail').clientWidth"
        )

        # 5. Header rows
        report["header_box"] = await page.locator("header").bounding_box()

        # 6. State filter / seg still usable
        await page.locator(".seg-btn[data-state='terminado']").click()
        await page.wait_for_timeout(200)
        report["cards_after_terminado"] = await page.locator(".card").count()
        await page.locator(".seg-btn[data-state='todos']").click()
        await page.wait_for_timeout(200)

        # 7. Settings dialog opens at mobile
        await page.locator("#btn-settings").click()
        await page.wait_for_timeout(200)
        report["settings_open"] = await page.locator("#settings-dialog").evaluate("d => d.open")
        await page.keyboard.press("Escape")

        report["console_errors"] = errors
        print(json.dumps(report, indent=2, ensure_ascii=False))

        # Screenshots
        await page.screenshot(path="shot_mobile_full.png", full_page=False)
        await page.screenshot(path="shot_mobile_fullpage.png", full_page=True)
        await browser.close()

asyncio.run(main())
