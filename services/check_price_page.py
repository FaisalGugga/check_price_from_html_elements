import re
import requests
from bs4 import BeautifulSoup

try:
    from selenium.webdriver.common.by import By
except Exception:  # pragma: no cover
    By = None


AMAZON_PRICE_SELECTORS = [
    "#twister-plus-price-data-price",
    "#corePriceDisplay_desktop_feature_div .a-offscreen",
    "#corePrice_feature_div .a-offscreen",
    "#ProductSpecs-1 .a-offscreen",
    "span.a-price .a-offscreen",
    "span.apexPriceToPay .a-offscreen",
    "span.a-price-whole",
    "span.a-price",
]


def _get_text(node):
    if node is None:
        return ""
    text = node.get_text("", strip=True)
    return re.sub(r"\s+", "", text)


def _clean_price_text(raw):
    if not raw:
        return None

    text = str(raw).replace("SAR", "").replace("\xa0", "").strip()
    cleaned = "".join(ch for ch in text if ch.isdigit() or ch == ".")
    if not cleaned:
        return None
    return cleaned


def normalize_price(value):
    if value is None:
        return None

    text = str(value).strip()
    text = text.replace(",", "")
    text = text.replace("$", "")

    if not text:
        return None

    match = re.search(r"(\d+(?:\.\d+)?)", text)
    if not match:
        return None

    return float(match.group(1))


def extract_price_with_selenium(driver):
    if By is None:
        return None

    selectors = [
        (By.XPATH, "//*[@id='twister-plus-price-data-price']", "value"),
        (By.CSS_SELECTOR, "#tp_price_block_total_price_ww .a-offscreen", "text"),
        (By.CSS_SELECTOR, "#ProductSpecs-1 .a-offscreen", "text"),
    ]

    for by, selector, mode in selectors:
        try:
            element = driver.find_element(by, selector)
            raw = element.get_attribute("value") if mode == "value" else element.text
            cleaned = _clean_price_text(raw)
            if cleaned:
                return cleaned
        except Exception:
            continue

    return None


def extract_price_from_html(html, xpath=None):
    soup = BeautifulSoup(html, "html.parser")

    lower_html = html.lower()
    if "captcha" in lower_html or "automated access" in lower_html:
        return "Amazon blocked the request or returned a bot-check page."

    if "robot" in lower_html and "twister-plus-price-data-price" not in lower_html:
        return "Amazon blocked the request or returned a bot-check page."

    price_input = soup.select_one("#twister-plus-price-data-price")
    if price_input:
        value = price_input.get("value")
        if value:
            return value

    visible_price = soup.select_one("#tp_price_block_total_price_ww .a-offscreen")
    if visible_price:
        text = visible_price.get_text(" ", strip=True)
        if re.search(r"\d", text):
            return text

    price_match = re.search(r'(?<!\d)(\d{2,6}(?:\.\d{2})?)(?!\d)', html)
    if price_match:
        return price_match.group(1)

    return "Price element not found."


def check_price_page(url, class_name=None, class_element_type=None, xpath=None):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        if xpath:
            return extract_price_from_html(response.text, xpath=xpath)

        soup = BeautifulSoup(response.text, 'html.parser')

        if class_name and class_element_type:
            price_element = soup.find(class_element_type, class_=class_name)
            if price_element:
                return price_element.get_text(" ", strip=True)

        return extract_price_from_html(response.text)

    except Exception as e:
        return f"An error occurred: {e}"

