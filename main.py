from services.check_price_page import check_price_page
from dotenv import dotenv_values as load_dotenv
import os

config = load_dotenv(".env")


url = config.get("URL_PAGE")
class_name = config.get("CLASS_NAME")
class_element_type = config.get("CLASS_ELEMENT_TYPE")
price = check_price_page(url, class_name, class_element_type)
print(f"The price is: ${price}")
