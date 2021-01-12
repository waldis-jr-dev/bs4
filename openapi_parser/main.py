import requests
from bs4 import BeautifulSoup
from os import path

global main_url



def get_main_file(request_url: str) -> str:
    resp = requests.get(request_url).text
    soup = BeautifulSoup(resp, 'lxml')
    if soup.find('redoc') is not None and 'spec-url' in soup.find('redoc').attrs:
        spec_url = soup.find('redoc').attrs['spec-url']
        global main_url = path.dirname(request_url + spec_url)
        with open(path.basename(spec_url))


def download_yaml_file(request_url: str) -> str:

    pass


if __name__ == '__main__':
    path = 'http://develop.jazzserve.com:9095/innovate/doc/'
    get_main_file(path)

