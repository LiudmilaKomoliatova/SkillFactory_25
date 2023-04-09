import pytest
from selenium import webdriver


@pytest.fixture
def firefox_options(firefox_options):
	firefox_options.add_argument('-foreground')
	firefox_options.add_argument('--headless')
	firefox_options.set_preference('browser.anchor_color', '#FF0000')
	return firefox_options


@pytest.fixture
def chrome_options(chrome_options):
	chrome_options.add_argument("--headless")
	chrome_options.add_argument('--kiosk')
	chrome_options.add_argument("--window-size=1920,1080")
	chrome_options.add_argument("--disable-gpu")
	chrome_options.add_argument("--disable-extensions")
	chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
	chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36')
	return chrome_options


@pytest.fixture(params=["chrome", "firefox"], scope="function")  # , "chrome", "firefox", "edge"
def driver(request, chrome_options, firefox_options):
	if request.param == "chrome":
		web_driver = webdriver.Chrome(options=chrome_options)
	if request.param == "firefox":
		web_driver = webdriver.Firefox(options=firefox_options)
	if request.param == "edge":
		web_driver = webdriver.Edge()
	web_driver.maximize_window()
	yield web_driver
	web_driver.close()
