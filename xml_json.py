import bs4 as bs
import json
import logging
import time


def check_images(nx_images: type[bs]) -> list:
    """
    Transforms images to dictionary for a given product.
    :param nx_images: The images of a product.
    """
    image_num = 1
    product_images = {}
    for image in nx_images:
        type = image["type"]
        while image_num <= int(type):
            product_images[f"image_{image_num}"] = None
            image_num += 1
        product_images[f"image_{type}"] = image["url"]

    return product_images


def check_prices(nx_prices: type[bs]) -> list:
    """
    Transforms prices to dictionary for a given product.
    :param nx_prices: The prices of a product.
    """
    prices = []
    for price in nx_prices:
        currency, value = price.findAll(["nsx:currency", "nsx:value"])
        prices.append({"currency": currency.string, "value": value.string})

    return prices


def parse_xml(contents: str) -> list:
    """
    Parses the xml string and returns a list of dictionaries.
    :param contents: The xml in string representation.
    """
    soup = bs.BeautifulSoup(contents, "lxml")
    items = soup.findAll("nsx:item")

    output = []

    for item in items:
        id = item["id"]
        category, description = item.findAll(["nsx:category", "nsx:description"])
        nx_images = item.findAll("nsx:image")
        images = check_images(nx_images)
        nx_prices = item.find_all("nsx:price")
        prices = check_prices(nx_prices)
        product = {"product_id": id, "product_category": category.string,
                   "product_description": description.string,
                   "product_images": images, "prices": prices}
        output.append(product)

    return output


def xml_json(file: str) -> str:
    """
    Reads and xml file and transforms it in a json file.
    :param file: The file to upload including the path to the file to upload.
    """
    # Read xml content
    try:
        with open(file, "r") as fd:
            contents = fd.read()
    except FileNotFoundError:
        logging.exception(f"No such file: '{file}'.")
        raise

    output = parse_xml(contents)
    json_object = json.dumps(output, indent=2)

    # Write json content
    ts = str(time.time())
    with open(f"sample{ts}.json", "a") as fd:
        fd.write(json_object)
    logging.info(f"Created new file sample{ts}.json")

    return f"sample{ts}.json"
