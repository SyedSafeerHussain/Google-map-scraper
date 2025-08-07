import asyncio
import csv
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://www.google.com/maps")
        await page.fill("input#searchboxinput", "dentist lahore")
        await page.click("button#searchbox-searchbutton")
        await page.wait_for_timeout(8000)  # wait for results to load

        containers = await page.query_selector_all("a.hfpxzc")

        with open("data.csv", 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Business Name", "Address", "Website", "Phone", "URL"])

            if containers:
                for i, detail in enumerate(containers[:5]):  # scrape only first 5 to avoid ban
                    await detail.click()
                    await page.wait_for_timeout(5000)


                    try:
                        await page.wait_for_selector("h1.DUwDvf",timeout=5000)
                        business_name = await page.locator("h1.DUwDvf").inner_text()
                    except:
                        business_name = "N/A"

                    try:
                        address = await page.locator("div.rogA2c").first.inner_text()
                    except:
                        address = "N/A"

                    try:
                        website = await page.locator("a[data-item-id='authority']").inner_text()
                    except:
                        website = "N/A"

                    try:
                        phone = await page.locator("button[data-tooltip='Copy phone number']").inner_text()
                    except:
                        phone = "N/A"

                    try:
                        url = page.url
                    except:
                        url = "N/A"

                    writer.writerow([business_name, address, website, phone, url])

                    # Go back to result list
                    await page.go_back()
                    await page.wait_for_timeout(3000)
            else:
                print("❌ No business cards found.")

        await browser.close()

asyncio.run(run())
