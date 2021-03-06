import time, pymysql.cursors
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# at the beginning:
start_time = time.time()
connection = pymysql.connect(user='root', password='abc123', host='127.0.0.1', db='trendy',
                             cursorclass=pymysql.cursors.DictCursor, use_unicode=True, charset="utf8mb4")
with connection.cursor() as cursor:
    cursor.execute("TRUNCATE TABLE facebook;")
connection.commit()

chromeOptions = Options()
chromeOptions.add_argument("--headless")
chromeOptions.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 2, 'geolocation': True})
driver = webdriver.Chrome(chrome_options=chromeOptions)
wait = WebDriverWait(driver, 30)
driver.get("https://facebook.com/")

# Typing credentials and signing in
wait.until(EC.visibility_of_element_located((By.ID, 'email')))
driver.find_element_by_id('email').send_keys('')
wait.until(EC.visibility_of_element_located((By.ID, 'pass')))
driver.find_element_by_id('pass').send_keys('')
wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@type="submit"]')))
driver.find_element_by_xpath('//input[@type="submit"]').click()

# Dialog box alert handler
try:
    notNowNotifcation = driver.find_element_by_xpath('//a[@action="cancel"]')
    if not notNowNotifcation is None:
        notNowNotifcation.click()
except:
    print("Couldn't click the SeeMore button!")

# Clicks on the seemore buton
wait.until(EC.visibility_of_element_located((By.XPATH, '//a[@data-position="seemore"]')))
driver.find_element_by_xpath('//a[@data-position="seemore"]').click()
time.sleep(3)

# Retrieval Process
wait.until(EC.presence_of_all_elements_located((By.XPATH, '//a[starts-with(@data-hovercard, "/pubcontent/trending/hovercard/?topic_id=")]')))
retrieved = driver.find_elements_by_xpath('//a[starts-with(@data-hovercard, "/pubcontent/trending/hovercard/?topic_id=")]')
while not len(retrieved) == 10:
    retrieved = driver.find_elements_by_xpath('//a[starts-with(@data-hovercard, "/pubcontent/trending/hovercard/?topic_id=")]')

# Trends Parsing
headlines = []
texts = []
for heads in retrieved:
    headlines.append(str(heads.find_element_by_tag_name('div').text).split('\n')[0])
for text in retrieved:
    texts.append(text.find_element_by_tag_name('span').text)

# Trends Links retrieval and parsing
links = []
wait.until(EC.presence_of_all_elements_located((By.XPATH, '//a[starts-with(@href, "/topic")]')))
hrefs = driver.find_elements_by_xpath('//a[starts-with(@href, "/topic")]')
for href in hrefs:
    links.append(href.get_attribute('href'))

username = 'alibaba'
with connection.cursor() as cursor:
    for num in range(0, len(headlines)):
        print(headlines[num] + " : " + texts[num] + " : " + links[num])
        sql = "INSERT INTO trendy.facebook(id, username, trend, content, link, loadtime) VALUES (DEFAULT, %s, %s, %s, %s, NOW())"
        cursor.execute(sql, (username, headlines[num], texts[num], links[num]))
    connection.commit()

# At the end of the program:
driver.quit()
print("Retrieval time took %f seconds" % (time.time() - start_time))
