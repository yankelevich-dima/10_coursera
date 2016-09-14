import sys
import json
import requests
from xml.etree import ElementTree

import pandas as pd
from bs4 import BeautifulSoup


TOP_COUNT = 20


def get_courses_list():
    response = requests.get('https://www.coursera.org/sitemap~www~courses.xml')
    tree = ElementTree.fromstring(response.content)
    urls = [child[0].text for child in tree]
    return urls


def get_course_info(course_url):
    response = requests.get(course_url)

    # If course not exists, coursera reroutes you to another url
    if response.url != course_url:
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    course_info = {'url': course_url}

    # Parsing rating
    rating_block = soup.select('.ratings-text.bt3-visible-xs')
    if rating_block:
        course_info['rating'] = rating_block[0].text.split(' ')[0]

    # Parsing language and week count
    table_rows = soup.select('.basic-info-table tbody')[0].select('tr')
    for row in table_rows:
        if row.select('td span')[0].text == 'Language':
            course_info['language'] = row.select('.td-data span span')[0].text
        elif row.select('td span')[0].text == 'Commitment':
            course_info['week_count'] = row.select('.td-data')[0].text

    # Parsing start Date
    json_data = soup.select('.rc-CourseGoogleSchemaMarkup')
    if json_data:
        course_data = json.loads(json_data[0].text)
        course_info['date_start'] = course_data['hasCourseInstance'][0].get('startDate', None)
        course_info['date_end'] = course_data['hasCourseInstance'][0].get('endDate', None)

    # If one of field is None - return None
    return course_info if len(course_info) == 6 else None


def output_courses_info_to_xlsx(filepath, cources_info):
    df = pd.DataFrame(cources_info)
    df.to_excel(filepath)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        courses = get_courses_list()
        courses_infos = []
        for course in courses:
            info = get_course_info(course)
            if info is not None:
                print('Added {}'.format(info['url']))
                courses_infos.append(info)
                if len(courses_infos) == TOP_COUNT:
                    break
        output_courses_info_to_xlsx(filepath, courses_infos)

    else:
        print('Please enter path to excel file')
