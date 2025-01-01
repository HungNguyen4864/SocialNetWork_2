
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

class FacebookGroupMemberCrawl:
    def __init__(self, username, password, group_id, scroll_count):
        print("\n====== Facebook Group Member Scraper ======")
        self.email = username
        self.password = password
        self.group_id = group_id
        self.scroll_count = scroll_count
        self.setup_driver()

    def setup_driver(self):
        try:
            self.driver = webdriver.Chrome()
            self.driver.maximize_window()
        except Exception as e:
            print(f"Error: {e}")

    def login(self):
        try:
            self.driver.get("https://www.facebook.com/")
            self.driver.implicitly_wait(10)
            self.driver.find_element(By.ID, "email").send_keys(self.email)
            self.driver.find_element(By.ID, "pass").send_keys(self.password)
            self.driver.find_element(By.NAME, "login").click()
            time.sleep(10)
            print('Login success')
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def get_group_members(self):
        try:
            self.driver.get(f"https://www.facebook.com/groups/{self.group_id}/members")
            time.sleep(5)
            members = set()
            for i in range(self.scroll_count):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
                print(f"Scroll {i+1}/{self.scroll_count}")
                user_elements = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='/user/']")
                print(len(user_elements))
                for user in user_elements:
                    try:
                        href = user.get_attribute("href")
                        if '/user/' in href:
                            user_id = href.split('/user/')[1].split('?')[0].strip('/')
                            name = user.text
                            members.add((user_id, name))
                            print(f"Member: {user_id} - {name}")
                    except Exception as e:
                        continue
            return list(members)
        
        except Exception as e:
            print(f"Error: {e}")

    def save_to_excel(self, members):
        try:
            file_name = f"all_group_members.xlsx"
            df = pd.DataFrame(members, columns=["User ID", "Name"])
            df_clean = df[df['Name'].str.strip() != '']
            df_clean.to_excel(file_name, index=False)
            print(f"Data saved to {file_name}")
        except Exception as e:
            print(f"Error: {e}")
