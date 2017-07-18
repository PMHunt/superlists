from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()
    
    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith requests our homepage (locally for now)
        self.browser.get('http://localhost:8000')

        # She checks the page title to confirm it's about to do lists
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test')

# She's invited to enter a to-do item right away

# She types 'buy peacock feathers'

# When she hits enter, the page updates with her new to-do
# '1: Buy peacock feathers' is now a line item in the list

# There is still a text box inviting more to-dos

# <need to elaborate what happens next>

if __name__ == '__main__':
    unittest.main(warnings='ignore')
