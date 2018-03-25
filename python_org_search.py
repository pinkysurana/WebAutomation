from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox()
# driver = new RemoteWebDriver("http://localhost:9515", DesiredCapabilities.chrome());

driver.get("http://www.python.org")
assert "Python" in driver.title
elem = driver.find_element_by_name("q")
elem.clear()
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
assert "No results found." in driver.page_source
driver.close()