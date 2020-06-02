import sys
import requests
import re
import json
from bs4 import BeautifulSoup

#script variables-buffer
searchAmount = 20

def InputProcessingName(input):
    return input.title()

def InputProcessingDis(input):
    if input == "none" or input == 'None' or input == 'NONE':
        return None
    return input

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
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/83.0.4103.61 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': 'laquesisff=gre-12226; lqstatus=1589791830; optimizelyEndUserId=oeu1589790625016r0.5368696980136993; _'
              'ga=GA1.2.993291220.1589790626; _gcl_au=1.1.2041847785.1589790626; __'
              'gads=ID=16c80757a26ad124:T=1589790632:S=ALNI_'
              'MYo6C4iDc9Ya3x3IDSkM8mWGERPkQ; __gfp_64b=mehwV_Dt.l5LpN2PSTZCNxqmGi6QNCtR29Tl8nizLoP.l7; '
              'laquesis=; newrelic_cdn_name=CF; '
              'PHPSESSID=oor6ckdh227rn6ip43huoeucdc; mobile_default=desktop; ninja_user_status=unlogged; '
              'observed5_id_clipboard=5ed516fb27bb3; '
              'observed5_sec_clipboard=5b3eT7yv2fuH%2BuMAcExphpf6lAS6a5Z5; '
              'b4da1ddd423e4e8c32114620d61bbfb1=87b1fc8446e122223180e30c3bb9acac; '
              'ldTd=true; _gid=GA1.2.604124014.1591023342; _gat_clientNinja=1;'
              ' onap=e75850ed0ecx28e8a848-4-1727061914cx54ba70c6-3-1591025142; '
              'lqstatus=1591024542',
    'referer': 'https://www.google.com/',
}

headers2 = {
    'authority': 'www.olx.pl',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,'
              '*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'referer': 'https://www.google.com/',
    'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': 'newrelicInited=0; dfp_segment_test_v3=31; dfp_segment_test=69; dfp_segment_test_'
              'v4=29; dfp_segment_test_oa=35; lister_lifecycle=1568205780; dfp_user_'
              'id=08414dde-da9f-d501-4fce-23b06aa2fd01-ver2; used_adblock=adblock_disabled; _'
              '_gfp_64b=KNHaHU0PL33iIPZgn_sK_x_.potRym4ynDqzUZbKnDL.J7; _'
              'ga=GA1.2.2040892305.1568205790; optimizelyEndUserId=oeu1568205791571r0.4045493597424197; '
              'G_ENABLED_IDPS=google; __gads=ID=a7077e84a2fa8d3e:T=1568205790:S=ALNI_MZ0dn0REFHK3_xMSZjRyN2O-GjQuA; '
              '_hjid=9fe57968-7f8e-42b2-9265-80b7164c49da; '
              '_abck=0B2A18020292D5C8E88D3F866D07B212~0~YAAQF9cSAi0kKxdtAQAAewVaIALWFsMXersA7bQysSYcB+'
              'SsvEYZQGKbwXyFYDkPnxfIS2h3kRCDv65YB1YjYwcuGWc9BQB2UEyUag9jDuuQjpOcejiTSlJoIcCk2radNHH+sopbEamr'
              'lwXhyg3nZsp48DdX0I/WGCIMeWzODP6b5oabvfsehjDhcglRPBhAVjlMq/Bz35bO72ucDStjCXroPYv2MOufjgvHpMYFHwbCQ'
              'mUYECNSuOhj6KHgZ+5xMdcZ5BWheixZVHM6QfgrDfYa97u7b031hrJxi5JKLw+Kk2ZAHg==~-1~-1~-1; random_segment_'
              'js=56; laquesisff=a2b-000#olxeu-0000#olxeu-29763; __diug=true; user_adblock_status=false; '
              '_gcl_au=1.1.2034920408.1586541205; last_locations=19701-0-0-Wroc%C5%82aw-Dolno%C5%9Bl%C4%85skie-wroclaw_'
              '8959-0-0-Krak%C3%B3w-Ma%C5%82opolskie-krakow; olxRebrandedWelcomeClosed=1;'
              ' cookieBarSeen=true; consentBarSeen=true; didomi_token=eyJ1c2VyX2lkIjoiMTcyNTUxMmEtZTk1Zi02ZTY5'
              'LTgxZjAtYmE2M2FhYWU2ZTUyIiwiY3JlYXRlZCI6IjIwMjAtMDUtMjdUMDc6Mzk6NDcuNjY0WiIsInVwZGF0ZWQiOiIyMDIw'
              'LTA1LTI3VDA3OjM5OjUzLjU2NVoiLCJ2ZW5kb3JzIjp7ImVuYWJsZWQiOlsiZ29vZ2xlIl0sImRpc2FibGVkIjpbXX0sInB1cn'
              'Bvc2VzIjp7ImVuYWJsZWQiOlsiY29va2llcyIsImFkdmVydGlzaW5nX3BlcnNvbmFsaXphdGlvbiIsImFkX2RlbGl2ZXJ5IiwiY2'
              '9udGVudF9wZXJzb25hbGl6YXRpb24iLCJhbmFseXRpY3MiXSwiZGlzYWJsZWQiOltdfX0=; '
              'euconsent=BO0DPykO0DPzfAHABBPLDG-AAAAvRrv7__7-_9_-_f__9uj3Or_v_f__32ccL59v_h_7v-_7fi_-1jV4u_'
              '1vft9yfk1-5ctDztp507iakivXmqdeb1v_nz3_9phP78k89r7337Ew-OkAAAAAAAAAAAAAAAAA; cmpvendors=4; '
              'cmpreset=true; laquesis=disco-1036@a#disco-773@b#olxeu-29551@b#olxeu-29990@c#olxeu-30294@a#olxe'
              'u-30387@c#olxeu-32816@b#olxeu-32823@b#search-273@a#srt-266@b#srt-386@b; _gid=GA1.2.1893756362.159'
              '1013186; newrelic_cdn_name=CF; PHPSESSID=ppqngvnlqtvbdjp48fjbd2isvm; mobile_default=desktop; new_'
              'dfp_segment_dfp_user_id_08414dde-da9f-d501-4fce-23b06aa2fd01-ver2=%5B%22t000%22%2C%22t076%22%5D; '
              'dfp_segment=%5B%22t000%22%2C%22t076%22%5D; fingerprint=MTI1NzY4MzI5MTs4OzA7MDswOzA7MDswOzA7MDswOzE'
              '7MTsxOzE7MTsxOzE7MTsxOzE7MTsxOzE7MTswOzE7MTsxOzA7MDsxOzE7MTsxOzE7MTsxOzE7MTsxOzA7MTsxOzA7MTsxOzE7M'
              'DswOzA7MDswOzA7MTswOzE7MTswOzA7MDsxOzA7MDsxOzE7MDsxOzE7MTsxOzA7MTswOzEyMDQzNDQ2NzY7MjsyOzI7MjsyOz'
              'I7MzsxMjM3Njc3NTc5OzE2NTk1ODk2NDk7MTsxOzE7MTsxOzE7MTsxOzE7MTsxOzE7MTsxOzE7MTsxOzA7MDswOzIxMzIwMzE'
              '0MjQ7NTM4MDk4Nzc4OzIwNTUxNzg4MjQ7MzMwODM4ODQxOzEwMDUzMDEyMDM7MjA0ODs4NjQ7MjQ7MjQ7MTIwOzYwOzEyMDs2M'
              'DsxMjA7NjA7MTIwOzYwOzEyMDs2MDsxMjA7NjA7MTIwOzYwOzEyMDs2MDsxMjA7NjA7MTIwOzYwOzA7MDsw; searchFavTo'
              'oltip=1; ldTd=true; __utma=221885126.2040892305.1568205790.1591086687.1591123553.16; __'
              'utmc=221885126; __utmz=221885126.1591123553.16.16.utmcsr=google|utmccn=(organic)|'
              'utmcmd=organic|utmctr=(not%20provided); __utmt=1; lqstatus=1591124753; search_id'
              '_md5=fa7728949163f46047398ee99359b9f2; pt=e44f2dfe68dd2c6433d64b66a70a7897a15faa713c9ec1c2933b5d2e'
              '824f245afc5933ecfafed68e5232c808d02ef55ad241d9911919e0ed2df2f2a5bf1bdfe2; from_detail=1; '
              'onap=16d20595b38x5d109d2c-16-172765aa8edx191d38d9-12-1591125454; __utmb=221885126.5.10.1591123553',
}

data = {
        'otodom':
            {'main': {
                'tag': 'article',
                'class': None
            },
                'price': {
                    'tag': 'li',
                    'class': 'offer-item-price'
                },
                'district': {
                    'tag': 'p',
                    'class': 'text-nowrap'
                },
                'url': 'https://www.otodom.pl/wynajem/?page={}',
                'headers': headers
            },
        'olx':
            {'main': {
                'tag': 'tr',
                'class': 'wrap'
            },
                'price': {
                    'tag': 'p',
                    'class': 'price'
                },
                'district': {
                    'tag': 'small',
                    'class': 'breadcrumb x-normal'
                },
                'url': 'https://www.olx.pl/nieruchomosci/mieszkania/wynajem/?page={}',
                'headers': headers2
            },}


if __name__ == '__main__':
    city = InputProcessingName(sys.argv[1])
    minPrice = int(sys.argv[2])
    maxPrice = int(sys.argv[3])
    district = InputProcessingDis(sys.argv[4])
    jsonData = {'otodom': [],
                'olx': []}

    with open('scriptFlats.json', 'w') as jsonFile:
        for key in data:
            for count in range(1, searchAmount + 1):
                #request-processing
                response = requests.get(data[key]['url'].format(count),
                                        headers=data[key]['headers'])
                soup = BeautifulSoup(response.content, 'html.parser')

                if data[key]['main']['class']:
                    allArticles = soup.find_all(data[key]['main']['tag'],
                                                class_=data[key]['main']['class'])
                else:
                    allArticles = soup.find_all(data[key]['main']['tag'])

                for singleArticle in allArticles:
                    singleArticleText = singleArticle.prettify()
                    if city in singleArticleText:

                        #Rent-processing
                        liPriceTag = singleArticle.find(data[key]['price']['tag'],
                                                        class_=data[key]['price']['class'])
                        currentPrice = re.search('\s\s[[[0-9][0-9][0-9]',
                                                 liPriceTag.get_text())
                        if not currentPrice:
                            currentPrice = re.search('\s[0-9]\s[0-9][0-9][0-9]',
                                                     liPriceTag.get_text())
                            if not currentPrice:
                                currentPrice = re.search('\s[0-9][0-9]\s[0-9][0-9][0-9]',
                                                         liPriceTag.get_text())
                        if currentPrice:
                            currentPriceINT = int(currentPrice.group(0).replace(' ',''))
                            if PriceComparison(currentPriceINT, minPrice, maxPrice):

                                #District-processing
                                if key == 'otodom':
                                    DistrictTag = singleArticle.find(data[key]['district']['tag'],
                                                            class_=data[key]['district']['class'])
                                elif key == 'olx':
                                    DistrictTag = singleArticle.find_all(data[key]['district']['tag'],
                                                class_=data[key]['district']['class'])[1].find('span')

                                currentDistrict = re.search('(?<={},\s)\w+'.format(city),
                                                            DistrictTag.get_text())
                                if not district or district == currentDistrict.group(0).strip():
                                    #final url
                                    aTag = singleArticle.find('a')
                                    hrefOutput = aTag.get('href')
                                    jsonData[key].append({currentPriceINT: hrefOutput})
                                    print(hrefOutput)

        json.dump(jsonData, jsonFile, indent=2)
