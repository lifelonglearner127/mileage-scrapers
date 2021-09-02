from sys import platform
from typing import Optional

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.exceptions import PlatformNotSupported


class Browser(webdriver.Chrome):
    def __init__(self, executable_path="chromedriver"):
        self.display = Display(visible=False)
        self.display.start()

        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-browser-side-navigation")
        options.add_argument("--disable-features=VizDisplayCompositor")
        options.add_argument("--disable-gpu")
        options.add_argument("--force-device-scale-factor=1")
        options.add_argument("--disable-backgrounding-occluded-windows")
        options.add_argument("--disable-extensions")
        options.add_argument("--start-maximized")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--allow-running-insecure-content")
        options.add_argument("--log-level=3")
        options.add_argument("--disable-blink-features=AutomationControlled")
        super().__init__(executable_path=executable_path, chrome_options=options)

    def quit(self):
        self.display.stop()
        super().quit()


class BaseCralwer:
    def __init__(self):
        if platform in ["win32", "win64"]:
            raise PlatformNotSupported()
        self._client = Browser()

    def wait_until(self, identifier: str, by: str = By.XPATH, timeout: int = 15) -> Optional[WebElement]:
        return WebDriverWait(self._client, timeout).until(EC.element_to_be_clickable((by, identifier)))

    def send_keys(self, web_element: WebElement, key: str):
        web_element.clear()
        web_element.send_keys(key)

    def find_element(self, web_element: WebElement, identifier: str, by: str = By.XPATH) -> WebElement:
        return web_element.find_element(by=By.XPATH, value=identifier)
