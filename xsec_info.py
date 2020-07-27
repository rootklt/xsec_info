#!/usr/bin/env python3
#coding:utf-8

import os
import urllib
import requests
from bs4 import BeautifulSoup
from urllib.request import urlretrieve     #直接存储图片
from urllib.parse import urljoin, urlsplit, quote

headers = {"User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/1    7.0.963.56 Safari/535.11"}

RED = '\033[0;31;40m'
GREEN = '\033[0;32;40m'
RESET = '\033[0m'

def getArticleUrl(summary):
    '''
    从主页上获取所有文章的URL
    '''
    for aElement in summary.find_all('a'):
        href = aElement.get('href')
        if '/' not in href or './' in href:
            continue
        yield href 
    
def getArticleContent(url):
    '''
    获取文件主要内容
    '''

    #创建文件夹
    storepath ='.' + '/'.join(urlsplit(url).path.split('/')[:-1])
    if not os.path.exists(storepath):
        os.system('mkdir -p "{}"'.format(storepath))

    page = requests.get(url, headers = headers)

    #保存页面html源代码
    filename = '.' + urlsplit(url).path
    if not os.path.exists(filename):
        with open(filename, 'wb') as w:
            w.write(page.content)


    #下载图片
    soup = BeautifulSoup(page.content, 'lxml')
    img_tags = soup.select('section p img')
    for src in img_tags:
        imgpath = storepath + '/' + '/'.join(src.get('src').split('/')[:-1])

        #创建图片文件夹
        if not os.path.exists(imgpath):
            os.system('mkdir -p "{}"'.format(imgpath))

        imgurl = urljoin(url, src.get('src'))       #图片链接
        local_img = storepath + '/' + src.get('src')   #本地文件名

        if not os.path.exists(local_img):
            try:
                print('[*]Download image:', imgurl)
                imgurl = quote(imgurl).replace('http%3A', 'http:')
                urlretrieve(imgurl, local_img)
                print(GREEN, '[+]Downloaded', RESET)
            except:
                print(RED, '[-]Downlaod image failed:', imgurl, RESET)

def makeTemplate(url):
    page = requests.get(url, headers = headers)
    soup = BeautifulSoup(page.content, 'lxml')

    #保存首页
    with open('index.html', 'wb') as w:
        w.write(page.content)

    #页面很简单，用CSS和JS构建的页面,这里先下载CSS
    css_links = soup.find_all(name='link', attrs = {'rel': 'stylesheet'})

    for css in css_links:
        href = css.get('href')
        csspath = '/'.join(href.split('/')[:-1])
        if not os.path.exists(csspath):
            os.system('mkdir -p "{}"'.format(csspath))
        cssurl = urljoin(url, href)

        if not os.path.exists(href):
            with open(href, 'wb') as w:
                w.write(requests.get(cssurl).content)

    #下载页面依赖的JS
    js_links = soup.find_all(name='script')

    for js in js_links:
        js_src = js.get('src')

        if not js_src:
            continue
        jspath = '/'.join(js_src.split('/')[:-1])
        if not os.path.exists(jspath):
            os.system('mkdir -p "{}"'.format(jspath))

        jsurl = urljoin(url, js_src)
        if not os.path.exists(js_src):
            with open(js_src, 'wb') as js:
                js.write(requests.get(jsurl).content)

    #更新文章列表，以后在保存文章时从模板里提取
    summary = soup.find_all(class_='book-summary')[0]
    with open('templates/book-summary.html', 'wb') as book_sum:
        book_sum.write(str(summary).encode('utf-8'))
   
    return summary

def main():
    main_url = 'https://edu.csdn.net/notebook/python/'
    book_summary = makeTemplate(main_url)
    count = 1

    for url in getArticleUrl(book_summary):
        url = urljoin(main_url, url)
        print('[{}]: '.format(count), url)
        getArticleContent(url)
        count += 1


if __name__ == '__main__':
    main()
