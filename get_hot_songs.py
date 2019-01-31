#! /usr/bin/env python

from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv


def parse_html_page(html):
    soup = BeautifulSoup(html, 'lxml')
    items = soup.find_all('span', 'txt')
    return items


def write_to_csv(items, artist_name):

    with open("music163_songs.csv", "a", encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        for item in items:
            writer.writerow([item.a['href'].replace('/song?id=', ''), item.b['title']])
    csvfile.close()


def read_csv():

    with open("music163_artists.csv", "r", encoding='utf-8', newline="") as csvfile:

        reader = csv.reader(csvfile)
        for row in reader:
            artist_id, artist_name = row
            if str(artist_id) is "artist_id":
                continue
            else:
                yield artist_id, artist_name


def main():
    driver = webdriver.Chrome()
    for readcsv in read_csv():
        artist_id, artist_name = readcsv
        url = "https://music.163.com/#/artist?id=" + artist_id
        try:
            print("正在获取{}的热门歌曲...".format(artist_name))
            driver.get(url)
            driver.switch_to_frame("g_iframe")
            time.sleep(3)
            html = driver.page_source
            items = parse_html_page(html)
            print("{}的热门歌曲获取完成!".format(artist_name))
            print("开始将{}的热门歌曲写入文件".format(artist_name))
            write_to_csv(items, artist_name)
            print("{}的热门歌曲写入到本地成功!".format(artist_name))
        except:
            print('...')


if __name__ == "__main__":
    main()
