from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import time
import pandas as pd
class FacebookGroupPostCrawl:
    def __init__(self, username, password, group_id, scroll_count):
        print("\n====== Facebook Group post Scraper ======")
        self.email = username
        self.password = password
        self.group_id = group_id
        self.scroll_count = scroll_count
        self.setup_driver()

    def setup_driver(self):
        try:
            options = Options()
            options.add_argument("--headless")
            options.add_argument("--disable-notifications") 
            self.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()), 
                options=options,
            )
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
        
    def get_group_posts(self):
        try:
            self.driver.get(f"https://www.facebook.com/groups/{self.group_id}/?sorting_setting=RECENT_ACTIVITY")
            time.sleep(5)
            postlist = set()
            i=0
            count_loop = 0
            while len(postlist) <= self.scroll_count:
                check_len_postlist = len(postlist)
                print(check_len_postlist)
                self.driver.execute_script("return document.body.scrollHeight")
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(5) 
                post_elements = self.driver.find_elements(By.XPATH, "//div[contains(@role, 'article')]")
                print(f"Found {len(post_elements)} post elements on scroll {i+1}")
                for post in post_elements:
                    try:
                        content = post.text.strip()
                        post_user = content.split('\n')[0]
                        post_content = content.split('\n')[1]
                        post_id_element = post.find_element(By.XPATH, ".//a[contains(@href, '/posts/')]")
                        post_id = post_id_element.get_attribute("href").split("/")[-2]
                        # print(f"Post ID: {post_id}, Post User: {post_user}, Post Content: {post_content}")
                        postlist.add((post_id,post_user,post_content))
                    except Exception as e:
                        continue
                print('-------------')
                print(len(postlist))
                print('-------------')
                if len(postlist) == check_len_postlist:
                    count_loop+=1
                    if count_loop == 10:
                        break
                i+=1
            return list(postlist)
        except Exception as e:
            print(f"{e}")
            
    def get_post_reactions(self,post_id):
        try:
            self.driver.get(f"https://www.facebook.com/groups/{self.group_id}/posts/{post_id}/") 
            time.sleep(10)
            self.driver.execute_script("return document.body.scrollHeight")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(10)
            xpaths = [
            "//span[@class='xrbpyxo x6ikm8r x10wlt62 xlyipyv x1exxlbk']",
            "//span[@class='xrbpyxo x6ikm8r x10wlt62 xlyipyv x1exxlbk']//span[contains(text(), '2')]"
            ] 
            for xpath in xpaths:
                try:
                    reaction_button = self.driver.find_element(By.XPATH, xpath)
                    print("Found element with XPath:", xpath)
                    self.driver.execute_script("arguments[0].click();", reaction_button)
                    time.sleep(5)
                    break
                except Exception as e:
                    print(f"Failed for XPath: {xpath}, Error: {e}")
            reactions = set()
            user_elements = self.driver.find_elements(By.XPATH, "//a[contains(@href, '/user/')]")
            for user in user_elements:
                try:
                    user_name = user.text.strip()
                    user_id = user.get_attribute("href").split("/user/")[1].split("/")[0]
                    print(f"Name: {user_name}, User ID: {user_id}")
                    reactions.add((user_id,user_name))
                except Exception as e:
                    print(f"Error processing reaction: {e}")
                    continue
            return list(reactions)
        except Exception as e:
            print(f"Error fetching reactions: {e}")
            return []
    def get_post_comments(self,post_id):
            try:
                self.driver.get(f"https://www.facebook.com/groups/{self.group_id}/posts/{post_id}/") 
                time.sleep(10)
                self.driver.execute_script("return document.body.scrollHeight")
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
                xpaths = [
                "//span[@class='xrbpyxo x6ikm8r x10wlt62 xlyipyv x1exxlbk']",
                "//span[@class='xrbpyxo x6ikm8r x10wlt62 xlyipyv x1exxlbk']//span[contains(text(), '2')]"
                ] 
                for xpath in xpaths:
                    try:
                        reaction_button = self.driver.find_element(By.XPATH, xpath)
                        print("Found element with XPath:", xpath)
                        self.driver.execute_script("arguments[0].click();", reaction_button)
                        time.sleep(5)
                        break
                    except Exception as e:
                        print(f"Failed for XPath: {xpath}, Error: {e}")
                reactions = set()
                user_elements = self.driver.find_elements(By.XPATH, "//a[contains(@href, '/user/')]")
                for user in user_elements:
                    try:
                        user_name = user.text.strip()
                        user_id = user.get_attribute("href").split("/user/")[1].split("/")[0]
                        # print(f"Name: {user_name}, User ID: {user_id}")
                        reactions.add((user_id,user_name))
                    except Exception as e:
                        print(f"Error processing reaction: {e}")
                return list(reactions)
            except Exception as e:
                print(f"Error fetching reactions: {e}")
                return []
    def get_detail_each_post(self,file_path):
        data = pd.read_excel(file_path)
        post_ids = data['post_id']
        print(post_ids)
        detailpost = set()
        for post in post_ids:
            try:
                post_reaction = self.get_post_reactions(post)
                detailpost.add((post, tuple(post_reaction)))
                self.save_reactions_to_excel(detailpost)
            except Exception as e:
                print(f"Error processing post: {e}")

        return list(detailpost)

    def save_post_to_excel(self, postlist):
        try:
            file_name = f"ex_post.xlsx"
            df = pd.DataFrame(postlist, columns=["post_id", "post_user",'post_content'])
            df.to_excel(file_name, index=False)
            print(f"Post data saved to {file_name}")
        except Exception as e:
            print(f"Error saving posts to Excel: {e}")
    def save_reactions_to_excel(self, detailpost):
        try:
            file_name = f"ex_reactions.xlsx"
            df = pd.DataFrame(detailpost, columns=["post_id", "list_reactions"])
            df.to_excel(file_name, index=False)
            print(f"Reaction data saved to {file_name}")
        except Exception as e:
            print(f"Error saving reactions to Excel: {e}")
        