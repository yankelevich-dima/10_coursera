import sys
import helpers
import requests
import string
from xml.etree import ElementTree

from bs4 import BeautifulSoup
from openpyxl import Workbook


TOP_COUNT = 20
DEFAULT_FILEPATH = 'Cources.xlsx'


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

    course_info = {'url': course_url}

    keys = ['rating', 'start_date', 'end_date', 'week_count', 'language']
    soup = BeautifulSoup(response.content, 'html.parser')

    for element in keys:
        course_info[element] = getattr(helpers, 'get_{}'.format(element))(soup)

    # If one of field is None - return None
    return course_info if None not in course_info.values() else None


def output_courses_info_to_xlsx(filepath, cources_info):
    wb = Workbook()
    ws = wb.active

    # Setting order of columns in excel file
    keys = ['url', 'rating', 'start_date', 'end_date', 'week_count', 'language']
    ws.append(keys)

    # Making header row bold
    for letter in string.ascii_uppercase[:len(keys)]:
        cell = ws['{}1'.format(letter)]
        cell.font = cell.font.copy(bold=True)

    # Writing data to excel
    for record in cources_info:
        ws.append([record[key] for key in keys])

    wb.save(filepath)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        filepath = DEFAULT_FILEPATH
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
