import re
import requests
from urllib.parse import urlparse


def search_emails(url, power):
    visitedPages.add(url)

    # Проверка на доступность url
    try:
        page = requests.get(url)

    except requests.exceptions.RequestException:
        print("Bad page" + url)
        return

    # Поиск электронных почт, находящихся на странице
    mail_regex_pattern = re.compile(r'<a href=\"mailto\:[a-zA-Z0-9\.\_\-]+@[a-zA-Z0-9\-\.\_]+\"')
    dirty_mails = set(mail_regex_pattern.findall(page.text))

    # "Очистка" адресов почты от html-тегов
    for mail in dirty_mails:
        mails.add(''.join(re.findall(r"(?<=\:)[^}]*(?=\")", mail)))

    # Поиск ссылок на страницы данного сайта
    page_regex_pattern = re.compile(r'<a href=\"/[a-zA-z0-9\/\_\- ]+\"|'
                                    r'<a href=\"[a-zA-z0-9\/\_\- ]+\"|'
                                    r'<a href=\"[a-zA-Z0-9\/\:\.\_\-]+.' + domain + r'[a-zA-z0-9\/\_\- ]+\"')

    dirty_pages = set(page_regex_pattern.findall(page.text))
    pages = set()

    # Очистка адресов страниц от html-тегов
    for page in dirty_pages:
        page = ''.join(re.findall(r"(?<=\")[^}]*(?=\")", page))
        if re.findall(domain, page):
            pages.add(page)
        elif page.__len__() > 0 and page[0] != '/':
            pages.add(URL + '/' + page)
        else:
            pages.add(URL + page)

    # Вывод информации о странице
    print(url)
    print(mails.__len__())
    print()

    # Поиск в глубину по другим страницам сайта
    for page in pages:
        if visitedPages.__contains__(page):
            continue

        if power <= 0:
            continue

        search_emails(page, power - 1)


# Ввод начальной страницы
URL = input("format: protocol://domains\n")
# Задание глубины обхода
power = int(input("power\n"))

# Данные действия необходимы для нахождения страниц,
# относящихся к тому же домену второго уровня
info = urlparse(URL)
try:
    domain = info.netloc
    nameList = domain.split(".")
    domain = "%s.%s" %(nameList[-2], nameList[-1])
except:
    print("Bad addr")
    exit()

visitedPages = set()
mails = set()

if URL[-1] == '/':
    URL = URL[:-1]


search_emails(URL, power)
print(mails.__len__())
print(mails)