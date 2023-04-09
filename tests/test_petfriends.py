from settings import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


def test_search_example(driver, time_limit=timeout_limit):
	driver.implicitly_wait(time_limit)
	wait = WebDriverWait(driver, time_limit)
	driver.get('https://petfriends.skillfactory.ru/')
	# wait and click on the new user button
	wait.until(lambda x: x.find_element(By.CLASS_NAME, "btn-success")).click()
	# wait and click on /login
	wait.until(lambda x: x.find_element(By.LINK_TEXT, u"У меня уже есть аккаунт")).click()

	# check and select button
	btn_submit = wait.until(ec.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
	# add email
	driver.find_element(By.ID, "email").send_keys(valid_email)
	# add password
	driver.find_element(By.ID, "pass").send_keys(valid_password)
	btn_submit.click()

	# wait and click my pet
	wait.until(lambda x: x.find_element(By.LINK_TEXT, u"Мои питомцы")).click()

	# wait and get rows count
	pet_rows = wait.until(lambda x: x.find_elements(By.XPATH, "//tbody/tr"))

	# get items
	my_pets_counter = int(
		driver.find_element(
			By.XPATH, '//div[@class=".col-sm-4 left"]').text.split("\n")[1].split(' ')[1])
	all_items = driver.find_elements(By.XPATH, "//tbody/tr/td")
	all_items_img = driver.find_elements(By.XPATH, "//tbody/tr/th/img")

	# 1 Присутствуют все питомцы
	assert my_pets_counter == len(pet_rows), f'Присутствуют не все питомцы {pet_rows}'

	# 2 Хотя бы у половины питомцев есть фото
	count_pets_with_img = 0
	for i in range(len(all_items_img)):
		if all_items_img[i].get_attribute('src') != '':
			count_pets_with_img += 1
	count_pets_with_img_percent = 100 * count_pets_with_img/my_pets_counter
	assert count_pets_with_img_percent > 50, 'Меньше половины питомцев без фото'

	set_pet = set()
	set_pet_names = set()
	# 3 У всех питомцев есть имя, возраст и порода.
	for i in range(0, len(all_items), 4):
		# name
		pet_name = all_items[i].text
		set_pet_names.add(pet_name)
		# type
		pet_type = all_items[i+1].text
		# age
		pet_age = all_items[i+2].text
		set_pet.add(pet_name+pet_type+pet_age)
		assert pet_name != '', 'Не у всех питомцев есть имя'
		assert pet_type != '', 'Не у всех питомцев есть возраст'
		assert pet_age != '', 'Не у всех питомцев есть порода'

	# 4 У всех питомцев разные имена.
	assert len(set_pet_names) == my_pets_counter, 'Не у всех питомцев разные имена'

	# 5 В списке нет повторяющихся питомцев.
	assert len(set_pet) == my_pets_counter, 'В списке повторяющиеся питомцы'

	# collect all pets data
	# _ = WebDriverWait(driver, time_limit).until(ec.visibility_of_all_elements_located((By.CLASS_NAME, "card")))
	# _ = WebDriverWait(driver, time_limit).until(ec.visibility_of_all_elements_located((By.CLASS_NAME, "card")))
	# pets_images = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
	# pets_names = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
	# pets_descriptions = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')