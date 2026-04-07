from services.check_price_page import check_price_page
from services.discord_notification_service import send_discord_notification 
from dotenv import dotenv_values as load_dotenv
import os

config = load_dotenv(".env")


url = config.get("URL_PAGE")
class_name = config.get("CLASS_NAME")
class_element_type = config.get("CLASS_ELEMENT_TYPE")
price = check_price_page(url, class_name, class_element_type)

if float(price) < 4.00:
    send_discord_notification(config.get("DISCORD_WEBHOOK_URL"), price)
else :
    print(f"The price is: ${price}, which is above the threshold.")