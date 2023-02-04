from dotenv import load_dotenv
import os
import requests
from urllib.parse import urlparse
import argparse
load_dotenv()


def shorten_link(token, long_url):
    url = "https://api-ssl.bitly.com/v4/bitlinks"
    headers = {"Authorization": token}
    body = {
        'long_url':long_url
    }
    
    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    bitlink = response.json()
    
    return bitlink['link']


def count_clicks(token, short_url):
    url = "https://api-ssl.bitly.com/v4/bitlinks/{}/clicks/summary".format(short_url)
    payload = {"Authorization": token}
    body = {
        'unit':'day',
        'units':-1
    }
    
    response = requests.get(url, headers=payload, params=body)
    response.raise_for_status()
    total_clicks = response.json()
    
    return total_clicks['total_clicks']


def is_bitlink(url, token):
    formated_url = 'https://api-ssl.bitly.com/v4/bitlinks/{}'.format(url)
    headers = {"Authorization": token}
    response = requests.get(formated_url, headers=headers)
    return response.ok


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Описание того, что делает программа')
    parser.add_argument('link', help='Ссылка для сокращения или битлинк')
    args = parser.parse_args()

    api_key = '0285a5d9b1374005cbdb28192cf6f02f497b3dd4'
    parsed_url = urlparse(args.link)
    url = '{0}{1}'.format(parsed_url.netloc, parsed_url.path)
    

    if is_bitlink(url, api_key):
        print('Эта ссылка уже битлинк. Всего нажатий: {}'.format(count_clicks(api_key, url)))
    else:
        print('Ссылка сокращена. Это битлинк: {}'.format(shorten_link(api_key, args.link)))