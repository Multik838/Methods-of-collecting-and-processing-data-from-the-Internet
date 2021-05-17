from bs4 import BeautifulSoup as bs
import requests
import re
import pandas as pd

def _parser_hh(vacancy):
    global last_page

    vacancy_date = []
    page = 0
    params = {
        'text': vacancy, \
        'search_field': 'name', \
        'items_on_page': '100', \
        'page': ''
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0'
    }

    link = 'https://hh.ru/search/vacancy'
       
    html = requests.get(link, params=params, headers=headers)
    
    if html.ok:
        parsed_html = bs(html.text,'html.parser')
        
        page_block = parsed_html.find('div', {'data-qa': 'pager-block'})
        if not page_block:
            last_page = '1'
        else:
            last_page = int(page_block.find_all('span', {'class': 'bloko-button bloko-button_pressed'})[-1].getText())
    
    for page in range(0, last_page):
        params['page'] = page
        html = requests.get(link, params=params, headers=headers)
        
        if html.ok:
            parsed_html = bs(html.text,'html.parser')
            
            vacancy_items = parsed_html.find('div', {'data-qa': 'vacancy-serp__results'}).find_all('div', {'class': 'vacancy-serp-item'})
                
            for item in vacancy_items:
                vacancy_date.append(_parser_item_hh(item))
                
    return vacancy_date

def _parser_item_hh(item):

    vacancy_date = {}
    
    # vacancy_name
    vacancy_name = item.find('span', {'class': 'resume-search-item__name'}).getText().replace(u'\xa0', u' ')

    
    vacancy_date['vacancy_name'] = vacancy_name
    
    # company_name
    company_name = item.find('div', {'class': 'vacancy-serp-item__meta-info'}).find('a').getText()
    
    vacancy_date['company_name'] = company_name
    
    # city
    city = item.find('span', {'class': 'vacancy-serp-item__meta-info'}).getText().split(', ')[0]
    
    vacancy_date['city'] = city
    
    #metro station
    metro_station = item.find('span', {'class': 'vacancy-serp-item__meta-info'}).findChild()

    if not metro_station:
        metro_station = None
    else:
        metro_station = metro_station.getText()
        
    vacancy_date['metro_station'] = metro_station
    
    #salary
    salary = item.find('div', {'class': 'vacancy-serp-item__compensation'})
    if not salary:
        salary_min = None
        salary_max = None
        salary_currency = None
    else:
        salary = salary.getText().replace(u'\xa0', u'')
        
        salary = re.split(r'\s|-', salary)
        
        if salary[0] == 'до':
            salary_min = None
            salary_max = int(salary[1])
        elif salary[0] == 'от':
            salary_min = int(salary[1])
            salary_max = None
        else:
            salary_min = int(salary[0])
            salary_max = int(salary[1])            
        
        salary_currency = salary[2]
        
    vacancy_date['salary_min'] = salary_min
    vacancy_date['salary_max'] = salary_max
    vacancy_date['salary_currency'] = salary_currency
    
#     # link
#     is_ad = item.find('div', {'data-qa': 'vacancy-serp__vacancy vacancy-serp__vacancy_standard'}).getText()
    
#     vacancy_link = item.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})['href']
    
#     if is_ad != 'Реклама':
#         vacancy_link = vacancy_link.split('?')[0]
    
#     vacancy_date['vacancy_link'] = vacancy_link 
    
     # site
    vacancy_date['site'] = 'hh.ru'
    
    return vacancy_date

# def superjob(main_link, search_str, n_str):
#     headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
#                          'Chrome/89.0.4389.105 YaBrowser/21.3.3.230 Yowser/2.5 Safari/537.36'}
#     #https://www.superjob.ru/vacancy/search/?keywords=fyfkbnbr&geo%5Bt%5D%5B0%5D=4
#     #n_str - кол-во просматриваемых страниц
#     search_str ={}
#     main_link = 'https://superjob.ru'
#     keywords = 'Аналитик'
#     params = {'keywords': keywords}
#     base_url=requests.get(main_link + '/vacancy/search/',params = params, headers=headers)
#     vacancy_date = []
#     session = requests.Session()
#     for i in range(n_str):
#         request = session.get(base_url)
#         if request.status_code == 200:
#             soup = bs(request.content, 'lxml')
#             divs = soup.find_all('div', {'class':'_3zucV _2GPIV f-test-vacancy-item i6-sc _3VcZr'})
#             for div in divs:
#                 title = div.find('div', {'class': '_3mfro CuJz5 PlM3e _2JVkc _3LJqf'}).text
#                 href = div.find('div', {'class': '_3mfro CuJz5 PlM3e _2JVkc _3LJqf'}).findParent()['href']
#                 salary = div.find('span', {'class': '_3mfro _2Wp8I f-test-text-company-item-salary PlM3e _2JVkc _2VHxz'}).text
#                 salary=salary.replace(u'\xa0', u'')
#                 if '—' in salary:
#                     salary_min = salary.split('—')[0]
#                     salary_min = re.sub(r'[^0-9]', '', salary_min)
#                     salary_max = salary.split('—')[1]
#                     salary_max = re.sub(r'[^0-9]', '', salary_max)
#                     salary_min = int(salary_min)
#                     salary_max = int(salary_max)
#                 elif 'от' in salary:
#                     salary_min = salary[2:]
#                     salary_min = re.sub(r'[^0-9]', '', salary_min)
#                     salary_min = int(salary_min)
#                     salary_max = None
#                 elif 'договорённости' in salary:
#                     salary_min = None
#                     salary_max = None
#                 elif 'до' in salary:
#                     salary_min = None
#                     salary_max = salary[2:]
#                     salary_max = re.sub(r'[^0-9]', '', salary_max)
#                     salary_max = int(salary_max)
#                 else:
#                     salary_min = int(re.sub(r'[^0-9]', '', salary))
#                     salary_max = int(re.sub(r'[^0-9]', '', salary))

#                 jobs.append({
#                     'title': title,
#                     'href': 'https://www.superjob.ru'+href,
#                     'salary_min': salary_min,
#                     'salary_max': salary_max,
#                     'link': main_link
#                 })
#             base_url = main_link + \
#                        soup.find('a', {'class': 'icMQ_ _1_Cht _3ze9n f-test-button-dalshe f-test-link-dalshe'})['href']
#             time.sleep(random.randint(1,10))
#         else:
#             print('Ошибка')

#     return vacancy_date

def parser_vacancy(vacancy):
    vacancy_date = []
    vacancy_date.extend(_parser_hh(vacancy))
#    vacancy_date.extend(superjob(vacancy_date, search_str, n_str))
#    search_str='Python'
#    n_str=2
# def parser_vacancy(vacancy, search_str, n_str):

    df = pd.DataFrame(vacancy_date)

    return df

vacancy = 'Python'
# search_str='Python'
# n_str=2
# df = parser_vacancy(vacancy, search_str, n_str)
df = parser_vacancy(vacancy)

df

