import requests
import math

def get_card_image(card : tuple) -> tuple:

    """This method returns the image of a card and the correct name.
    If the card does not exist, then it raises a value error.
    Scryfall uses a fuzzy API so minor misspelings are allowed."""

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
    Scryfall uses a fuzzy API so minor misspelings are allowed."""

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

    """Returns the correct spelling of a card using
    the fuzzy API. (Example: 'lightning balt' --> 'lightning bolt')
    Scryfall acts as the source of truth. This should only be used after 
    calling card_exists as it assumes the card exist."""

    cardURL = "https://api.scryfall.com/cards/named?fuzzy=" + " ".join(card).title()
    scryfall_json = requests.get(cardURL)
    card_name = scryfall_json.json()["name"]
    return card_name
    