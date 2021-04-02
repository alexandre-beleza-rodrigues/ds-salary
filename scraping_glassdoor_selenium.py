from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def get_jobs(keyword, location, num_jobs, verbose, path, slp_time):
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''

    # Initializing the webdriver
    options = webdriver.ChromeOptions()

    # Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    # options.add_argument('headless')

    # Change the path to where chromedriver is in your home folder.
    driver = webdriver.Chrome(executable_path=path, options=options)
    driver.set_window_size(1120, 1000)

    driver.get(
        'https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=&sc.keyword=&locT=&locId=&jobType=')

    # Uses first variable in function to input job title
    search = driver.find_element_by_id("KeywordSearch")
    search.send_keys(keyword)

    # Uses second variable in function to input Location.  Use 'City,State Abbreviation'
    search = driver.find_element_by_id("LocationSearch").clear()
    search = driver.find_element_by_id("LocationSearch")
    search.send_keys(location)
    #search.send_keys(Keys.RETURN)
    driver.find_element_by_id('HeroSearchButton').click()


    # Test for the "Sign Up" prompt and get rid of it.
    time.sleep(slp_time)

    try:
        driver.find_element_by_css_selector("li[data-selected=true]").click()
    except ElementClickInterceptedException:
        pass

    time.sleep(.1)

    try:
        driver.find_element_by_css_selector('[alt="Close"]').click()  # clicking to the X.
    except NoSuchElementException:
        pass

    # changes 'posted' dropdown to 'Last Week'
    #driver.find_element_by_id('filter_fromAge').click()
    #time.sleep(5)
    #driver.find_element_by_xpath('//*[@id="PrimaryDropdown"]/ul/li[4]/span[1]').click()

    jobs = []

    # accepting cookies so they get out of the way when clicking
    driver.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()

    while len(jobs) < num_jobs:  # If true, should be still looking for new jobs.

        # Let the page load. Change this number based on your internet speed.

        time.sleep(5)

        # Going through each job in this page
        job_buttons = driver.find_elements_by_class_name(
            "react-job-listing")  # jl for Job Listing. These are the buttons we're going to click.
        for job_button in job_buttons:

            print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:
                break

            try:
                driver.execute_script("arguments[0].click();", job_button)  # You might
                time.sleep(1)
                collected_successfully = False
            except StaleElementReferenceException:
                print("didn't click the button")
                continue

            while not collected_successfully:
                try:
                    name_n_rating = driver.find_element_by_xpath('//*[@id="JDCol"]/div/article/div/div[1]/div/div/div[1]/div[3]/div[1]/div[1]').text
                    company_name = name_n_rating
                    rating = name_n_rating.split()[-1]
                    location = driver.find_element_by_xpath('//*[@id="JDCol"]/div/article/div/div[1]/div/div/div[1]/div[3]/div[1]/div[3]').text
                    job_title = driver.find_element_by_xpath('//*[@id="JDCol"]/div/article/div/div[1]/div/div/div[1]/div[3]/div[1]/div[2]').text
                    job_description = driver.find_element_by_xpath('.//div[@class="jobDescriptionContent desc"]').text
                    collected_successfully = True
                except:
                    time.sleep(5)

            try:
                salary_estimate = driver.find_element_by_xpath('//*[@id="JDCol"]/div/article/div/div[1]/div/div/div[1]/div[3]/div[1]/div[4]/span').text

            except (NoSuchElementException, StaleElementReferenceException):
                salary_estimate = -1  # You need to set a "not found value. It's important."

            #try:
                #rating = driver.find_element_by_xpath('.//span[@class="rating"]').text
            #except NoSuchElementException:
                #rating = -1  # You need to set a "not found value. It's important."

            # Printing for debugging
            if verbose:
                print("Job Title: {}".format(job_title))
                print("Salary Estimate: {}".format(salary_estimate))
                print("Job Description: {}".format(job_description[:500]))
                print("Rating: {}".format(rating))
                print("Company Name: {}".format(company_name))
                print("Location: {}".format(location))

            # Going to the Company tab...
            # clicking on this:
            # <div class="tab" data-tab-type="overview"><span>Company</span></div>
            try:
                driver.find_element_by_xpath('.//div[@data-item="tab" and @data-test="overview"]').click()


                try:
                    size = driver.find_element_by_xpath(
                        '//*[@id="EmpBasicInfo"]/div[1]/div/div[1]/span[2]').text
                except NoSuchElementException:
                    size = -1

                try:
                    founded = driver.find_element_by_xpath(
                        '//*[@id="EmpBasicInfo"]/div[1]/div/div[2]/span[2]').text
                except NoSuchElementException:
                    founded = -1

                try:
                    type_of_ownership = driver.find_element_by_xpath(
                        '//*[@id="EmpBasicInfo"]/div[1]/div/div[3]/span[2]').text
                except NoSuchElementException:
                    type_of_ownership = -1

                try:
                    industry = driver.find_element_by_xpath(
                        '//*[@id="EmpBasicInfo"]/div[1]/div/div[4]/span[2]').text
                except NoSuchElementException:
                    industry = -1

                try:
                    sector = driver.find_element_by_xpath(
                        '//*[@id="EmpBasicInfo"]/div[1]/div/div[5]/span[2]').text
                except NoSuchElementException:
                    sector = -1

                try:
                    revenue = driver.find_element_by_xpath(
                        '//*[@id="EmpBasicInfo"]/div[1]/div/div[6]/span[2]').text
                except NoSuchElementException:
                    revenue = -1


            except (NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException):  # Some job postings do not have the "Company" tab.
                print("didn't click in 'Company'")
                size = -1
                founded = -1
                type_of_ownership = -1
                industry = -1
                sector = -1
                revenue = -1

            if verbose:
                print("Size: {}".format(size))
                print("Founded: {}".format(founded))
                print("Type of Ownership: {}".format(type_of_ownership))
                print("Industry: {}".format(industry))
                print("Sector: {}".format(sector))
                print("Revenue: {}".format(revenue))
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

            jobs.append({"Job Title": job_title,
                         "Salary Estimate": salary_estimate,
                         "Job Description": job_description,
                         "Rating": rating,
                         "Company Name": company_name,
                         "Location": location,
                         "Size": size,
                         "Founded": founded,
                         "Type of ownership": type_of_ownership,
                         "Industry": industry,
                         "Sector": sector,
                         "Revenue": revenue, })
            # add job to jobs

        # Clicking on the "next page" button
        try:
            driver.find_element_by_xpath('//*[@id="FooterPageNav"]/div/ul/li[7]/a/span').click()
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs,
                                                                                                         len(jobs)))
            break

    return pd.DataFrame(jobs)  # This line converts the dictionary object into a pandas DataFrame.
