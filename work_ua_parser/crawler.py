import requests
from typing import Optional, Iterable
import parser


SEARCH_STRING = 'python'
LAST_PAGE = None


def domain() -> str:
    return 'www.work.ua'


def get_search_url(job_type: str = None, page: int = None) -> Optional[str]:
    if job_type is None:
        return
    if page is None:
        return f'https://{domain()}/jobs-kyiv-{job_type}/'
    return f'https://{domain()}/jobs-kyiv-{job_type}/?page={page}'


def send_request(url: str) -> str:
    resp = requests.get(url)
    final_data = resp.text
    return final_data


def save_html(html: str):
    with open('page.html', 'w') as file:
        file.write(html)


def get_full_url(url_tail: str) -> str:
    """Make full url from tail and domain"""
    return f'https://{domain()}{url_tail}'


def send_request_for_vacansy(url_tail: str) -> str:
    url = get_full_url(url_tail)
    resp = requests.get(url)
    final_data = resp.text
    return final_data


def parse_one_page_all_data(page_number=1) -> Iterable[dict]:
    global LAST_PAGE
    url = get_search_url(SEARCH_STRING, page=page_number)
    response_text = send_request(url)
    if LAST_PAGE is None:
        LAST_PAGE = parser.parse_last_page(response_text)

    all_data = {
        'preview_data': None,
        'full_data': None
    }

    data = parser.parse_preview_data(response_text, page_number)
    for element in data:
        full_vacancy_raw_data = send_request_for_vacansy(element['url_tail'])
        answer = all_data.copy()
        answer['preview_data'] = element
        answer['full_data'] = parser.parse_full_vacancy(full_vacancy_raw_data)
        yield answer


def pagination() -> Iterable[dict]:
    global LAST_PAGE
    for element in parse_one_page_all_data():
        yield element

    for page_number in range(2, LAST_PAGE+1):
        print(page_number)
        for element in parse_one_page_all_data(page_number):
            yield element


if __name__ == '__main__':
    lol = pagination()
    for i in lol:
        print(i)
