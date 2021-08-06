from modules import SideServiceChecker
from modules import ResourceCheck
import asyncio

if __name__ == '__main__':
    '''url = "https://paypal.pqaz.xyz/"
    url1 = "http://letoctf.org"
    sideCheck = SideServiceChecker.SideServiceChecker(url)
    sideCheck1 = SideServiceChecker.SideServiceChecker(url1)
    # asyncio.get_event_loop().run_until_complete(sideCheck.is_google_secure_check_fishing())
    # asyncio.get_event_loop().run_until_complete(sideCheck1.is_google_secure_check_fishing())
    asyncio.get_event_loop().run_until_complete(sideCheck1.whois_info_json())'''

    ResourceCheck.ResourceCheck.Scan("http://vk.com")

    pass