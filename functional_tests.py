from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    # helper to enable refactoring
    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    
    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith requests our homepage (locally for now)
        self.browser.get('http://localhost:8000')

        # She checks the page title and header to confirm they're about to do lists
        self.assertIn('To-Do', self.browser.title)
        header_text= self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She's invited to enter a to-do item right away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # She types 'buy peacock feathers'
        inputbox.send_keys('Buy peacock feathers')

        # When she hits enter, the page updates with her new to-do
        # '1: Buy peacock feathers' is now a line item in the list
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        self.check_for_row_in_list_table('1: Buy peacock feathers')

        #there is still a text box allowing her to add more to-dos
        # she enters 'Use peacock feathers to make a fly'
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        #the page updates again and now shows both items on her list
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')

        # There is still a text box inviting more to-dos
        self.fail('finish the test')

        # <need to elaborate what happens next>

if __name__ == '__main__':
    unittest.main(warnings='ignore')
