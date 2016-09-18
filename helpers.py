import json
from bs4 import BeautifulSoup


def get_rating(response):
    soup = BeautifulSoup(response.content, 'html.parser')

    rating_block = soup.select('.ratings-text.bt3-visible-xs')
    if rating_block:
        return rating_block[0].text.split(' ')[0]
    else:
        return None


def get_language(response):
    soup = BeautifulSoup(response.content, 'html.parser')

    table_rows = soup.select('.basic-info-table tbody')[0].select('tr')
    for row in table_rows:
        if row.select('td span')[0].text == 'Language':
            return row.select('.td-data span span')[0].text
    return None


def get_week_count(response):
    soup = BeautifulSoup(response.content, 'html.parser')

    table_rows = soup.select('.basic-info-table tbody')[0].select('tr')
    for row in table_rows:
        if row.select('td span')[0].text == 'Commitment':
            return row.select('.td-data')[0].text
    return None


def get_start_date(response):
    soup = BeautifulSoup(response.content, 'html.parser')

    json_data = soup.select('.rc-CourseGoogleSchemaMarkup')
    if json_data:
        course_data = json.loads(json_data[0].text)
        return course_data['hasCourseInstance'][0].get('startDate', None)

    return None


def get_end_date(response):
    soup = BeautifulSoup(response.content, 'html.parser')

    json_data = soup.select('.rc-CourseGoogleSchemaMarkup')
    if json_data:
        course_data = json.loads(json_data[0].text)
        return course_data['hasCourseInstance'][0].get('endDate', None)

    return None
