import requests
from bs4 import BeautifulSoup as bs
from app import db, Hospital


def scrape():
    try:
        url = 'https://www.hospitalsafetygrade.org/all-hospitals'

        response = requests.get(url).content

        soup = bs(response, "html.parser")
        # opening main page
        try:
            links = soup.select('#BlinkDBContent_849210 ul li a')

        except:
            print("ERROR:  Couldn't find any hospital")

        # start a for loop
        i = 0
        for link in links:

            # opening leap frog page
            try:
                print("Visiting -->  " + link['href'])
                new_response = requests.get(link['href']).content

                soup = bs(new_response, "html.parser")

                redir_one = soup.select(
                    '#survey-results-container a')[0]['href']

            except:
                print("ERROR: Couldn't open hospital Leap Frog Page")

            # Opening survery results page
            try:
                print('  Redirecting to --->  ' + redir_one)
                an_response = requests.get(redir_one).content

                soup = bs(an_response, "html.parser")

            except:
                print("ERROR: Couldn't open survey results")

                # getting the name of the hospital
            try:
                name = soup.find_all(
                    'h1', class_='quote-large blue margin-bottom-20')[0].text
            except:
                name = ""

            # getting the address of the hospital
            try:
                address = soup.select('.facility-address strong')[0].text.replace(
                    '\n', '').replace('                        ', '')
            except:
                address = ""

            try:
                website = soup.select(
                    '.margin-bottom-40')[0].select('tr')[1].select('td a')[0]['href']
            except:
                website = ""

            data = Hospital(name=name, address=address, website=website)
            db.session.add(data)
            db.session.commit()

            # with open('hospital.csv', 'a') as h:
            #     writer = csv.writer(h, delimiter='|')
            #     writer.writerow([name, address, website])

            print(f'SUCCESS --> HOSPITAL INFO GOTTEN ---> {i + 1}')

            i += 1

    except ConnectionError:
        print('Network Error --> Try Again')
    except ConnectionAbortedError:
        print('Network Error --> Try Again')
    except ConnectionRefusedError:
        print('Network Error --> Try Again')
    except ConnectionResetError:
        print('Network Error --> Try Again')
