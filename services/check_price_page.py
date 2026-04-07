import requests
from bs4 import BeautifulSoup


def check_price_page(url, class_name, class_element_type):
    
    headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')

        price_element = soup.find(class_element_type ,class_=class_name)
        
        if price_element:
            price = price_element.get_text().strip()
            return price
        else:
            return "Price element not found."
        
    except Exception as e:
        return f"An error occurred: {e}"
        
