# -*- coding: utf-8 -*-

from selenium import webdriver
from time import sleep
from PIL import Image
from pytesseract import image_to_string
from os import getenv
from dotenv import load_dotenv

load_dotenv()

chrome_options_socks = webdriver.ChromeOptions()
proxy = '192.168.1.64:9050'
chrome_options_socks.add_argument('--disable-gpu')
chrome_options_socks.add_argument('--no-sandbox')
chrome_options_socks.add_argument('--headless')
chrome_options_socks.add_argument('--proxy-server=socks5://' + proxy)
driver_proxy = webdriver.Chrome(r'/home/user/chromedriver', chrome_options=chrome_options_socks)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(r'/home/user/chromedriver', chrome_options=chrome_options)
name = getenv('LOGIN')
passwd = getenv('PASSWORD')
captcha_img = '/home/user/python/vpn/captcha_vpnbook.png'


def get_password():
    driver_proxy.get("https://www.vpnbook.com/freevpn")
    sleep(3)
    captcha = driver_proxy.find_element_by_xpath('//*[@id="pricing"]/div/div[3]/ul/li[11]/img')
    captcha.screenshot('captcha_vpnbook.png')
    driver_proxy.quit()
    password = image_to_string(Image.open('captcha_vpnbook.png'))
    return password


def autorization(name, passwd):
    driver.get("http://192.168.1.1/index.asp")
    username = driver.find_element_by_name('login_username')
    username.send_keys(name)
    p = driver.find_element_by_name('login_passwd')
    p.send_keys(passwd)
    driver.find_element_by_xpath('//input[@class="button"]').click()


def turn_on_vpn():
    driver.get("http://192.168.1.1/Advanced_OpenVPNClient_Content.asp")
    sleep(3)
    if driver.find_element_by_id("vpn_state_msg").text == "Connected":
        driver.quit()
    else:
        driver.find_element_by_class_name('iphone_switch').click()
        sleep(15)
        driver.get("http://192.168.1.1/Advanced_OpenVPNClient_Content.asp")
        sleep(3)
        if driver.find_element_by_id("vpn_state_msg").text == "Connected":
            driver.quit()
        else:
            input_password = driver.find_element_by_name('vpn_client_password')
            input_password.clear()
            input_password.send_keys(get_password())
            submit = driver.find_element_by_name('button')
            submit.click()
            sleep(15)
            driver.get("http://192.168.1.1/Advanced_OpenVPNClient_Content.asp")
            sleep(3)
            if driver.find_element_by_id("vpn_state_msg").text == "Connected":
                driver.quit()
            else:
                driver.quit()


def main():
    try:
        autorization(name, passwd)
        turn_on_vpn()
        driver.quit()
        driver_proxy.quit()
    except:
        driver.quit()
        driver_proxy.quit()


if __name__ == '__main__':
    main()
