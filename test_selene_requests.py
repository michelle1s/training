from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import json
import pytest
from hamcrest import equal_to, assert_that, is_in
from addict import Dict
import allure


def send_request(data):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("https://httpbin.org/forms/post")
    driver.find_element_by_name('custname').send_keys(data.name)
    driver.find_element_by_name('custtel').send_keys(data.phone)
    driver.find_element_by_name('custemail').send_keys(data.email)
    driver.find_element_by_xpath(f"//input[@value='{data.size}']").click()
    driver.find_element_by_name('delivery').send_keys(data.time)
    driver.find_element_by_name('comments').send_keys(data.comments)

    for top in data.toppings:
        driver.find_element_by_xpath(f"//input[@value='{top}']").click()

    driver.find_element_by_xpath('//button[text()="Submit order"]').click()
    content = driver.find_element_by_tag_name("body").text
    content_json = json.loads(content)
    driver.close()
    return content_json["form"]


@pytest.mark.parametrize('scenario', [
    Dict(name="Michelle", phone="0123456789", email="Michelle@gmail.com", size="large", toppings=["bacon", "onion"],
         time="12:45", comments="No comments")])
@allure.description('Check Pizza Ordering')
@allure.title('Pizza Ordering')
def test_input_data(scenario):
    result = send_request(scenario)
    print(result)
    assert_that(result['custname'], equal_to(scenario.name), "String should be equal")
    assert_that(result['custtel'], equal_to(scenario.phone), "String should be equal")
    assert_that(result['custemail'], equal_to(scenario.email), "String should be equal")
    assert_that(result['delivery'], equal_to(scenario.time), "String should be equal")
    assert_that(result['size'], equal_to(scenario.size), "String should be equal")
    assert_that(result['comments'], equal_to(scenario.comments), "String should be equal")

    if "toppings" in scenario.keys():
        user_toppings = result['topping']
        if type(user_toppings) != list:
            user_toppings = [user_toppings]

        for topping in scenario.toppings:
            assert_that(topping, is_in(user_toppings), "value in list")





