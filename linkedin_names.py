from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as cond
from time import sleep
import json

#Credentials
config = {
    'EMAIL': 'your email',
    'PASSWORD': 'your password'
}
LOGIN_URL = 'https://www.linkedin.com/login?trk=guest_homepage-basic_nav-header-signin'
NAMES = []

def set_browser():
    option = webdriver.ChromeOptions()
    option.add_argument(' — incognito')
    # option.set_headless(True)
    browser = webdriver.Chrome(executable_path='/usr/bin/chromedriver', chrome_options=option)
    return browser

def log_in(page_url,browser):
    browser.get(page_url)
    username_field = browser.find_element_by_xpath('//*[@id="username"]')
    password_field = browser.find_element_by_xpath('//*[@id="password"]')
    sign_in_btn = browser.find_element_by_xpath('//*[@id="app__container"]/main/div/form/div[3]/button')
    username_field.send_keys(config['EMAIL'])
    password_field.send_keys(config['PASSWORD'])
    sign_in_btn.click()
    sleep(3)
    return

def paginate_connection(browser):
    print('I am here 1')
    sleep(1)
    lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    pagination = browser.find_element_by_class_name('artdeco-pagination')
    print('I am here 1.1')
    buttons = pagination.find_elements_by_class_name('artdeco-pagination__indicator--number')
    number = buttons[-1].find_element_by_tag_name('span').get_attribute('innerHTML')
    print('I am here 2')
    number =  int(number)
    for _ in range(number):
    # grab the data
        print('I am here 3')
        lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        match=False
        while(match==False):
                lastCount = lenOfPage
                sleep(3)
                lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
                if lastCount==lenOfPage:
                    match=True
        search_res = browser.find_element_by_class_name('search-results__list')
        actor_names = search_res.find_elements_by_class_name('actor-name')
        for actor_name in actor_names:
            NAMES.append(actor_name.get_attribute('innerHTML'))
        # click next link
    
        next_button = browser.find_element_by_class_name('artdeco-pagination__button--next')
        browser.execute_script("arguments[0].click();", next_button)
        sleep(5)
        

def crawl_connection(link,browser):
    browser.get(link)
    sleep(3)
    ul = browser.find_element_by_class_name('pv-top-card-v3--list-bullet')
    li_items = ul.find_elements_by_tag_name('li')
    print(li_items)
    see_conn = li_items[1]
    print(see_conn.get_attribute('innerHTML'))
    try:
        see_conn.click()
        print('No exceptiom')
        sleep(5)
        paginate_connection(browser)
        return
    except Exception as e:
        print('Exception caught in Crawl_connection')
        print(e)
        return


def main():        
    browser = set_browser()
    log_in(LOGIN_URL,browser)

    try:
        WebDriverWait(browser,10).until(
            lambda browser: browser.current_url == 'https://www.linkedin.com/feed/?trk=guest_homepage-basic_nav-header-signin')
    except TimeoutException as e:
        print('Could not log in')
        print(e)



    aside = browser.find_element_by_tag_name('aside')
    your_name = aside.find_element_by_class_name('t-16').get_attribute('innerHTML')
#    print(your_name)
    browser.find_element_by_xpath('//*[@id="mynetwork-tab-icon"]').click()


    try:
        WebDriverWait(browser,10).until(
            lambda browser:browser.current_url == 'https://www.linkedin.com/mynetwork/')
    except TimeoutException as e:
        print('mynetwork not coming up')
        print(e)


    sleep(5)

    element = browser.find_element_by_class_name('mn-community-summary__section')
    element.find_element_by_class_name('t-14').click()


    sleep(5)


    lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match=False
    while(match==False):
            lastCount = lenOfPage
            sleep(3)
            lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            if lastCount==lenOfPage:
                match=True


    section = browser.find_element_by_class_name('mn-connections')
    connection_cards = section.find_elements_by_class_name('mn-connection-card__details')

    links = []
    for card in connection_cards:
        link = card.find_element_by_tag_name('a').get_attribute('href')
        name = card.find_element_by_class_name('mn-connection-card__name').get_attribute('innerHTML')
        name = name.strip()
        NAMES.append(name)
        links.append(link)
    print("Before Crawl_connection")

    for link in links:
        crawl_connection(link,browser)
    
    with open('data.json', 'w') as outfile:
        json.dump(NAMES, outfile)

if __name__ == "__main__":
    main()