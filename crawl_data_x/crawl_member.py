# %%
import time
import pandas as pd
from groupmembercrawl import FacebookGroupMemberCrawl
from grouppostcrawl import FacebookGroupPostCrawl


# %%
username = 'phanmthihoa05@gmail.com'
password = 'Hung26082003'
group_id = '811896080494851'
scroll_count = 1500
try:
    scraper = FacebookGroupPostCrawl(username= username, password = password, group_id = group_id, scroll_count= scroll_count)
    if scraper.login():
        print('-----------------')
        # postlist = scraper.get_group_posts()
        # scraper.save_post_to_excel(postlist)
        file_path = 'ex_post.xlsx'
        deitalpost = scraper.get_detail_each_post_comments(file_path)
        scraper.save_comments_to_excel(deitalpost)
        time.sleep(10)
except Exception as e:
    pass

# %%
# def save_to_excel(members):
#             file_name = f"ex_post.xlsx"
#             df = pd.DataFrame(members, columns=["Post ID", "type"])
#             df.to_excel(file_name, index=False)
#             print(f"Data saved to {file_name}")
# save_to_excel(all_post)

# %%



