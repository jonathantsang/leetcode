from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import sys

browser = webdriver.Chrome("/Users/Jon/Downloads/chromedriver") # directory of chromedriver
URL = "https://leetcode.com/contest/{}/ranking/{}/"
savedir = "./scraped/"

# Populate contests[] with arguments like "weekly-contest-197"
contests = sys.argv[1:]

# Read results
ZERO = "###@@@ZERO@@@###"
for i, contest in enumerate(contests):
    fname = str(i).zfill(3) + contest + ".txt"
    fname = savedir + fname
    try:
        with open(fname, encoding="utf-8") as fi:
            res = fi.read()
        if res:
            print("skipping", fname)
            continue
    except:
        pass

    print("starting", fname)
    results = []
    firstzero = False
    for d in range(1, 11111):
        url = URL.format(contest, str(d))
        browser.get(url)
        try:
            myElem = WebDriverWait(browser, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "ranking-username"))
            )
        except:
            break
        soup = BS(browser.page_source, "html.parser")
        names = soup.find_all("a", {"class": "ranking-username"})
        found = False
        for name in names:
            found = True
            if firstzero is False:
                score = name.next_element.next_element.next_element.next_element.next_element.text

                if score == "0":
                    results.append(ZERO)
                    firstzero = True
            results.append(name.text)

        if not found:
            break

    print("!", contest, len(results))
    with open(fname, "w", encoding="utf-8") as fo:
        fo.write("\n".join(results))

driver.close()
print("done")
