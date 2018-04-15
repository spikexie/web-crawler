import urllib.request
import os
import socket
import re
from bs4 import BeautifulSoup


headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}


def get_url():
    page_urls = []
    url = "https://www.404cf.com/htm/piclist4/"
    request = urllib.request.Request(url, headers=headers)
    html = urllib.request.urlopen(request, timeout=20).read()
    soup = BeautifulSoup(html, 'lxml')
    lis = soup.find('div', {'class': 'box list channel'}).find('ul').find_all('li')
    for li in lis:
        page_urls.append(li.find('a')['href'])
    return page_urls


def get_img_num(theme_url):
    request = urllib.request.Request(theme_url, headers=headers)
    try:
        html = urllib.request.urlopen(request, timeout=20)
    except:
        try:
            html = urllib.request.urlopen(request, timeout=20)
        except:
            return None
    soup = BeautifulSoup(html, 'lxml')
    img_num = soup.find('div', {'class': 'content'}).find_all('a')
    return int(img_num)


def get_img_urls(theme_url):
    img_num = get_img_num(theme_url)
    img_urls = []
    request = urllib.request.Request(theme_url, headers=headers)
    html = urllib.request.urlopen(request, timeout=20).read()
    soup = BeautifulSoup(html, 'lxml')
    img_tag = soup.find('div', {'class': 'content'}).select('img')
    for i in range(0, img_num):
        img_urls.append(img_tag[i]['src'])
    return img_urls


def get_img_title(theme_url):
    request = urllib.request.Request(theme_url, headers=headers)
    try:
        html = urllib.request.urlopen(request, timeout=20)
    except:
        try:
            html = urllib.request.urlopen(html, timeout=20)
        except:
            return None
    soup = BeautifulSoup(html, 'lxml')
    img_title = soup.find('h2、')


