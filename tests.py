import requests
import pytest
from hamcrest import *
NUMBER_1 = "1"


@pytest.mark.parametrize("a,b,expected", [
    ("1", "2", "3"),
    ("1.2", "3.3", "4.5"),
    ("1000000000000", "1000000000000", "2e+12"),
    ("-5", "-6", "-11")
])
def test_add(a, b, expected):
    req = requests.get('http://api.mathjs.org/v4/?expr=' + a + '%2B' + b)
    value = req.text
    print(value)
    assert value == expected


@pytest.mark.parametrize("a,b,expected", [
    ("1", "a", "Error: Undefined symbol"),
    ("1", "#", "Unexpected end of expression")
])
def test_sub_invalid_char(a, b, expected):
    req = requests.get('http://api.mathjs.org/v4/?expr=' + a + '%2B' + b)
    value = req.text
    assert_that(value, contains_string(expected), 'Unexpected Error due to illegal char')



@pytest.mark.parametrize("a,b,expected", [
    ("1", "2", "-1"),
    ("2", "1", "1"),
    ("-5", "-5", "0"),
    ("2", "0", "2")
])
def test_sub(a, b, expected):
    req = requests.get('http://api.mathjs.org/v4/?expr=' + a + '-' + b)
    value = req.text
    print(value)
    assert value == expected

@pytest.mark.parametrize("a,b,expected", [
    ("1", "a", "Error: Undefined symbol"),
    ("1", "#", "Unexpected end of expression")
])
def test_sub_invalid_char(a, b, expected):
    req = requests.get('http://api.mathjs.org/v4/?expr=' + a + '-' + b)
    value = req.text
    assert_that(value, contains_string(expected), 'Unexpected Error due to illegal char')


@pytest.mark.parametrize("a,b,expected", [
    ("1", "2", "2"),
    ("0.5", "0.5", "0.25"),
    ("5", "0", "0"),
    ("-5", "-2", "10"),
    ("5", "2", "10"),
    ("5", "A", "5 A"),
    ("1000000000000", "1000000000000", "1e+24")
])
def test_multiple(a, b, expected):
    req = requests.get('http://api.mathjs.org/v4/?expr=' + a + '*' + b)
    value = req.text
    print(value)
    assert value == expected


@pytest.mark.parametrize("a,b,expected", [
    ("1", "a", "Error: Undefined symbol"),
    ("1", "#", "Unexpected end of expression")
])
def test_multiple_invalid_char(a, b, expected):
    req = requests.get('http://api.mathjs.org/v4/?expr=' + a + '*' + b)
    value = req.text
    assert_that(value, contains_string(expected), 'Unexpected Error due to illegal char')


@pytest.mark.parametrize("a,b,expected", [
    ("1", "2", "0.5"),
    ("-5", "-5", "1"),
    ("0", "5", "0"),
    ("1000000000000", "1", "1e+12")
])
def test_div(a, b, expected):
    req = requests.get('http://api.mathjs.org/v4/?expr=' + a + '/' + b)
    value = req.text
    print(value)
    assert value == expected


def test_div_divide_zero():
    req = requests.get('http://api.mathjs.org/v4/?expr=' + NUMBER_1 + '/' + '0')
    value = req.text
    assert_that(value, contains_string("Infinity"), 'Divide by 0')


@pytest.mark.parametrize("a,b,expected", [
    ("1", "a", "Error: Undefined symbol"),
    ("1", "#", "Unexpected end of expression")
])
def test_multiple_invalid_char(a, b, expected):
    req = requests.get('http://api.mathjs.org/v4/?expr=' + a + '/' + b)
    value = req.text
    assert_that(value, contains_string(expected), 'Unexpected Error due to illegal char')


@pytest.mark.parametrize("a,b,expected", [
    ("1", "2", "1"),
    ("2", "0", "1"),
    ("-5", "2", "-25"),
    ("5", "-2", "0.04"),
])
def test_square_root(a, b, expected):
    req = requests.get('http://api.mathjs.org/v4/?expr=' + a + '^' + b)
    value = req.text
    print(value)
    assert value == expected


@pytest.mark.parametrize("a,b,expected", [
    ("1", "a", "Error: Undefined symbol"),
    ("1", "#", "Unexpected end of expression")
])
def test_square_invalid_char(a, b, expected):
    req = requests.get('http://api.mathjs.org/v4/?expr=' + a + '*' + b)
    value = req.text
    assert_that(value, contains_string(expected), 'Unexpected Error due to illegal char')