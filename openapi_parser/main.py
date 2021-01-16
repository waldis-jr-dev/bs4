from bs4 import BeautifulSoup
import os
import requests
import yaml


def get_main_file_url(request_url: str) -> str:
    resp = requests.get(request_url).text
    soup = BeautifulSoup(resp, 'lxml')
    if soup.find('redoc') is not None and 'spec-url' in soup.find('redoc').attrs:
        spec_url = soup.find('redoc').attrs['spec-url']
        return request_url + spec_url


def download_and_parse_yaml_file(request_url: str) -> str:
    if not os.path.exists(dir): 
        os.mkdir(dir)
    with open(f"/{spec_url}", 'w') as file:
        file.write()
    return os.path.dirname(full_url)


def main(main_url: str):
    main_file_url = get_main_file_url(main_url)
    work_url = os.path.dirname(main_file_url)


if __name__ == '__main__':
    main('http://develop.jazzserve.com:9095/innovate/doc/')
