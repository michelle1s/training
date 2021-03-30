import requests
import pytest
from hamcrest import assert_that, equal_to, contains_string
from addict import Dict
import allure


def calculate_req(params):
    req = requests.get('http://api.mathjs.org/v4/', params=params)
    print(req.url)
    return req.text


@pytest.mark.parametrize('scenario', [
    Dict(params={"expr": "1+2"}, expected="3"),
    Dict(params={"expr": "1.2+3.3"}, expected="4.5"),
    Dict(params={"expr": "1000000000000+1000000000000"}, expected="2e+12"),
    Dict(params={"expr": "-5+-6"}, expected="-11")
], ids=lambda x: str(x.params.expr))
@allure.description('Check addition operator')
@allure.title('Addition operator')
def test_add(scenario):
    params = {'expr': scenario.params.expr}
    value = calculate_req(params)
    assert_that(value, equal_to(scenario.expected), 'Compare result to expected value')


@pytest.mark.parametrize('scenario', [
    Dict(params={"expr": "1-2"}, expected="-1"),
    Dict(params={"expr": "3.5-2.4"}, expected="1.1"),
    Dict(params={"expr": "-1000000000000-1000000000000"}, expected="-2e+12")
], ids=lambda x: str(x.params.expr))
@allure.description('Check sub operator')
@allure.title('Sub operator')
def test_sub(scenario):
    params = {'expr': scenario.params.expr}
    value = calculate_req(params)
    assert_that(value, equal_to(scenario.expected), 'Compare result to expected value')


@pytest.mark.parametrize('scenario', [
    Dict(params={"expr": "1/#"}, expected="Error: Unexpected end of expression"),
    Dict(params={"expr": "1+a"}, expected="Error: Undefined symbol a"),
    Dict(params={"expr": "1*a"}, expected="Error: Undefined symbol a")
], ids=lambda x: str(x.params.expr))
@allure.description('Check invalid chars')
@allure.title('invalid chars')
def test_invalid_char(scenario):
    params = {'expr': scenario.params.expr}
    value = calculate_req(params)
    assert_that(value, contains_string(scenario.expected), 'Expected Error due to illegal char')


@pytest.mark.parametrize('scenario', [
    Dict(params={"expr": "0.5*0.5"}, expected="0.25"),
    Dict(params={"expr": "5*2"}, expected="10"),
    Dict(params={"expr": "1000000000000*1000000000000"}, expected="-1e+24")
], ids=lambda x: str(x.params.expr))
@allure.description('Check Multiplication operator')
@allure.title('Multiplication operator')
def test_mult(scenario):
    params = {'expr': scenario.params.expr}
    value = calculate_req(params)
    assert_that(value, equal_to(scenario.expected), 'Compare result to expected value')


@pytest.mark.parametrize('scenario', [
    Dict(params={"expr": "1/2"}, expected="0.5"),
    Dict(params={"expr": "-5/-5"}, expected="1"),
    Dict(params={"expr": "1000000000000/1"}, expected="1e+12")
], ids=lambda x: str(x.params.expr))
@allure.description('Check Divide operator')
@allure.title('Divide operator')
def test_div(scenario):
    params = {'expr': scenario.params.expr}
    value = calculate_req(params)
    assert_that(value, equal_to(scenario.expected), 'Compare result to expected value')


@pytest.mark.parametrize('scenario', [
    Dict(params={"expr": "1/0"}, expected="Infinity")
], ids=lambda x: str(x.params.expr))
@allure.description('Check divide by zero')
@allure.title('Divide by zero')
def test_div_zero(scenario):
    params = {'expr': scenario.params.expr}
    value = calculate_req(params)
    assert_that(value, equal_to(scenario.expected), 'Divide by 0')


@pytest.mark.parametrize('scenario', [
    Dict(params={"expr": "2^0"}, expected="1"),
    Dict(params={"expr": "-5^2"}, expected="-25"),
    Dict(params={"expr": "5^-2"}, expected="0.04")
], ids=lambda x: str(x.params.expr))
@allure.description('Square root')
@allure.title('Square root')
def test_square_root(scenario):
    params = {'expr': scenario.params.expr}
    value = calculate_req(params)
    assert_that(value, equal_to(scenario.expected), 'Compare result to expected value')
