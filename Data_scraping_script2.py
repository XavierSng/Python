""" Collation of company contacts and detail"""
import requests
import csv
import time
from bs4 import BeautifulSoup

# Function for calling company detail on company page


def company_contacts(url, name):

    # Requesting of html
    results = requests.get(url)

    # Checking if html successfully requested
    if results.status_code == 200:

        company_html = BeautifulSoup(results.text, "html.parser")

        # Company Address

        address = ''

        address_html = company_html.find('i', attrs={'class': 'icofont-location-pin'})

        if address_html:
            address = address_html.next_sibling.strip()

        else:
            print('No address!')

        # Contact No.

        tele = ''

        phone_html = company_html.find('i', attrs={'class': 'icofont-ui-call'})

        if phone_html:
            tele = phone_html.next_sibling.strip()

        else:
            print('No Contact no.!')

        # Specialisation

        all_specialisation = ''

        specialisation_html = company_html.find('ul', attrs={'class': 'regnheads'})

        if specialisation_html:
            specialisation = specialisation_html.find_all('span')

            for z in specialisation:
                y = z.string
                all_specialisation += y.strip() + '/ '

            all_specialisation = all_specialisation.rstrip('/ ')

        else:
            print('No specialisations!')

        # Collated into data as list
        company_data = [name, tele, address, all_specialisation]
        print(company_data)

        total_data.append(company_data)

    else:
        print('\nError, html request failed [Company]')


# Starting page
page = 1

# All data collected appended here
total_data = [["Company Name", "Contact No.", "Address", "Specialisation"]]

# End page
while page < 500:

    # Based URL used to collate individual company URL, once loop finishes add '1' to page variable
    base_url = f'https://www.scal.com.sg/helper/searchmembers?index={page}&companyName=&memberType=&regnhead=&workhead='
    base_url_contents = requests.get(base_url)

    # Checking if html successfully requested
    if base_url_contents.status_code == 200:

        json_data = base_url_contents.json()

        # Last page checker
        if json_data['data']:

            # Collation of individual company URL
            for url_ingredients in json_data['data']:

                company_link_name = url_ingredients['slug']
                company_scal_id = url_ingredients['id']

                company_url = f'https://www.scal.com.sg/memberlisting-details/{company_scal_id}-{company_link_name}'
                company_name = url_ingredients['name']

                company_contacts(company_url, company_name)

            page += 1

            # Time between each page
            time.sleep(1)

        else:
            print('\nLast page reached')
            break

    else:
        print('\nError, failed html request [Directory]')
        break

else:
    print('\nRequested page reached')


# Adding of data into CSV file
if total_data != [["Company Name", "Contact No.", "Address", "Specialisation"]]:
    with open('SCAL_contacts_ALL.csv', 'w', newline='') as file:
        writer = csv.writer(file)

        for x in total_data:
            writer.writerow(x)

    print('\nData added into .csv')

else:
    print('\nError, no new data')
