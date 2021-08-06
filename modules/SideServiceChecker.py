import requests
import pyppeteer

GOOGLE_SECURE = "https://transparencyreport.google.com/safe-browsing/search"
PHISHTANK = 'http://checkurl.phishtank.com/checkurl/'

class SideServiceChecker:

    def __init__(self, url) -> None:
        super().__init__()
        self.url = url
        self.browser = await pyppeteer.launch()

    def close_connection(self):
        await self.browser.close()

    async def is_google_secure_check_fishing(self):
        page = await self.browser.newPage()
        await page.goto(GOOGLE_SECURE)
        site_field = await page.querySelector('input.ng-valid')
        await site_field.type(self.url)
        search_btn = await page.querySelector('i.material-icons:nth-child(2)')
        await search_btn.click()
        await page.waitFor(2000)
        answer = await page.querySelector('.value > span:nth-child(2)')
        res = await page.evaluate("document.querySelector('.value > span:nth-child(2)').innerText")
        print(res)

        if res == "This site is unsafe":
            return False
        elif res == "No unsafe content found":
            return True

    async def is_fishtank_fishing(self):

        pass
