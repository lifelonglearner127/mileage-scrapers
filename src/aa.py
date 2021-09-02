import time

from selenium.common.exceptions import TimeoutException

from src.base import BaseCralwer

login_id = "4X2JC78"
last_name = "BURAU"
password = "Madeline1!"


class AACrawler(BaseCralwer):
    def login(self):
        login_url = "https://www.aa.com/loyalty/login?uri=%2floyalty%2flogin&previousPage=%2fhomePage.do&bookingPathStateId=&marketId="  # noqa
        self._client.get(login_url)
        try:
            accept_cookie_bar = self.wait_until("//button[@name='optoutmulti_button']")
            accept_cookie_bar.click()
            time.sleep(1)
        except TimeoutException:
            pass

        login_form = self.wait_until("//form[@id='loginFormId']")
        login_id_input = login_form.find_element_by_xpath(".//input[@id='loginId']")
        self.send_keys(login_id_input, login_id)
        # time.sleep(1)

        last_name_input = login_form.find_element_by_xpath(".//input[@id='lastName']")
        self.send_keys(last_name_input, last_name)
        time.sleep(1)

        password_input = login_form.find_element_by_xpath(".//input[@id='password']")
        password_input.send_keys(password)
        time.sleep(1)

        self._client.execute_script("document.getElementById('button_login').click()")
        self.wait_until("//ul//li[@id='headerCustomerInfo']")

    def extract(self):
        self._client.get("https://www.aa.com/aadvantage-program/profile/account-summary")
        member_details = self.wait_until("//div[contains(@class, 'member-details-container')]")

        res = {
            "status": self.find_element(member_details, ".//span[@data-test='member-info-tierlevel']").text,
            "500mile_upgrade": self.find_element(
                member_details, ".//span[@data-test='upgrades-500-mile upgrades']"
            ).text,
            "award_miles": self.find_element(member_details, ".//div[@data-test='member-info-awardmiles-value']").text,
            "expiring_on": self.find_element(member_details, ".//div[@data-test='award-miles-expiration']").text,
            "dollars": "",
            "miles": "",
            "segments": "",
        }
        qualification_container = self._client.find_element_by_xpath(
            "//div[contains(@class, 'progress-qualification-container')]"
        )
        res["dollars"] = (
            qualification_container.find_element_by_xpath(
                ".//div[@id='progressCircleGraph']//div[@id='container-eqd']"
                "//span[@data-test='summary-progress-graph-current-delta-dollars']"
            ).text
            + " / "
            + qualification_container.find_element_by_xpath(
                ".//div[@id='progressCircleGraph']//div[@id='container-eqd']"
                "//span[@data-test='summary-progress-graph-max-delta-dollars']"
            ).text
        )
        res["miles"] = (
            qualification_container.find_element_by_xpath(
                ".//div[@id='progressCircleGraph']//div[@id='container-eqm']"
                "//span[@data-test='summary-progress-graph-current-delta-miles']"
            ).text
            + " / "
            + qualification_container.find_element_by_xpath(
                ".//div[@id='progressCircleGraph']//div[@id='container-eqm']"
                "//span[@data-test='summary-progress-graph-max-delta-miles']"
            ).text
        )
        res["segments"] = (
            qualification_container.find_element_by_xpath(
                ".//div[@id='progressCircleGraph']//div[@id='container-eqs']"
                "//span[@data-test='summary-progress-graph-current-delta-segments']"
            ).text
            + " / "
            + qualification_container.find_element_by_xpath(
                ".//div[@id='progressCircleGraph']//div[@id='container-eqs']"
                "//span[@data-test='summary-progress-graph-max-delta-segments']"
            ).text
        )

        return res

    def start(self):
        self.login()
        print(self.extract())
        self._client.quit()


if __name__ == "__main__":
    crawler = AACrawler()
    crawler.start()
