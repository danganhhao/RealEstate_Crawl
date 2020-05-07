from bs4 import BeautifulSoup
import requests
import lxml
import pandas as pd

total_page = 1
BASE_URL = 'https://batdongsan.com.vn/nha-dat-ban'

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
                product_detail = detail_soup.find(
                    'div', class_='body-left').find(
                    'div', class_='container-default').find(
                    'div', {"id": "product-detail"}
                )
                title = product_detail.find('div', class_='pm-title').h1.text
                print(title)


#
# def export_table_and_print(data):
#     table = pd.DataFrame(data, columns=[
#         'Image', 'Name', 'URL', 'Artist', 'Binding', 'Format', 'Release Date', 'Label'])
#     table.index = table.index + 1
#     clean_band_name = band_name.lower().replace(' ', '_')
#     table.to_csv(f'{clean_band_name}_albums.csv',
#                  sep=',', encoding='utf-8', index=False)
#     print('Scraping done. Here are the results:')
#     print(table)
#
#
# def get_cd_attributes(cd):
#     # Getting the CD attributes
#     image = cd.find('img', class_='ProductImage')['src']
#     name = cd.find('h2').find('a').text
#     url = cd.find('h2').find('a')['href']
#     url = base_url + url
#     artist = cd.find('li', class_="Artist")
#     artist = artist.find('a').text if artist else ''
#     binding = cd.find('li', class_="Binding")
#     binding = binding.text.replace('Binding: ', '') if binding else ''
#     format_album = cd.find('li', class_="Format")
#     format_album = format_album.text.replace('Format: ', '') if format_album else ''
#     release_date = cd.find('li', class_="ReleaseDate")
#     release_date = release_date.text.replace('Released: ', '') if release_date else ''
#     label = cd.find('li', class_="Label")
#     label = label.find('a').text if label else ''
#     # Store the values into the 'data' object
#     data['Image'].append(image)
#     data['Name'].append(name)
#     data['URL'].append(url)
#     data['Artist'].append(artist)
#     data['Binding'].append(binding)
#     data['Format'].append(format_album)
#     data['Release Date'].append(release_date)
#     data['Label'].append(label)
#
#
# # HTTP GET requests
# page = requests.get(search_url)
# # Checking if we successfully fetched the URL
# if page.status_code == requests.codes.ok:
#     bs = BeautifulSoup(page.text, 'lxml')
#     # Fetching all items
#     list_all_cd = bs.findAll('li', class_='ResultItem')
#     data = {
#         'Image': [],
#         'Name': [],
#         'URL': [],
#         'Artist': [],
#         'Binding': [],
#         'Format': [],
#         'Release Date': [],
#         'Label': [],
#     }
#
#     for cd in list_all_cd:
#         get_cd_attributes(cd)
# export_table_and_print(data)
