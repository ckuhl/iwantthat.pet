from bs4 import BeautifulSoup
import requests


UNAVAILABLE = 'Sorry, the animal you are trying to view is not available.'
ADOPTED = 'This animal has found its forever home!'


def get_animal_page(animal_id):
        BASE_URL = 'https://humaneanimalrescuepets.shelterbuddy.com/'
        ADDRESS = 'animal/animalDetails.asp?searchType=4&rspca_id=%s'

        animal = BASE_URL + ADDRESS % animal_id
        page = requests.get(animal)
        return page.content

def is_animal_adopted(page_content):
    """
    Return whether or not the animal is available
    """
    if UNAVAILABLE in page_content:
        return True
    if ADOPTED in page_content:
        return True
    return False

def get_name(page):
    """
    Grab the animal's name from the page content
    """
    soup = BeautifulSoup(page, 'html.parser')
    soup.prettify()
    name = soup.find("legend", class_="animalNameHeader").contents[0]
    return name.strip().split('\'')[0]

