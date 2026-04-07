
import requests


def send_discord_notification(webhook_url,price):
    webhook_url = webhook_url
    message = f"The price is: ${price}"
    requests.post(webhook_url, json={"content": message})
    
