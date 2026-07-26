import os
import time

from dotenv import dotenv_values as load_dotenv

from services.check_price_page import check_price_page, normalize_price
from services.discord_notification_service import send_discord_notification

config = load_dotenv(".env")

url = config.get("URL_PAGE") or os.environ.get("URL_PAGE")
class_name = config.get("CLASS_NAME") or os.environ.get("CLASS_NAME")
class_element_type = config.get("CLASS_ELEMENT_TYPE") or os.environ.get("CLASS_ELEMENT_TYPE")
discord_webhook_url = config.get("DISCORD_WEBHOOK_URL") or os.environ.get("DISCORD_WEBHOOK_URL")
# Prefer the direct hidden Amazon price field instead of the old XPath fallback.
xpath = None

price_text = None
price_value = None

for attempt in range(3):
    price_text = check_price_page(url, class_name, class_element_type, xpath=xpath)
    price_value = normalize_price(price_text)
    if price_value is not None:
        break
    time.sleep(1)

if price_value is None:
    print(f"Could not parse price from page: {price_text}")
    raise SystemExit(0)

if isinstance(price_text, str) and ("blocked" in price_text.lower() or "not found" in price_text.lower()):
    print(price_text)
    raise SystemExit(0)

print(f"Current price: ${price_text}")
print(f"Numeric price: {price_value}")

# Send Discord notification
if discord_webhook_url:
    try:
        send_discord_notification(discord_webhook_url, price_value)
        print("✓ Discord notification sent successfully!")
    except Exception as e:
        print(f"✗ Failed to send Discord notification: {e}")
else:
    print("⚠ Discord webhook URL not configured")
