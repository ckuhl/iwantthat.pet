from bs4 import BeautifulSoup
import requests


# TODO: A class is not the right format for this


UNAVAILABLE = 'Sorry, the animal you are trying to view is not available.'


class Animal(object):
    def __init__(self, animal_id):
        self.animal_id = animal_id
        page = self.get_html()
        self.name = self.get_name(page)

    def get_html(self):
        BASE_URL = 'https://humaneanimalrescuepets.shelterbuddy.com/'
        ADDRESS = 'animal/animalDetails.asp?searchType=4&animalid=%d'

        animal = BASE_URL + ADDRESS % self.animal_id
        page = requests.get(animal)
        return page.content

    def get_name(self, page):
        soup = BeautifulSoup(page, 'html.parser')
        soup.prettify()
        name = soup.find("legend", class_="animalNameHeader").contents[0]
        return name.strip().split('\'')[0]

