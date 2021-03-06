import requests


def get_scryfall_json(card: tuple) -> object:

    """Returns the json object of the card passed in.
    Scryfall uses a fuzzy API so minor misspelings are allowed."""

    card_url = "https://api.scryfall.com/cards/named?fuzzy=" + " ".join(card).title()
    scryfall_json = requests.get(card_url)
    return scryfall_json.json()


def get_card_image(card: tuple) -> tuple:

    """Returns the image of a card and the correct name.
    If the card does not exist, then it raises a value error."""

    scryfall_json = get_scryfall_json(card)

    if scryfall_json["object"] == "error":
        raise ValueError("Card does not exist.")
    else:
        image_url = scryfall_json["image_uris"]["normal"]
        card_name = scryfall_json["name"]
        return (card_name, image_url)


def get_card_legality(card: tuple) -> tuple:

    """Returns the legality of a card and the correct name.
    If the card does not exist, then it raises a value error."""

    scryfall_json = get_scryfall_json(card)

    if scryfall_json["object"] == "error":
        raise ValueError("Card does not exist.")
    else:
        card_name = scryfall_json["name"]
        legality_json = scryfall_json["legalities"]
        return (card_name, legality_json)
