import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def get_news():
    # optiune pentru a ramane deschisa fereastra
    options = Options()
    options.add_experimental_option('detach', True)
    options.add_argument('headless')       # not open the Chrome window
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.watchathletics.com/headlines/all/")


    # select title, link, date
    elements = driver.find_elements(By.CLASS_NAME, "page_headline_container")

    # create dictionary to save the articles
    articles = {}
    i = 0
    for element in elements:
        partition = element.find_element(By.TAG_NAME,"a")
        date = element.find_element(By.TAG_NAME, "strong")
        link = partition.get_attribute("href")
        title = partition.get_attribute("title")
        date = date.text

        articles[i] = {
            "date": date,
            "title": title,
            "link": link,
        }
        i = i+1

    #print(articles)
    driver.quit()


    # get actual date
    day = datetime.datetime.now()
    now = day.strftime("%d %B %Y")
    #print(now)

    day_articles = {}
    j=0
    # get all articles from today
    for n in range(len(articles)):
        # if articles[n]["date"] == now:
            day_articles[j] = articles[n]
            j = j+1

    #print((day_articles[0]))
    return day_articles

