from django.test import TestCase

# Create your tests here.
from .models import Reward


class Rewardtest(TestCase):
    Reward.crawl_main_page()
