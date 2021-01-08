from bs4 import BeautifulSoup
import requests
import os

def crawl_heroes(heroLink):
    link = heroLink.get("href")
    heroPage = requests.get(link)
    heroSoup = BeautifulSoup(heroPage.content, 'html.parser')
    heroName = heroSoup.find("h1").text
    heroPortrait = heroSoup.find("img", {"id": "heroTopPortraitIMG"}).get("src")
    get_image(heroName, heroPortrait)

def get_image(hero, image_url):
    print("Getting img for " + hero)
    img_data = requests.get(image_url).content
    with open("./heroes/" + hero + ".jpg", 'wb') as handler:
        handler.write(img_data)

if __name__ == "__main__":

    page = requests.get("https://www.dota2.com/heroes/")

    soup = BeautifulSoup(page.content, 'html.parser')
    heroLinks = soup.findAll("a", {"class": "heroPickerIconLink"})
    for heroLink in heroLinks:
        crawl_heroes(heroLink)