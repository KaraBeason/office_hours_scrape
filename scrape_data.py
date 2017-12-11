import urllib.request as urlreq
from bs4 import BeautifulSoup as bs
import re
import mysql.connector
from mysql.connector import errorcode


def get_faculty_info(url):
    url_html = urlreq.urlopen(url)
    page_soup = bs(url_html, 'html.parser')
    email = get_email(page_soup)
    # print(email)
    # location = get_office(page_soup)
    # print(location)


def get_email(soup):
    for a in soup.find_all('a'):
        if a and a.get('href') and "@" in a.get('href'):
            return a.get('href').split(":")[1]
    return "no email listed"


# def get_office(page_soup):
    # for element in page_soup.select('span.contact'):
        # print(element.text)


# url to scrape
cs_faculty = 'https://compsci.appstate.edu/faculty-staff'

# get the html
page = urlreq.urlopen(cs_faculty)

# parse using beautiful soup
soup = bs(page, 'html.parser')
faculty_sites = []
for link in soup.find_all('a'):
    faculty_sites.append(link.get('href'))

#  get all faculty web pages
faculty_sites[:] = (url for url in faculty_sites if url and url.startswith('http://cs.appstate.edu/~'))

# print(faculty_sites)
for f in faculty_sites:
    get_faculty_info(f)

math_faculty ='https://mathsci.appstate.edu/OfficeHours'
page = urlreq.urlopen(math_faculty)
soup = bs(page, 'html.parser')


table = soup.find('table')
rows = []
for row in table.findChildren('tr'):
    if len(row.find_parents('tr')) == 0:
        rows.append(row)
rows.pop(0)


contact_list = []
for row in rows:
    contact = []
    # some extra bs because wtf is this table formatting for?
    cells = row.findChildren('td')
    if len(cells) >= 4:
        for  i in range(0, 4):
            cell_content = cells[i].getText()
            clean_content = re.sub( '\s+', ' ', cell_content).strip()
            contact.append(clean_content)
        temp = []
        for i in range(4, len(cells)):
            cell_content = cells[i].getText()
            clean_content = re.sub( '\s+', ' ', cell_content).strip()
            temp.append(clean_content)
        office_hours = ', '.join(set(temp)) # get rid of duplicates, join all office hours into one string
        contact.append(office_hours)
        contact_list.append(contact)
# print(contact_list)

def create_faculty_members(contact):
    # MySql configs

    try:
        conn = mysql.connector.connect(user='kara', password='admin',
                                   host='127.0.0.1',
                                   database='officehours')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cursor = conn.cursor()
        _name = contact[0]
        _email = contact[1]
        _phone = contact[2]
        _office = contact[3]
        _department = "math"
        _user_type = "teacher"
        _office_hours = contact[4]
        # _hours = d[4]
        cursor.callproc('sp_createFacultyMember',(_name, _email, _phone, _office, _department, _office_hours, _user_type))
        conn.commit()
        # cursor.execute("SELECT * FROM tbl_user")

        # print the first and second columns
        # for row in cursor.fetchall():
        #     print(row)
        cursor.close()
        conn.close()

for c in contact_list:
    create_faculty_members(c)



