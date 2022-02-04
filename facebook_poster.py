import datetime
import random

from sample.prestashop_api import PrestaShopWebService, Product
from sample import database
from sample.facebook_api import FacebookPage

DEVELOP_MODE = True

if not DEVELOP_MODE:
    from config.credentials import FACEBOOK_ACCESS, PRESTASHOP_ACCESS
else:
    from config.dev_credentials import FACEBOOK_ACCESS, PRESTASHOP_ACCESS


def main():
    # Facebook page access initiation
    page = FacebookPage(FACEBOOK_ACCESS['user_access_token'], FACEBOOK_ACCESS["page_id"])
    # Prestashop access initiation
    shop = PrestaShopWebService(PRESTASHOP_ACCESS['api'], PRESTASHOP_ACCESS['api_key'])

    product = pick_product(shop, database.get_all_id())

    # Add product_id to posted product database
    database.add(product.id)

    # Post link to facebook page
    message = ''  # TODO message generated by AI
    page.put_object(link=product.url, message=message)


def pick_product(shop: PrestaShopWebService, posted_id: list) -> Product:
    active_id = set(shop.get_id_products_active())
    available_id = list(active_id.difference(posted_id))
    return Product(shop, random.choice(available_id))


if __name__ == '__main__':
    main()
