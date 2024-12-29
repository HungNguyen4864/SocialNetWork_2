from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import getpass
from datetime import datetime
import os
import pandas as pd
class FacebookGroupScraper:
    def __init__(self):
        print("\n======Facebook group member scraper======")
        self.get_config()
        self.setup_driver()
    def get_config(self):
        try:
            print('Input your username:')
            self.email = input("Email/Username: ").strip()
            self.password = getpass.getpass("Password: ")
            
            print('\n Input ID Group facebook:')
            self.group_id = input("Group ID: ").strip()

            print('\nInput srcoll number:')
            self.scroll_count = int(input("Scroll number (default 5): ") or "5")

        except Exception as e:
            print(f"Error: {e}")
    
    def setup_driver(self):
        try:
            self.driver = webdriver.Chrome()
            self.driver.maximize_window()
            # self.driver.get("https://www.facebook.com/")
            # self.driver.implicitly_wait(10)
        except Exception as e:
            print(f"Error: {e}")
            pass
    
    def login(self):
        try:
            self.driver.get("https://www.facebook.com/")
            self.driver.implicitly_wait(10)
            email_input = self.driver.find_element(By.ID, "email").send_keys(self.email)
            password_input = self.driver.find_element(By.ID, "pass").send_keys(self.password)
            login_button = self.driver.find_element(By.NAME, "login").click()
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
                self.driver.web
                print(f"Scroll {i+1}/{self.scroll_count}")

                user_elements = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='/user/']")
                # print(len(user_elements))
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
            file_name = f"{self.group_id}.xlsx"
            df = pd.DataFrame(members, columns=["User ID", "Name"])
            print(df.head())
            df = df[~df['User ID'].str.contains("contributions", na=False, case=False)]
            df_clean = df[df['Name'].str.strip() != '']
            df_clean.to_excel(file_name, index=False)
            print(f"Data saved to {file_name}")
        except Exception as e:
            print(f"Error: {e}")
            pass
def main():
    scraper = None
    try:
        scraper = FacebookGroupScraper()
        if scraper.login():
            print('-----------------')
            members = scraper.get_group_members()
            scraper.save_to_excel(members)
            time.sleep(15)
    except Exception as e:
        pass

if  __name__== "__main__":
    main()