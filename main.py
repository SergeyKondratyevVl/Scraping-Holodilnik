import json
import os
import time
import requests
from info import regional_urls
from selenium import webdriver
from selenium.webdriver.common.by import By

def get_categories(id, city):

    url = f'https://www.holodilnik.ru/i/cache/catsmenu/categories_repair_{id}.json'

    response = requests.get(url=url).json()

    if not os.path.exists('data'):
        os.mkdir('data')
    
    if not os.path.exists(f'data/{city}'):
        os.mkdir(f'data/{city}')
    
    category_list = []
    for category in response:
        
        category_id = category['id']
        category_tag = category['tag']
        category_title = category['title']
        subcategories = category['categories']
        category_list.append(category_title)
        # for k, subcategory in enumerate(subcategories):
        #     subcategory_id = subcategory['id']
        #     subcategory_url = 'https:' + subcategory['href']
        #     subcategory_title = subcategory['title']
        
        with open(f'data/{city}/{category_title}.json', 'w', encoding='utf-8') as file:
            json.dump(category, file, indent=4, ensure_ascii=False)
        
    return category_list

def get_city_categories_urls():
    listCityCategories = {}
    for k in regional_urls:
        try:
            listCityCategories[regional_urls[k]] = get_categories(k, regional_urls[k])
        except Exception as ex:
            print(regional_urls[k])
    
    with open('listCityCategories.json', 'w', encoding='utf-8') as file:
        json.dump(listCityCategories, file, indent=4, ensure_ascii=False)

def get_source_html(city='', category_name=''):

    driver = webdriver.Chrome(
        executable_path='chromedriver.exe'
    )

    # city = 'adler'
    # category_name = 'Аудио-видео'

    path_category = f'data/{city}/{category_name}'

    with open(f'data/{city}/{category_name}.json', 'r', encoding='utf-8') as file:
        categories = json.load(file)

    try:
        category_items = {}
        for category in categories['categories']:

            url = 'https:' + category['href']
            title_name = category['title']

            driver.get(url=url)
            time.sleep(1)
            find_more_element = driver.find_elements(by=By.CLASS_NAME, value='product-specification')
            if not find_more_element:
                continue
            else:

                if not os.path.exists(path_category):
                    os.mkdir(path_category)

                category_items[f'{city}_{title_name}'] = []

                for element in find_more_element:
                    name = element.find_element(by=By.CLASS_NAME, value='product-name').text
                    url = element.find_element(by=By.CLASS_NAME, value='product-name').get_attribute('href')
                    old_price = element.find_element(by=By.CLASS_NAME, value='old-price').text.replace(' ', '')[:-1]
                    price = element.find_element(by=By.CLASS_NAME, value='price').text.replace(' ', '')[:-1]
                    category_items[f'{city}_{title_name}'].append({
                        'name': name,
                        'url': url,
                        'old_price': old_price,
                        'price': price,
                    })

        if category_items:
            with open(f'{path_category}/{category_name}.json', 'w', encoding="utf-8") as file:
                json.dump(obj=category_items, fp=file, indent=4, ensure_ascii=False)
            

    except Exception as ex:
        print(ex)

    driver.close()
    driver.quit()

def get_html_city_categories():

    with open('listCityCategories.json', 'r', encoding='utf-8') as file:
        items = json.load(file)
        
    for city in ['adler',]:
        categories = items[city]
        for category_name in categories:
            print(f'City: {city}, Category: {category_name}')
            get_source_html(city=city, category_name=category_name)

def main():
    # get_city_categories_urls()
    get_html_city_categories()

if __name__ == '__main__':
    main()





""""
Эти города не спарсились:

voronezh
kazan
nnovgorod
rostovnd
tyumen
ufa
cheboksary

"""