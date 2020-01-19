# Generic
import sys
import argparse
import json
import os
from time import sleep
# Selenium scraper
from selenium.webdriver import Chrome
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select

site = 'https://bankonweb.expressbank.bg/page/default.aspx?user_id=&session_id=&xml_id=/en-US/.login'
download_name = 'report.xml'
report_file_path = '../' + download_name

account_path = "/html/body/form/div[3]/div/div/section[2]/control[2]/div/div[1]/div/table[1]/tbody/tr/td[1]/a"
account_movements = "/html/body/form/div[3]/div/div/section[3]/control/div[3]/div/table/tbody[1]/tr[2]/td/table/tbody/tr[2]/td[7]/a"
montlhy = "/html/body/form/div[3]/div/div/section[3]/control[2]/div/div[2]/control[3]/div/div[1]/table/tbody/tr[1]/td[2]/a[2]"
daily = "/html/body/form/div[3]/div/div/section[3]/control[2]/div/div[2]/control[3]/div/div[1]/table/tbody/tr[1]/td[2]/a[1]"
xml_download = "/html/body/form/div[3]/div/div/section[3]/control[2]/div/div[2]/control[3]/div/div[1]/div[2]/div/ul/li[1]/a"


class Account():

    def __init__(self, download_path, creds):
        self.creds = creds
        self.download_path = download_path
        self.browser = None

    def connect(self):
        options = Options()
        # Check if directory is valid
        prefs = {"download.default_directory": self.download_path}
        options.add_experimental_option("prefs", prefs)

        browser = Chrome(chrome_options=options)
        browser.get(site)

        try:
            login = browser.find_element_by_id('userName')
            login.send_keys(self.creds['user'])
            login = browser.find_element_by_id('pwd')
            login.send_keys(self.creds['pwd'])
        except NoSuchElementException as e:
            print("Can't authenticate")
            browser.quit()

        sleep(1)
        browser.find_element_by_css_selector('button.red').click()
        sleep(1)

        self.browser = browser

    def download_xml_report(self, report_type):
        browser = self.browser
        try:
            # Choose account
            browser.find_element_by_xpath(account_path).click()
            sleep(1)

            # Movements
            # NoSuchElementException
            browser.find_element_by_xpath(account_movements).click()
            sleep(1)

            if report_type is "Monthly":
                ############# Chose Whole month to current date ########################
                browser.find_element_by_xpath(montlhy).click()
                sleep(1)
            elif report_type is "Daily":
                ############# Chose today ########################
                browser.find_element_by_xpath(daily).click()
                sleep(1)
            else:
                print('{} is not a valid report_type. Choose Monthly or Daily!'.format(
                    report_type))

            # Select for page to show all results
            select_all_entries = Select(
                browser.find_element_by_id('Paging_ResultsForPage'))
            select_all_entries.select_by_visible_text('All')
            sleep(1)

            # Download XML
            browser.find_element_by_xpath(xml_download).click()
            sleep(1)
        except NoSuchElementException as e:
            print('Element {} could not be found'.format(e))

    def remove_report(self):
        try:
            os.remove('../{}'.format(download_name))
            print("Report {} removed.".format(download_name))
        except:
            print("Error while deleting file {}".format(filePath))

    def disconnect(self):
        self.browser.quit()
        print('Closed browser session!')


def cmdline_args():
    # Make parser object
    p = argparse.ArgumentParser(description="""
        Get structured account data.
        """,
                                formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    p.add_argument("--creds", type=str, required=True,
                   help="Path to credentials.")
    return(p.parse_args())


if __name__ == "__main__":
    # Check python version
    if sys.version_info < (3, 0, 0):
        sys.stderr.write("You need python 3.0 or later to run this script\n")
        sys.exit(1)

    args = cmdline_args()
    print(args)

    creds = {}
    with open(args.creds, "r+") as c:
        file = c.read()
        creds = json.loads(file[4:])

        acc = Account("/home/mike/code/home_sheets", creds)
        acc.connect()
        acc.download_xml_report("Monthly")
        acc.disconnect()
        acc.remove_report()
