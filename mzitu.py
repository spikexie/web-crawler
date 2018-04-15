import urllib.request
from bs4 import BeautifulSoup

import re
import os
import socket

headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}


def get_url():
    page_url = []
    for page in range(1, 2):
        url = "http://www.mzitu.com/"
        request = urllib.request.Request(url)
        html = urllib.request.urlopen(request, timeout=20).read()
        soup = BeautifulSoup(html, 'lxml')
        lis = soup.find('ul', {'id': 'pins'}).find_all('li')
        for li in lis:
            page_url.append(li.find('a')['href'])
    return page_url


def get_page_num(page_url):
    request = urllib.request.Request(page_url)
    try:
        html = urllib.request.urlopen(request, timeout=20).read()
    except:
        try:
            html = urllib.request.urlopen(request, timeout=20).read()
        except:
            return None
    soup = BeautifulSoup(html, 'lxml')
    try:
        page_num = soup.find('div', {'class':'pagenavi'}).find_all('a')[-2].find('span').get_text()
    except:
        return None
    return int(page_num)


def get_img_url(url):
    request = urllib.request.Request(url)
    try:
        html = urllib.request.urlopen(request, timeout=20).read()
    except:
        try:
            html = urllib.request.urlopen(request, timeout=20).read()
        except:
            return None
    soup = BeautifulSoup(html, 'lxml')
    try:
        img_url = soup.find('div', {'class': 'main-image'}).find('p').find('a').find('img')['src']
    except:
        return None
    return img_url


def get_img_urls(page1_url):
    page_num = get_page_num(page1_url)
    if page_num is None:
        return None
    img_urls = []
    for page in range(1, page_num+1):
        url = page1_url + '/' + str(page)
        img_url = get_img_url(url)
        if img_url is None:
            return None
        else:
            img_urls.append(img_url)
    return img_urls


def get_img_title(page1_url):
    request = urllib.request.Request(page1_url)
    try:
        html = urllib.request.urlopen(request, timeout=20).read()
    except:
        try:
            html = urllib.request.urlopen(request,timeout=20).read()
        except:
            return None
    soup = BeautifulSoup(html, 'lxml')
    title = soup.find('h2', {'class': 'main-title'}).get_text()
    removeSign = re.compile(r'[\/:*?<>|]')
    title = re.sub(removeSign, '', title)
    return title
        

def download_imgs(page1_urls):
    img_urls = get_img_urls(page1_urls)
    if img_urls is None:
        return None
    if not os.path.exists('./妹子图/'):
        os.mkdir('./妹子图/')
    title = get_img_title(page1_urls)
    if title is None:
        return
    local_path = './妹子图/' + title
    if not os.path.exists(local_path):
        try:
            os.mkdir(local_path)
        except:
            pass
    if local_path is None or len(img_urls) == 0:
        return
    else:
        print('--开始下载' + title + '--')
        for img_url in img_urls:
            img_name = os.path.basename(img_url)
            print('正在下载' + img_name)
            print('from' + img_url)
            socket.setdefaulttimeout(10)
            try:
                urllib.request.urlretrieve(img_url, local_path + '/' + img_name)
            except:
                print('下载失败')
    print('--' + title + '下载完成--')


def craw_mzitu():
    page1_urls = get_url()
    if page1_urls is None or len(page1_urls) == 0:
        return
    else:
        for page1_url in page1_urls:
            download_imgs(page1_url)


def main():
    craw_mzitu()


if __name__ == '__main__':
    main()
print(__name__)



    






