from selenium import webdriver
import json
import pytest
from hamcrest import *


@pytest.fixture(scope='session')
def set_up():
    chromedriver_location = "/usr/bin/chromedriver"
    driver = webdriver.Chrome(chromedriver_location)
    driver.get("https://httpbin.org/forms/post")

    costumer_name = "/html/body/form/p[1]/label/input"
    phone = "/html/body/form/p[2]/label/input"
    email = "/html/body/form/p[3]/label/input"
    large_pizza = "/html/body/form/fieldset[1]/p[3]/label/input"
    top_bacon = "/html/body/form/fieldset[2]/p[1]/label/input"
    top_onion = "/html/body/form/fieldset[2]/p[3]/label/input"
    delivery_time = "/html/body/form/p[4]/label/input"
    comments = "/html/body/form/p[5]/label/textarea"
    submit = "/html/body/form/p[6]/button"

    driver.find_element_by_xpath(costumer_name).send_keys("Michelle")
    driver.find_element_by_xpath(phone).send_keys("0123456789")
    driver.find_element_by_xpath(email).send_keys("Michelle@gmail.com")
    driver.find_element_by_xpath(large_pizza).click()
    driver.find_element_by_xpath(top_bacon).click()
    driver.find_element_by_xpath(top_onion).click()
    driver.find_element_by_xpath(delivery_time).send_keys("12:45PM")
    driver.find_element_by_xpath(comments).send_keys("No comments")
    driver.find_element_by_xpath(submit).click()
    content = driver.find_element_by_tag_name("body").text

    content_json = json.loads(content)
    driver.close()
    return content_json["form"]


def test_custname(set_up):
    assert_that(set_up['custname'], matches_regexp('^[A-Za-z]+'),"String should match")


def test_custemail(set_up):
    assert_that(set_up['custemail'], matches_regexp('^[\w]+[@][\w]+\.[\w]+$'),"String should match")


def test_custtel(set_up):
    assert_that(set_up['custtel'], matches_regexp('^\d{10}'),"Number contain 10 digits")

def test_delivery(set_up):
    assert_that(set_up['delivery'], matches_regexp('^(1[1-9]|2[0-3]):(00|15|30|45)$'),"Time between 11:00-23:45")


def test_size(set_up):
    assert_that(set_up['size'], is_in(['large','medium','small]']),"value in list")


def test_topping(set_up):
    valid_topping = ["bacon","onion","mushroom","extra cheese"]
    if "topping" in set_up.keys():
        user_toppings = set_up['topping']
        if type(user_toppings) != list:
            user_toppings = [user_toppings]

        for topping in user_toppings:
            assert_that(topping, is_in(valid_topping),"value in list")