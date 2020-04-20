#!/usr/bin/env python
# coding: utf-8

import requests
URL = 'https://suumo.jp/jj/chintai/ichiran/FR301FC005/?shkr1=03&shkr3=03&cb=0.0&rn=3225&shkr2=03&mt=9999999&sngz=&ar=050&bs=040&shkr4=03&ct=9999999&ra=023&cn=9999999&ek=322553990&mb=0&et=9999999'
page = requests.get(URL)

from bs4 import BeautifulSoup
soup = BeautifulSoup(page.content, 'html.parser')

# properti = one unit
properties = soup.find_all('div', class_='property property--highlight js-property js-cassetLink')


for properti in properties:
    properties_details = soup.find_all('div', class_='detailbox')
    
for properti_details in properties_details:
    buildings_names = soup.find_all('a', class_='js-cassetLinkHref')
    rents = soup.find_all('div', class_='detailbox-property-point')
    other_fees = soup.find_all('td', class_='detailbox-property-col detailbox-property--col2')
    #notreadyyet #unit_descriptions = soup.find_all('td', class_='detailbox-property-col detailbox-property--col3')
    #notreadyyet #address = soup.find_all('td', class_='detailbox-property-col')
    #notreadyyet #distance_from_NU_station = soup.find_all('div', attrs={'style':'font-weight:bold'}) 


b_name_list = [] #cleaned
for building_name in buildings_names:
    b_name = building_name.string
    b_name_list.append(b_name)

rent_list = [] #cleaned
for rent in rents:
    r = rent.string
    rent_list.append(r)


deposit_n_reikin = []
for other_fee in other_fees:
    d_r_html = other_fee.find_all(attrs = {'class':None})
    for drhtml in d_r_html:
        dr = drhtml.text
        deposit_n_reikin.append(dr)

deposit = deposit_n_reikin[::2]
reikin = deposit_n_reikin[1::2]

deposit = [s.replace('敷', '') for s in deposit] #cleaned
reikin = [s.replace('礼', '') for s in reikin] #cleaned


hoshokin_n_shikibiki = []
for other_fee in other_fees:
    h_s_html = other_fee.find_all('div', class_='detailbox-property-inactive')
    for hshtml in h_s_html:
        hs = hshtml.text
        hoshokin_n_shikibiki.append(hs)

hoshokin = hoshokin_n_shikibiki[::2]
shikibiki = hoshokin_n_shikibiki[1::2]

shikibiki = [s.replace('敷引・償却\xa0', '') for s in shikibiki] #cleaned
hoshokin = [s.replace('保証金\xa0', '') for s in hoshokin] #cleaned


mapped = zip(b_name_list, rent_list, deposit, reikin, shikibiki, hoshokin)
mapped = list(mapped)


import pandas as pd


df = pd.DataFrame(mapped, columns = ['Building Name' , 'Rent', 'Deposit', 'Reikin', 'Shikibiki', 'Hoshokin'])

#change file location to safe the to-be-exported excel file
df.to_csv(r'D:\Nagoya Uni\Y3 S2\3(F4) Doi Seminar\export_dataframe.csv', encoding='utf-8-sig', index = False, header=True)



