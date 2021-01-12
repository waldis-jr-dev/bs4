from bs4 import BeautifulSoup
from typing import Iterable, Optional


def parse_preview_data(data_html: str, page_number: int) -> Iterable[dict]:
    if page_number > 1:
        class_name = 'card card-hover card-visited wordwrap job-link'
    else:
        class_name = 'card card-hover card-visited wordwrap job-link js-hot-block'

    for element in parse_preview_data_different_class(data_html, class_name):
        yield element


def parse_preview_data_different_class(data_html: str, class_name: str) -> Iterable[dict]:
    soup = BeautifulSoup(data_html, 'lxml')
    data_dict = {
        'job_name': None,
        'firm_name': None,
        'url_tail': None,
        'cost': None,
        'description': None
    }

    divs = soup.find_all('div', {'class': class_name})
    for div in divs:
        data = data_dict.copy()

        job_name = div.findChild('a').get_text()
        data['job_name'] = job_name

        url_tail = div.findChild('a').get('href')
        data['url_tail'] = url_tail

        cost = div.findChild('b').get_text()
        if 'грн' in cost or '$' in cost:
            data['cost'] = cost

        firm_name_div = div.findChild('div', {'class': 'add-top-xs'})
        firm_name = firm_name_div.findChild('b').get_text()
        data['firm_name'] = firm_name

        description = div.findChild('p', {'class': 'overflow text-muted add-top-sm add-bottom'}).get_text().strip()
        data['description'] = description
        yield data


def parse_full_vacancy(data_html: str) -> Iterable[dict]:
    soup = BeautifulSoup(data_html, 'lxml')
    div_job_description = soup.find('div', {'id': 'job-description'})
    return div_job_description.get_text()


def parse_last_page(data_html: str) -> Optional[int]:
    soup = BeautifulSoup(data_html, 'lxml')
    nav_tag_pages = soup.find_all('nav')
    li_tag_pages = nav_tag_pages[-1].findChildren('li')
    a_tag_last_page = li_tag_pages[-2].findChild('span')
    title_text = a_tag_last_page.get('title')
    last_page_number = title_text.split()[-1]
    try:
        return int(last_page_number)
    except ValueError:
        return
