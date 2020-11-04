import os
import time

import requests
from bs4 import BeautifulSoup
from requests.compat import urljoin
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


base_url = "https://www.advertisingarchives.co.uk/"
out_path = "data/images"

url_range = list(range(1, 26))
with open("data/image_metadata.tsv", "w") as outfile:
    h = "Number\tDecade\tCountry\tSource\tFile\n"
    outfile.write(h)
    for i in url_range:
        print(i)
        url = f"https://www.advertisingarchives.co.uk/?service=search&action=do_quick_search&language=en&mode=&q=womens&qw=&page={i}&grid_layout=4&grid_thumb=2&md_1=USA&md_2="
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        drvr = webdriver.Chrome(
            ChromeDriverManager().install(), chrome_options=chrome_options
        )
        # drvr = webdriver.Chrome(ChromeDriverManager().install())
        drvr.get(url)
        time.sleep(10)
        html = drvr.page_source
        drvr.close()
        time.sleep(1)
        soup = BeautifulSoup(html, "lxml")
        imgs = soup.find_all("div", {"class": "pictureBox test"})
        noi = 0
        for img in imgs:
            try:
                sub_soup = BeautifulSoup(str(img), "lxml")
                picture_link = sub_soup.find("img")
                img_details = sub_soup.find("div", {"class": "imageDetails"})
                img_details = img_details.text.strip().split("\n")
                img_details = [e.strip() for e in img_details if len(e) > 0][:2]
                img_number, img_meta = img_details[0], img_details[1]
                img_meta = img_meta.split(" ")
                decade = img_meta[0]
                country = img_meta[1]
                source = " ".join(img_meta[2:]).strip()
                picture_link = urljoin(base_url, picture_link["src"])
                fname = picture_link.split("/")[-1]
                with open(os.path.join(out_path, fname), "wb") as img_file:
                    r = requests.get(picture_link)
                    img_file.write(r.content)
                o = (
                    img_number
                    + "\t"
                    + decade
                    + "\t"
                    + country
                    + "\t"
                    + source
                    + "\t"
                    + fname
                    + "\n"
                )
                outfile.write(o)
                noi += 1
            except Exception as e:
                print("Failed")
                continue
        print(f"Downloaded {noi} images from {i}")
