import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        await page.goto("http://127.0.0.1:8021/", wait_until="networkidle")
        await page.wait_for_timeout(800)
        await page.screenshot(path="shot_desktop_full.png", full_page=False)
        await page.screenshot(path="shot_desktop_fullpage.png", full_page=True)
        await browser.close()

asyncio.run(main())
