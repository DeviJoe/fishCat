import requests
import pyppeteer
import json

GOOGLE_SECURE = "https://transparencyreport.google.com/safe-browsing/search"
PHISHTANK = 'http://checkurl.phishtank.com/checkurl/'
WHOIS_JSON = 'https://whoisjson.com/whois-api'


class SideServiceChecker:

    def __init__(self, url) -> None:
        super().__init__()
        self.url = url

    async def is_google_secure_check_fishing(self):
        browser = await pyppeteer.launch()
        page = await browser.newPage()
        await page.goto(GOOGLE_SECURE)
        site_field = await page.querySelector('input.ng-valid')
        await site_field.type(self.url)
        search_btn = await page.querySelector('i.material-icons:nth-child(2)')
        await search_btn.click()
        await page.waitFor(500)
        answer = await page.querySelector('.value > span:nth-child(2)')
        res = await page.evaluate("document.querySelector('.value > span:nth-child(2)').innerText")
        print(res)
        await browser.close()
        if res == "This site is unsafe":
            return False
        elif res == "No unsafe content found":
            return True

    # async def is_fishtank_fishing(self):
    #     browser = await pyppeteer.launch()
    #     userAgent =
    #     page = await browser.newPage()
    #     await browser.close()
    #     pass

    async def whois_info_json(self) -> dict:
        browser = await pyppeteer.launch()
        page = await browser.newPage()
        await page.setUserAgent("Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0")
        await page.setViewport({'width': 1280, "height": 720})
        await page.goto(WHOIS_JSON)
        search_field = await page.querySelector('#domain')
        await page.evaluate('document.getElementById("domain").value = ""')
        await search_field.type(self.url)
        go_btn = await page.querySelector("#whois-btn")
        await go_btn.click()
        await page.waitFor(500)
        res_data = await page.querySelector('#display')
        await page.screenshot({
            'path': './image.png'
        })

        res = await page.evaluate("document.querySelector('#display').innerText")
        res = json.loads(res)
        return res
        pass
