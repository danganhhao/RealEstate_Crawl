import json
import requests
import pandas as pd
from bs4 import BeautifulSoup
from src.define import *
from src.convert_data_helper import *

total_page = 1
BASE_URL = 'https://batdongsan.com.vn/nha-dat-ban'
data = {
    'title': [],  # require
    'estateType': [],  # require
    'expireAfter': [],  # require
    'project': [],
    'province': [],  # require
    'district': [],  # require
    'ward': [],
    'street': [],
    'numberOfRoom': [],
    'description': [],  # require
    'image': [],
    'detail': [],
    'price': [],
    'area': [],
    'contact': [],
    'transaction': [],  # require
    'addressDetail': [],
    'lat': [],
    'lng': [],
}

with open('location.json') as f:
    location = json.load(f)


def convertProvince(m_province):
    for m_location in location:
        if m_province == m_location['name']:
            return m_location['id']
        if m_province == u'Hà Nội':
            m_province = u'Hà Nội'
        if m_province == m_location['name']:
            return m_location['id']


def convertDistrict(m_province, m_district):
    for m_location in location:
        if m_province == m_location['name']:
            for m_d in m_location['districts']:
                if m_district == m_d['name']:
                    return m_d['id']
        if m_province == u'Hà Nội':
            m_province = u'Hà Nội'
        if m_province == m_location['name']:
            for m_d in m_location['districts']:
                if m_district == m_d['name']:
                    return m_d['id']


def export_table_and_print(m_data):
    table = pd.DataFrame(m_data, columns=[
        'title', 'estateType', 'expireAfter', 'project', 'province', 'district', 'ward', 'street',
        'numberOfRoom', 'description', 'image', 'detail', 'price', 'area', 'contact', 'transaction',
        'addressDetail', 'lat', 'lng'])
    table.index = table.index + 1
    table.to_csv('realestate_data.csv',
                 sep=',', encoding='utf-8', index=False)
    print('Scraping done. Here are the results:')
    print(table)


sources = requests.get(BASE_URL)
if sources.status_code == requests.codes.ok:
    soup = BeautifulSoup(sources.text, 'lxml')
    title_page = soup.find(
        'div', class_='site-center').find(
        'div', class_='body-left').find(
        'div', class_='container-default').find(
        'div', class_='Title')
    total = title_page.span.text.replace(',', '')
    total_page = int(int(total) / 20)

### TEST TEST ###
total_page = 2

for i in range(1, total_page):
    URL = f'https://batdongsan.com.vn/nha-dat-ban/p{i}'

    # HTTP GET requests
    sources = requests.get(URL)

    # Checking if we successfully fetched the URL
    if sources.status_code == requests.codes.ok:
        soup = BeautifulSoup(sources.text, 'lxml')
        body = soup.find(
            'div', class_='site-center').find(
            'div', class_='body-left').find(
            'div', class_='container-default').find(
            'div', class_='Main')

        list_item = body.findAll('div', class_='vip0 search-productItem')
        for item in list_item:
            href_url = item.find('a', href=True)['href']
            child_url = BASE_URL + href_url

            # ----- Get detail item------
            detail_sources = requests.get(child_url)
            if detail_sources.status_code == requests.codes.ok:
                detail_soup = BeautifulSoup(detail_sources.text, 'lxml')
                # ----------------------
                title = ''
                estateType = ''
                estateAfter = ''
                project = ''
                province = ''
                district = ''
                ward = ''
                street = ''
                numberOfRoom = ''
                description = ''
                image = ''
                detail = ''
                price = ''
                area = ''
                contact = ''
                transaction = ''
                addressDetail = ''
                lat = ''
                lng = ''

                # ----------------------
                product_detail = detail_soup.find(
                    'div', class_='body-left').find(
                    'div', class_='container-default').find(
                    'div', {"id": "product-detail"}
                )

                priceAndArea = product_detail.find('div', class_='kqchitiet')

                product_detail_content = product_detail.find(
                    'div', class_='div-table').find(
                    'div', class_='table-detail'
                )
                list_item_content = product_detail_content.findAll('div', class_='row')
                for item_content in list_item_content:
                    key = item_content.find('div', class_='left').text
                    value = item_content.find('div', class_='right').text
                    if key == ESTATE_TYPE:
                        estateType = convertEstateType(value)
                    if key == NUMBER_OF_ROOM:
                        value = value.split('\r\n')
                        numberOfRoom = value[1]
                    if key == ADDRESS:
                        address = value
                        address = address.replace('\r\n', '')
                        address = address.split(', ')
                        province_t = address[len(address) - 1]
                        province = convertProvince(province_t)
                        district_t = address[len(address) - 2]
                        district = convertDistrict(province_t, district_t)

                title = product_detail.find('div', class_='pm-title').h1.text
                area = priceAndArea.find_all(lambda tag: tag.name == 'span' and tag.get('class') == ['gia-title'])[0]. \
                    find('strong').text
                area = convertArea(area)
                price = priceAndArea.find('span', class_='gia-title mar-right-15').find('strong').text
                price = convertPrice(price, area)

                description = product_detail.find('div', class_='pm-desc').text
                image = product_detail.find(
                    'div', class_='pm-middle-content').find(
                    'div', class_='img-map').find(
                    'div', class_='photo').find(
                    'div', class_='show-img').find('img', src=True)['src']

                data['title'].append(title)
                data['estateType'].append(estateType)
                data['expireAfter'].append('365')
                data['project'].append('')
                data['province'].append(province)
                data['district'].append(district)
                data['ward'].append('')
                data['street'].append('')
                data['numberOfRoom'].append(numberOfRoom)
                data['description'].append(description)
                data['image'].append(image)
                data['detail'].append('')
                data['price'].append(price)
                data['area'].append(area)
                data['contact'].append('')
                data['transaction'].append('6')
                data['addressDetail'].append('')
                data['lat'].append('')
                data['lng'].append('')

                print('%s - %s' % ('Done', title))

export_table_and_print(data)
