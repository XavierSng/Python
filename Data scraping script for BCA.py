""" Collation of company contacts and detail"""
import requests
import csv
import time
from bs4 import BeautifulSoup

# Function for calling company detail on company page


def company_contacts(url):

    # Requesting of html
    results = requests.get(url)

    # Checking if html successfully requested
    if results.status_code == 200:

        company_html = BeautifulSoup(results.text, "html.parser")

        # Company name
        html_class = company_html.find_all(attrs={'class': 'body-bluetext bold'})
        company_name = html_class[0].string

        # Company UEN
        div = company_html.find_all('div')
        uen = div[60].string.lstrip('UEN No. : ')

        # Company Address
        address = div[61].string.lstrip('Address : ')

        # Company telephone
        td = company_html.find_all('td')
        tele = td[2].string

        # Company specialisation
        specialisation_html = company_html.findAll(attrs='title')
        specialisation = [y.string for y in specialisation_html]

        # Formatting of specialisation
        all_specialisation = ''

        for y in specialisation:
            y = y.strip()
            all_specialisation += y + '/ '

        all_specialisation = all_specialisation.rstrip('/ ')

        # Collated into data as list
        company_data = [company_name, tele, uen, address, all_specialisation]
        print(company_data)

        total_data.append(company_data)

    else:
        print('Error, html request failed [Company]')


# Starting page
page = 1

# All data collected appended here
total_data = [["Company Name", "Contact No.", "UEN No.", "Address", "Specialisation"]]

# End page
while page < 1000:

    # Based URL used to collate individual company URL, once loop finishes add '1' to page variable
    base_url = f'https://bca.gov.sg/BCADirectory/Search/Result?pBLSSelected=%2C140%2C141%2C142%2C143%2C144%2C145%2C146%2C147&pGrading=NONE&page={page}&d=0&pCLSCondition=AND&pBLSCondition=OR'
    base_url_html = requests.get(base_url)

    # Checking if html successfully requested
    if base_url_html.status_code == 200:

        html_script = BeautifulSoup(base_url_html.text, 'html.parser')

        # Last page checker
        if not html_script.findAll(string='No record(s) found.'):

            # Collation of individual company URL
            body = html_script.find('tbody')
            url_list = body.find_all('a')

            for incomplete_url in url_list:

                company_url = "https://www.bca.gov.sg" + incomplete_url['href']

                company_contacts(company_url)

            page += 1

            # Time between each page
            time.sleep(0)

        else:
            print('\nLast page reached')
            break

    else:
        print('Error, failed html request [Directory]')
        break

else:
    print('Requested page reached')


# Adding of data into CSV file
with open('BCA_contacts_Contractor.csv', 'w', newline='') as file:
    writer = csv.writer(file)

    for x in total_data:
        writer.writerow(x)

print('\nData added into .csv')
