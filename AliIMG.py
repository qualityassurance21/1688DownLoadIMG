#!/usr/bin/env python
# encoding: utf-8
"""
@author: yangwei.1024
@file: AliIMG.py
@time: 2020-03-28 14:37
@desc: # 采集阿里巴巴商品图片数据
"""

from selenium import webdriver
import time
import requests
import os
import re


def crawle(url):
    browser = webdriver.Chrome()
    browser.get(url=url)

    # 将滚动条移动到页面的底部
    js = "var q=document.documentElement.scrollTop=100000"
    browser.execute_script(js)
    time.sleep(5)

    # 打印当前网页源码
    # print(browser.page_source)

    # 获取当前网页标题
    title = browser.title
    title = title.replace(" - 阿里巴巴", "")
    title = re.sub(r'[\|\/\<\>\:\*\?\\\"]', "_", title)
    print(title)

    os.makedirs(f"alibb/{title}/", exist_ok=True)

    # 获取当前网页链接
    website = browser.current_url
    print(website)

    # 创建txt文档并保存商品数据
    fname = 'spider'
    shopping = '%s%s%s%s' % (website, ":", title, '\n')
    with open(f"alibb/{fname}.txt", 'a+', encoding='utf-8') as f:
        f.write(shopping)
    print(f"保存{title}链接成功！")

    imgs_urls = []
    imgb_urls = []
    for link in browser.find_elements_by_xpath("//*[@src]"):  # 获取当前页面的src
        img_url = link.get_attribute('src')
        # 获取宝贝首图图片链接
        if "60x60" in img_url:
            if "jpg" in img_url:
                imgs_url = img_url.replace("60x60.jpg", "jpg")
            if "png" in img_url:
                imgs_url = img_url.replace("60x60.png", "png")
            print(imgs_url)
            imgs_urls.append(imgs_url)

        # 获取宝贝详情图片链接
        if "https://cbu01.alicdn.com/img/" in img_url:
            if "search" not in img_url:
                if "140x140xz" not in img_url:
                    if "summ" not in img_url:
                        if "x" not in img_url:
                            print(img_url)
                            imgb_urls.append(img_url)

    # 下载宝贝首图
    print(imgs_urls)
    x = 1
    for simgs in imgs_urls:
        if 'jpg' in simgs:
            imgs_name = f's{x}.jpg'
        if 'png' in simgs:
            imgs_name = f's{x}.png'
        rs = requests.get(simgs)
        with open(f"alibb/{title}/{imgs_name}", 'wb') as f:
            f.write(rs.content)
        x = x + 1
    print(f"下载宝贝首图成功！")

    # 下载宝贝详情图
    print(imgb_urls)
    y = 1
    for bimgs in imgb_urls:
        if 'jpg' in bimgs:
            imgb_name = f'{y}.jpg'
        if 'png' in bimgs:
            imgb_name = f'{y}.png'
        rs = requests.get(bimgs)
        with open(f"alibb/{title}/{imgb_name}", 'wb') as f:
            f.write(rs.content)
        y = y + 1

    print(f"下载宝贝详情图成功！")

    time.sleep(2)
    browser.quit()


if __name__ == '__main__':
    f = open("阿里商品链接.txt", "r")
    data = f.readlines()
    f.close()
    print(data)
    for url in data:
        url = url.replace('\n', '')
        print(url)
        crawle(url)