from pprint import pprint
import lxml.html
import lxml.html.clean
import requests


def delete_html_symbols(text: str) -> str:
    cleaner = lxml.html.clean.Cleaner()
    return cleaner.clean_html(lxml.html.fromstring(text)).text_content()


def clean_text(text: str) -> str:
    text = delete_html_symbols(text)
    return " ".join(text.split())


class PrestaShopWebService:
    def __init__(self, website_url, api_key):
        self._urls = {
            "website": website_url,
            "api": f"{website_url}/api",
            "products": f"{website_url}/api/products",
            "categories": f"{website_url}/api/categories",
            'product_features': f"{website_url}/api/product_features",
            'product_feature_values': f"{website_url}/api/product_feature_values"
        }
        self._session = self.__set_session(api_key=api_key)

    @staticmethod
    def __set_session(api_key) -> requests.Session:
        session = requests.Session()
        session.params = {"io_format": "JSON"}
        session.auth = (api_key, "")
        return session

    def get_id_products_active(self) -> list[int]:
        params = {
            "display": "[id]",
            "filter[active]": str(1),
        }
        content = self._session.get(self._urls.get("products"), params=params).json()
        return [x["id"] for x in content["products"]]

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
        params = {"display": "full", "filter[id]": product_id}
        return self.__session.get(self.__urls.get("products"), params=params).json()["products"][0]

    def __category_link_rewrite(self):
        params = {
            "display": "[link_rewrite]",
            "filter[id]": self.__product_details["id_category_default"],
        }
        content = self.__session.get(
            self.__urls.get("categories"), params=params
        ).json()
        return content["categories"][0]["link_rewrite"]

    @property
    def url(self):
        website = self.__urls.get("website")
        category = self.__category_link_rewrite()
        product = f'{self.__product_details["id"]}-{self.__product_details["products"][0]["link_rewrite"]}'
        return f"{website}/{category}/{product}.html"

    @property
    def description(self):
        return clean_text(self.__product_details["description"])

    @property
    def description_short(self):
        return clean_text(self.__product_details["description_short"])

    @property
    def atributes(self):
        atributes = self.__product_details['associations']['product_features']

        product_features = []
        for atribute in atributes:
            product_feature = {}

            # Get product_features value
            params = {"display": '[value]', "filter[id]": atribute.get('id_feature_value')}
            response = self.__session.get(self.__urls.get("product_feature_values"), params=params).json()
            product_feature_value = response['product_feature_values'][0]['value']

            # Get product_features name
            params = {"display": '[name]', "filter[id]": atribute.get('id')}
            response = self.__session.get(self.__urls.get("product_features"), params=params).json()
            product_feature_name = response['product_features'][0]['name']

            product_feature[product_feature_name] = product_feature_value
            product_features.append(product_feature)

        return product_features

    @property
    def name(self):
        return self.__product_details['name']

    @property
    def id(self):
        return self.__product_details["id"]
