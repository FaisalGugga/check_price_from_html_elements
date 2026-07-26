import unittest

from services.check_price_page import extract_price_from_html, normalize_price


class PriceParserTests(unittest.TestCase):
    def test_extracts_amazon_price_from_nested_spans(self):
        html = '<span class="a-price-whole">584<span class="a-price-decimal">.</span></span>'
        self.assertEqual(extract_price_from_html(html), "584")

    def test_detects_bot_check_page(self):
        html = '<html><body><h1>Robot or automated access</h1></body></html>'
        self.assertEqual(extract_price_from_html(html), "Amazon blocked the request or returned a bot-check page.")

    def test_ignores_meta_robots_when_price_input_exists(self):
        html = '<html><head><meta name="robots" content="index,follow"></head><body><input id="twister-plus-price-data-price" type="hidden" value="584"></body></html>'
        self.assertEqual(extract_price_from_html(html), "584")

    def test_normalizes_currency_values(self):
        self.assertEqual(normalize_price("$1,234.56"), 1234.56)
        self.assertEqual(normalize_price("584."), 584.0)

    def test_extracts_price_from_xpath(self):
        html = '<div><span class="price">$12.34</span></div>'
        self.assertEqual(extract_price_from_html(html, xpath='//span[@class="price"]'), "12.34")

    def test_prefers_hidden_price_input_over_xpath_fallback(self):
        html = '<input id="twister-plus-price-data-price" type="hidden" value="584"><div><span class="price">$12.34</span></div>'
        self.assertEqual(extract_price_from_html(html, xpath='//span[@class="price"]'), "584")


if __name__ == "__main__":
    unittest.main()
