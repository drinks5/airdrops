from selenium import webdriver
from common.pubilc import create_proxyauth_extension

proxyauth_plugin_path = create_proxyauth_extension(
    proxy_host="http-cla.abuyun.com",
    proxy_port=9030,
    proxy_username="HN3NLQ62E1ZH1P7C",
    proxy_password="5E4DFF016E27932C"
)


co = webdriver.ChromeOptions()
# co.add_argument("--start-maximized")
co.add_extension(proxyauth_plugin_path)


driver = webdriver.Chrome(executable_path="C:\chromedriver.exe", chrome_options=co)
driver.get("http://ip138.com/")
print(driver.page_source)
