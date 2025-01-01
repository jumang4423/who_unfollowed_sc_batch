from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os
import platform


def get_driver():
    options = Options()
    # options.add_argument("--headless")
    options.add_argument("--disable-gpu")  # Windows向けの設定
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--enable-unsafe-swiftshader")  # Added flag for WebGL fallback

    # ChromeDriverManagerを使用して自動的にドライバーをセットアップ
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    print("Chrome Driver created")
    return driver
