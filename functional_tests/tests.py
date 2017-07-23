from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 10
# Functional Tests

class NewVisitorTest(LiveServerTestCase):

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    # helper to enable refactoring
    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    
    def test_can_start_a_list_for_one_user(self):
        # Edith requests our homepage (locally for now)
        self.browser.get(self.live_server_url)

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
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        #there is still a text box allowing her to add more to-dos
        # she enters 'Use peacock feathers to make a fly'
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        #the page updates again and now shows both items on her list
        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')

        # There is still a text box inviting more to-dos
        self.fail('finish the test')

        # <need to elaborate what happens next>

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Edith starts a new list
        ## first bit is simplified version of old test
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # she notices her list has a unique URL, hanging off lists
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        # now Francis, a new user comes along

        ## use a new browser session to make sure none of Edith's info
        ## is there in cookies or session or wherever
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Francis starts a more boring list by entering a new item
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: milk')

        # Francis gets his own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # again, there is no trace of edith's list
        page_text = self.browser.find_element_by_tag_name
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)
        
