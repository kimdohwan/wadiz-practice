import re

from bs4 import BeautifulSoup
from django.db import models

from selenium import webdriver


# 메인페이지 크롤링
# - 상품 메인 문구(h2)
# - 사진(background_image_url)-
# - 분류(category)-
# - 회사명(company)-
# - 잔여일수(number_of_days_remaining)-
# - 도달률(rate_of_achivement)-
# - 펀딩액(cur_amount_of_funding)

# 디테일페이지 크롤링
# - 서포터 수(number_of_supporters)
# - 목표 금액(goal_amount)
# - 펀딩 기간(funding_duration)
# - 디테일 정보 html(description_html)

# 모델 설계 시 화면에 출력해서 보여줘야 하는 항목과 필수적인 attribute 속성들을 구분해서 설계하자
# 1. 모든 필요한 속성을 적어보기 -진행중
# 2. 모델의 필수 속성과 그 외의 것들을 분류(기본 attrbute 의 수치를 이용해서 동적으로 구분 가능한 것들)
#                    -> 그 외의 것들을 property 로 구현해야 하지 않을까?
# 3.


class Reward(models.Model):
    # 함수를 이용해서 크롤링한 카테고리 값을 설정해준다
    CHOICES_CATEGORY = []  # constants (상수)에 해당하는 값으로 대문자로 써주게 되면 class 의 field 값이 들어가지 않는다. 명배님이 알려준거 생각하자 잘못이해했다

    no = models.IntegerField()

    main_description = models.CharField(max_length=100)

    category = models.CharField(choices=CHOICES_CATEGORY, max_length=20)

    # 이미지를 media 파일에 저장, 일단 url 로 진행
    background_image_url = models.CharField(max_length=200)

    # forein key 로 user 연결 해줘야함
    company = models.CharField(max_length=50)

    # 투자 끝나는 날짜까지 남은 기한 동적으로 추적할 수 있게 만들 것
    number_of_days_remaining = models.CharField(max_length=50)

    # 목표액에 수식 적용해서 동적으로 설정 가능
    rate_of_achivement = models.CharField(max_length=50)

    # User.objects.filter(myreward=self) 에서 value 를 뽑아낸 값을 모두 더하면 동적인 수치가 나오지 않을까?
    cur_amount_of_funding = models.CharField(max_length=50)

    description_html = models.TextField()

    # len(Reward.objects.filter(reward_contibuted_user)) 동적설계?
    number_of_supporters = models.CharField(max_length=50)

    goal_amount = models.CharField(max_length=50)

    # 시작일, 마감일 두개로 나눌 것인가, 아니면 통째로 문자열로 지정할 것인가?
    # funding_duration = models.CharField

    @classmethod
    def crawl_main_page(cls):
        chrome_driver_path = '/home/kimdohwan/Downloads/chromedriver_linux64/chromedriver'
        driver = webdriver.Chrome(chrome_driver_path)

        url_main = 'https://www.wadiz.kr/web/wreward/main'
        driver.get(url_main)
        html = driver.page_source

        soup = BeautifulSoup(html, 'lxml')

        li_list = soup.select('ul._34FDqXUubQC345dbhWBh3o > li')
        for li in li_list:
            no = re.findall(
                r'\/(\d+)',
                li.select_one('a:nth-of-type(1)')['href']
            )[0]

            main_description = li.select_one('h4._3Mq3sAjD_F2tpQN5xlr7fy').get_text(strip=True)

            background_image_url = re.findall(
                r'\"(\S+)\"',
                li.select_one('span._3gmVBJTXNxBdKgoA_xSK3R')['style']
            )[0]

            category = li.select_one('span._1JCOjgeEis2hboba89en0C').string

            company = li.select_one('button._1XZwqXQKAz1Rfbk-czMXCl').string

            number_of_days_remaining = re.findall(
                r'\d+',
                li.select_one('span._2ytpGKsjZ9jevYYIimonTk').string
            )
            number_of_days_remaining = number_of_days_remaining[0] if number_of_days_remaining else '오늘마감'
            # if not number_of_days_remaining:
            #     number_of_days_remaining = '오늘마감'

            rate_of_achivement = re.findall(
                r'\d+',
                li.select_one('span._2bGDWMnFtEtsSX50mvvjXN').string
            )[0]

            cur_amount_of_funding = re.findall(
                r'\d*\W*\d*\W*\d*\W*\d*\W*\d*',
                li.select_one('span.gMWiodyJQonfslldKgpx4').string
            )[0]

            # 카테고리 종류 크롤링
            a_list = soup.select('a.TJ9occ9va1TXDH9ojcQ60')
            for category_string in a_list[1:]:
                cls.CHOICES_CATEGORY.append(category_string.select_one('span').string)

            Reward.objects.create(
                main_description=main_description,
                background_image_url=background_image_url,
                category=category,
                company=company,
                number_of_days_remaining=number_of_days_remaining,
                rate_of_achivement=rate_of_achivement,
                cur_amount_of_funding=cur_amount_of_funding,
            )
        driver.close()
