import unittest
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup

from utils.extract import extract_fashion_data, fetching_content, scrape_fashion

class FashionDataExtractionTests(unittest.TestCase):
    def setUp(self):
        self.sample_html = '''
            <div class="product-details">
                <h3 class="product-title">Unknown Product</h3>
                <div class="price-container"><span class="price">$100.00</span></div>
                <p>Rating: ⭐ Invalid Rating / 5</p>
                <p>5 Colors</p>
                <p>Size: M</p>
                <p>Gender: Men</p>
            </div>
        '''
        self.parsed_html = BeautifulSoup(self.sample_html, 'html.parser')
        self.product_block = self.parsed_html.select_one('div.product-details')

    def test_single_product_extraction(self):
        extracted = extract_fashion_data(self.product_block)
        expected_output = {
            "Title": "Unknown Product",
            "Price": "$100.00",
            "Rating": "Rating: ⭐ Invalid Rating / 5",
            "Colors": "5 Colors",
            "Size": "Size: M",
            "Gender": "Gender: Men"
        }
        self.assertDictEqual(extracted, expected_output)

    @patch("utils.extract.requests.get")
    def test_content_fetching_from_url(self, mock_request):
        html_content = """
        <html>
            <body>
                <div class='product-details'>
                    <h3 class='product-title'>Unknown Product</h3>
                    <div class='price-container'><span class='price'>$100.00</span></div>
                    <p>Rating: ⭐ Invalid Rating / 5</p>
                    <p>5 Colors</p>
                    <p>Size: M</p>
                    <p>Gender: Men</p>
                </div>
            </body>
        </html>
        """
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.content = html_content.encode("utf-8")
        mock_request.return_value = mock_resp

        fetched = fetching_content("https://fashion-studio.dicoding.dev")
        self.assertIn(b"Unknown Product", fetched)

    @patch("utils.extract.fetching_content")
    def test_scraping_multiple_products(self, mocked_fetch_content):
        mocked_fetch_content.return_value = self.sample_html

        scraped_data = scrape_fashion("https://fashion-studio.dicoding.dev")
        self.assertIsInstance(scraped_data, list)
        self.assertTrue(len(scraped_data) >= 1)
        self.assertIn("Title", scraped_data[0])
        self.assertEqual(scraped_data[0]["Title"], "Unknown Product")

if __name__ == "__main__":
    unittest.main()
