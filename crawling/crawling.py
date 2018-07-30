#!/usr/bin/env python
import os
import re

import requests
from bs4 import BeautifulSoup

from selenium import webdriver

## ==========파일 저장해서 쓰기==============
# dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'html_wadiz')
# file_path = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), dir_path), 'wadiz_reward_detail.html')
#
# if os.path.exists(file_path):
#     html = open(file_path, 'rt').read()
# else:
#     os.makedirs(dir_path, exist_ok=True)
#
#     url_main = 'https://www.wadiz.kr/web/wreward/main'
#     chrome_driver_path = '/home/kimdohwan/Downloads/chromedriver_linux64/chromedriver'
#     driver = webdriver.Chrome(chrome_driver_path)
#     driver.get(url_main)
#     html = driver.page_source
#
#     open(file_path, 'wt').write(html)
## =======================================

# 셀레니엄 크롬 드라이버 변수 설정
chrome_driver_path = '/home/kimdohwan/Downloads/chromedriver_linux64/chromedriver'
driver = webdriver.Chrome(chrome_driver_path)

# 메인페이지 크롤링
# - 상품 메인 문구(h2)
# - 사진(background_image_url)-
# - 분류(category)-
# - 회사명(company)-
# - 잔여일수(number_of_days_remaining)-
# - 도달률(rate_of_achivement)-
# - 펀딩액(amount_of_funding)
url_main = 'https://www.wadiz.kr/web/wreward/main'
driver.get(url_main)
html = driver.page_source

soup = BeautifulSoup(html, 'lxml')

li_list = soup.select('ul._34FDqXUubQC345dbhWBh3o > li')
for li in li_list:
    h4 = li.select_one('h4._3Mq3sAjD_F2tpQN5xlr7fy').get_text(strip=True)

    background_image = li.select_one('div._3gmVBJTXNxBdKgoA_xSK3R')['style']
    background_image_url = re.findall('\"\S*\"', background_image)

    category = li.select_one('span._1JCOjgeEis2hboba89en0C').string

    company = li.select_one('button._1XZwqXQKAz1Rfbk-czMXCl').string

    number_of_days_remaining = li.select_one('span._2ytpGKsjZ9jevYYIimonTk').string

    rate_of_achivement = li.select_one('span._2bGDWMnFtEtsSX50mvvjXN').string

    amount_of_funding = li.select_one('span.gMWiodyJQonfslldKgpx4').string

# 디테일페이지 크롤링
# - 서포터 수(number_of_suppoters)
# - 목표 금액(goal_amount)
# - 펀딩 기간(funding_duration)
# - 디테일 정보 html(description_html)
url_detail = 'https://www.wadiz.kr/web/campaign/detail/21754'
driver.get(url_detail)
html = driver.page_source

soup = BeautifulSoup(html, 'lxml')

number_of_suppoters = soup.select('p.total-supporter')[0].select_one('strong').string

div_with_style = soup.find('div', {'style': 'padding:20px;background:#eafbf7;background:rgba(0, 204, 163, 0.1)'})
p = div_with_style.select('p')[0].get_text(strip=True)
goal_amount = re.findall(r'금액(\S+)원', p)[0]
funding_duration = re.findall(r'기간(\S+)', p)[0]

description = soup.select_one('div.inner-contents')
description_html = description.prettify()

# description_path = os.path.join(dir_path, 'description.html')
# open(description_path, 'wt').write(description_html)

driver.close()
