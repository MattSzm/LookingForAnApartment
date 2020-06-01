import sys
import requests
import re
import json
from bs4 import BeautifulSoup

"""#input variables
city = 'warszawa'
district = 'śródmieście'
minPrice = 1000
maxPrice = 3000"""

#script variables-buffer
searchAmount = 30

def InputProcessingName(input):
    return input.title()

def InputProcessingPrice(input):
    if input == "none" or input == 'None':
        return None
    return int(input)

def PriceComparison(value, lowConstraint, highConstraint):
    if not lowConstraint and not highConstraint:
        return True
    elif not lowConstraint and value <= highConstraint:
        return True
    elif not highConstraint and value >= lowConstraint:
        return True
    elif value >= lowConstraint and value <= highConstraint:
        return True
    else:
        return False

headers = {
    'authority': 'www.otodom.pl',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': 'laquesisff=gre-12226; lqstatus=1589791830; optimizelyEndUserId=oeu1589790625016r0.5368696980136993; _ga=GA1.2.993291220.1589790626; _gcl_au=1.1.2041847785.1589790626; __gads=ID=16c80757a26ad124:T=1589790632:S=ALNI_MYo6C4iDc9Ya3x3IDSkM8mWGERPkQ; __gfp_64b=mehwV_Dt.l5LpN2PSTZCNxqmGi6QNCtR29Tl8nizLoP.l7; laquesis=; newrelic_cdn_name=CF; PHPSESSID=oor6ckdh227rn6ip43huoeucdc; mobile_default=desktop; ninja_user_status=unlogged; observed5_id_clipboard=5ed516fb27bb3; observed5_sec_clipboard=5b3eT7yv2fuH%2BuMAcExphpf6lAS6a5Z5; b4da1ddd423e4e8c32114620d61bbfb1=87b1fc8446e122223180e30c3bb9acac; ldTd=true; _gid=GA1.2.604124014.1591023342; _gat_clientNinja=1; onap=e75850ed0ecx28e8a848-4-1727061914cx54ba70c6-3-1591025142; lqstatus=1591024542',
    'referer': 'https://www.google.com/',
}

city = sys.argv[1]
district = sys.argv[2]
minPrice = InputProcessingPrice(sys.argv[3])
maxPrice = InputProcessingPrice(sys.argv[4])

city = InputProcessingName(city)
district = InputProcessingName(district)

with open('scriptFlats.json', 'w') as jsonFile:
    data = {'otodom': []}

    for count in range(1, searchAmount+1):
        #request-processing
        response = requests.get('https://www.otodom.pl/wynajem/?page={}'.format(count),
                                headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        for singleArticle in soup.find_all('article'):
            singleArticleText = singleArticle.prettify()
            if city in singleArticleText:

                #Rent-processing
                liPriceTag = singleArticle.find_all('li', class_='offer-item-price')[0]
                currentPrice = re.search('\s\s[[[0-9][0-9][0-9]', liPriceTag.get_text())
                if not currentPrice:
                    currentPrice = re.search('\s[0-9]\s[0-9][0-9][0-9]', liPriceTag.get_text())
                    if not currentPrice:
                        currentPrice = re.search('\s[0-9][0-9]\s[0-9][0-9][0-9]', liPriceTag.get_text())
                if currentPrice:
                    currentPriceINT = int(currentPrice.group(0).replace(' ',''))
                    if PriceComparison(currentPriceINT, minPrice, maxPrice):

                        #District-processing
                        DistrictTag = singleArticle.find_all('p', class_='text-nowrap')[0]
                        currentDistrict = re.search('(?<={},\s)\w+'.format(city), DistrictTag.get_text())
                        if not district or district == currentDistrict.group(0).strip():

                            aTag = (singleArticle.find('a'))
                            hrefOutput = aTag.get('href')
                            data['otodom'].append({currentPriceINT: hrefOutput})
                            print(hrefOutput)

    json.dump(data, jsonFile, indent=2)

#print(soup.prettify())

