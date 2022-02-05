import requests


class PrestaShopWebService:
    def __init__(self, website_url, api_key):
        self._urls = {
            'website': website_url,
            'api': f"{website_url}/api",
            'products': f"{website_url}/api/products",
            'categories': f"{website_url}/api/categories"
        }
        self._session = self.__set_session(api_key=api_key)

    @staticmethod
    def __set_session(api_key) -> requests.Session:
        session = requests.Session()
        session.params = {
            'io_format': 'JSON'
        }
        session.auth = (api_key, '')
        return session

    def get_id_products_active(self) -> list[int]:
        params = {
            'display': '[id]',
            'filter[active]': str(1),
        }
        content = self._session.get(self._urls.get("products"), params=params).json()
        return [x["id"] for x in content['products']]

    @property
    def urls(self):
        return self._urls

    @property
    def session(self):
        return self._session


class Product:

    def __init__(self, shop: PrestaShopWebService, product_id):
        self.__session = shop.session
        self.__urls = shop.urls
        self.__product_details = self.__get_product_details(product_id)

    def __get_product_details(self, product_id):
        params = {
            'display': 'full',
            'filter[id]': product_id
        }
        return self.__session.get(self.__urls.get('products'), params=params).json()

    def __category_link_rewrite(self):
        params = {
            'display': '[link_rewrite]',
            'filter[id]': self.__product_details['products'][0]['id_category_default']
        }
        content = self.__session.get(self.__urls.get('categories'), params=params).json()
        return content["categories"][0]["link_rewrite"]

    @property
    def url(self):
        website = self.__urls.get('website')
        category = self.__category_link_rewrite()
        product = f'{self.__product_details["products"][0]["id"]}-{self.__product_details["products"][0]["link_rewrite"]}'
        return f"{website}/{category}/{product}.html"

    @property
    def description(self):
        return self.__product_details['products'][0]['description']

    @property
    def id(self):
        return self.__product_details['products'][0]['id']
