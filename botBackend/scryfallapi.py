import requests
import math

""" This makes requests to the scryfall API to get cards and images."""

def get_card_image(card : tuple) -> tuple:

    """This method returns the image of a card and the correct name.
    If the card does not exist, then it raises a value error.
    Since scryfall uses a fuzzy API, you can misspell a card name
    slightly and it will correct it and return the proper spelling. """

    card_url = "https://api.scryfall.com/cards/named?fuzzy=" + " ".join(card).title()
    scryfall_json = requests.get(card_url)
    object_type = scryfall_json.json()["object"]

    if object_type == "error":
        raise ValueError("Card does not exist.")
    else:
        image_url = scryfall_json.json()["image_uris"]["normal"]
        card_name = scryfall_json.json()["name"]
        return (card_name, image_url)

def get_card_legality(card : tuple) -> tuple:
    
    """This method returns the legality of a card and the correct name.
    If the card does not exist, then it raises a value error.
    Since scryfall uses a fuzzy API, you can misspell a card name
    slightly and it will correct it and return the proper spelling."""

    cardURL = "https://api.scryfall.com/cards/named?fuzzy=" + " ".join(card).title()
    scryfall_json = requests.get(cardURL)
    object_type = scryfall_json.json()["object"]

    if object_type == "error":
        raise ValueError("Card does not exist.")
    else:
        card_name = scryfall_json.json()["name"]
        legality_json = scryfall_json.json()["legalities"]
        return (card_name, legality_json)

def card_exists(card : tuple) -> bool:

    """Determines if a card exists."""

    card_url = "https://api.scryfall.com/cards/named?fuzzy=" + " ".join(card).title()
    scryfall_json = requests.get(card_url)
    object_type = scryfall_json.json()["object"]

    return object_type != "error"
    
def get_fuzzied_correct(card : tuple) -> str:

    """This returns the correct spelling of a card using
    scryfalls fuzzy API. If the user enters 'lightning balt', 
    scryfall will realize they meant 'lightning bolt'. 
    This ensures two people can't pick the same card with 
    slightly different spellings. We use whatever scryfall 
    returns as the source of truth. This method should only 
    be used when the card_exists method is called before as 
    it assumes the card does exist."""

    cardURL = "https://api.scryfall.com/cards/named?fuzzy=" + " ".join(card).title()
    scryfall_json = requests.get(cardURL)
    card_name = scryfall_json.json()["name"]
    return card_name
    