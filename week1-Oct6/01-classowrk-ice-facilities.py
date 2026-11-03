# %% [markdown]
# ## Project: Scrape ICE Detention Facilities Website
# 
# **Description:** Scrape the ICE website for information about its detention facilities, including names and addresses.
# 
# **Goal:** Map the locations of ICE detention facilities to see how widely they are spread across the country. For example:
# 
# - Which state has the most ICE detention facilities?
# - What does a comparison of border and interior states reveal?
# - What other patterns emerge from the map?

# %% [markdown]
# 1. Fetch page content

# %%
base_url = 'https://www.ice.gov/detention-facilities'

# %%
import requests

# %%
headers= {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36'}
response = requests.get(base_url, headers=headers)

response.raise_for_status(), response.status_code

# %%
response.text[:5000]

# %%
# !pip install beautifulsoup4

# %%


# %%
from bs4 import BeautifulSoup
content=BeautifulSoup(response.text, 'html.parser')

content

# %% [markdown]
# 2. Extract the number of pages

# %%
# pagination_content=content.find_all('nav', class_="usa-pagination")

# %%
# for li in pagination_content:
#     lis=li.find_all('li')
#     for l in lis:
#         print(l)


# %%
pagination_content=content.find_all("li", class_="usa-pagination__item usa-pagination__page-no")

# %%
pages=[]
for li in pagination_content: 
    pages.append(li.get_text().strip())

pages

# %%
page_nums=[]
for li in pagination_content:
    page_nums.append(li.find('a')['href'])
page_nums

# %%
import numpy as np

np.arange(0, 8)

# %% [markdown]
# 3. Scrape the first page

# %%
grid_content=content.find_all('li', class_='grid')

# %%
grid_content[0].find_all("span")

# %%
grid_list = []
for grid in grid_content:
    facility_name = grid.find("span", class_="field-content").get_text().strip()
    address = grid.find('p', class_="address").get_text().strip()
    administrative_area = grid.find("span", class_="administrative-area").get_text().strip()
    postal_code = grid.find("span", class_="postal-code").get_text().strip()
    image_src = "https://www.ice.gov" + grid.find("img").get("src")

    grid_list.append({
        "facility_name": facility_name,
        "address": address,
        "administrative_area": administrative_area,
        "postal_code": postal_code,
        "image_src": image_src
    })


# %%

import pandas as pd

df=pd.DataFrame(grid_list)
df.head()

# %%
df.shape

# %% [markdown]
# 4. Scrape all pages

# %%
pages

# %%
headers= {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36'}

dfs=[]
for page in pages:
    page_url = base_url + "?page=" + str(int(page) - 1)

    response = requests.get(page_url, headers=headers)

    print(page_url, response.status_code)

    grid_list = []
    for grid in grid_content:
        facility_name = grid.find("span", class_="field-content").get_text().strip()
        address = grid.find('p', class_="address").get_text().strip()
        administrative_area = grid.find("span", class_="administrative-area").get_text().strip()
        postal_code = grid.find("span", class_="postal-code").get_text().strip()
        image_src = "https://www.ice.gov" + grid.find("img").get("src")

        grid_list.append({
            "facility_name": facility_name,
            "address": address,
            "administrative_area": administrative_area,
            "postal_code": postal_code,
            "image_src": image_src
        })

    
    df=pd.DataFrame(grid_list)
    # print(df.shape)
    dfs.append(df)


df=pd.concat(dfs, ignore_index=True)


df.shape

# %%
import os

os.mkdir("scraped_data")

df.to_csv("scraped_data/ice_facilities.csv", index=False)

# %%


# %%


# %% [markdown]
# 5. Check for errors

# %%


# %%


# %%


# %%


# %% [markdown]
# 6. Scrape facility page

# %%


# %%


# %%


# %%


# %% [markdown]
# 7. Save save save

# %%


# %%


# %%


# %% [markdown]
# 8. Read file

# %%


# %%


# %%


# %% [markdown]
# 9. Extract Zip and state

# %%


# %%


# %%


# %% [markdown]
# 8. Geocode

# %%


# %%


# %%


# %%


# %%


# %% [markdown]
# 9. Map it

# %%


# %%


# %%


# %% [markdown]
# 10. Download Images

# %%


# %%


# %%


# %%


# %% [markdown]
# 11. do something fun with it

# %%


# %%


# %%


# %%


# %% [markdown]
# -------------

# %% [markdown]
# 


