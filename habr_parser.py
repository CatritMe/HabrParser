import requests
from bs4 import BeautifulSoup


def get_links(hab):
    """
    Получение сырых данных с сайта(html-код)
    Возвращает список найденных статей в хабе и название хаба
    """
    url = hab
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    hab_title = soup.title.string
    links = soup.find_all('a', class_='tm-article-datetime-published tm-article-datetime-published_link')
    return links, hab_title


def get_info(link):
    """
    Получение информации о статьях
    :param link: список найденных статей
    :return: ссылка на статью, название статьи, дата публикации, ник автора, ссылка на автора
    """
    url_article = f'https://habr.com{link.get('href')}'
    response = requests.get(url_article)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.title.string
    date = soup.time['datetime']
    try:
        author_name = soup.find('a', class_='tm-user-info__username').text
    except AttributeError:
        author_name = soup.find('a', class_='tm-publication-hub__link').text
    try:
        author_url = f'https://habr.com{soup.find('a', class_='tm-user-info__username')['href']}'
    except TypeError:
        author_url = f'https://habr.com{soup.find('a', class_='tm-publication-hub__link')['href']}'
    return url_article, title, date, author_name, author_url


def print_info(hab_title, hab, title, date, author_name, author_url, url_article):
    print(f'Добавлена запись:\n'
          f'хаб: {hab_title}, {hab}\n'
          f'статья: {title}, {url_article}\n'
          f'автор: {author_name}, {author_url}\n'
          f'дата публикации: {date}\n'
          f'-----------------------------\n')
