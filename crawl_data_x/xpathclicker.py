import time
from selenium.webdriver.common.by import By

class XPathClicker:
    def __init__(self, driver):
        self.driver = driver

    def click_elements(self, xpaths, repeat=1):
        """Duyệt qua danh sách XPath, tìm và click vào phần tử đầu tiên có thể, lặp lại nếu cần."""
        for xpath in xpaths:
            for attempt in range(repeat):
                try:
                    element = self.driver.find_element(By.XPATH, xpath)
                    print(f"Attempt {attempt + 1}: Found element with XPath:", xpath)
                    self.driver.execute_script("arguments[0].click();", element)
                    time.sleep(5)
                    break  
                except Exception as e:
                    break
        return False  

    def execute(self):
        """Thực hiện các hành động click theo thứ tự ưu tiên XPath."""
        xpath_groups = [
            [
                "//div[contains(@class, 'x9f619') and contains(@class, 'x1n2onr6') and contains(@class, 'x1ja2u2z') and contains(@class, 'xt0psk2')]//i[@data-visualcompletion='css-img']"
            ],
            [
                "//div[contains(@class, 'xu06os2') and contains(@class, 'x1ok221b')]//span[contains(text(), 'All comments')]"
            ],
            [
                "//span[contains(@class, 'html-span')]//span[contains(text(), 'View more comments')]"
            ]
        ]

        for index, xpaths in enumerate(xpath_groups):
            repeat = 3 if index == 2 else 1  
            if self.click_elements(xpaths, repeat=repeat):
                break 

# Sử dụng class này:
# driver = ...  # Selenium WebDriver instance
# clicker = XPathClicker(driver)
# clicker.execute()
