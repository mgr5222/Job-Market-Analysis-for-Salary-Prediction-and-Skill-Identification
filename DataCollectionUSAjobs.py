'''
Data Collection
Use web scraping tools to collect job postings from the mentioned websites.
Extract relevant information such as job title, company, location, required skills, and salary.
'''
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Path to ChromeDriver (Change this if necessary)
# chrome_driver_path = r"C:\Users\mrami\.cache\selenium\chromedriver\win64\134.0.6998.88\chromedriver.exe" # laptop driver location
chrome_driver_path = r"C:\Users\mrami\.cache\selenium\chromedriver\win64\134.0.6998.88\chromedriver.exe"   # desktop driver location
''' 
# If you are unable to find where chromedriver was installed, use this script
driver = webdriver.Chrome()
ChromeDriverLocation = driver.service.path
print(ChromeDriverLocation)
'''



def collectData(url): # test function to open a url with selenium
    # Initialize WebDriver
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service)

    # Test URL
    try:
        driver.get(url)
        
        # Wait until the page loads (waits up to 10 seconds for title or body to load)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Check if relevant keyword appears in title
        if "Software Engineer" in driver.title:  
            print(f"Connection successful! ({url})")
        else:
            print(f"Connection established, but unexpected content. ({url})")

        # Extract job titles (Modify selectors based on website structure)
        jobs = driver.find_elements(By.CSS_SELECTOR, "h2")  # Example selector
        print("\nTop 5 Job Listings:")
        for job in jobs[:5]:  # Print first 5 job listings
            print(job.text)

    except Exception as e:
        print(f"Error scraping {url}: {e}")

    finally:
        driver.quit()  # Close the browser

# scrape data from usajobs.gov
def usaJobsScrape(url):
     # Initialize WebDriver
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service)

    # Test URL
    try:
        driver.get(url)
        
        # Wait until the page loads (waits up to 10 seconds for title or body to load)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Check if relevant keyword appears in title
        if "Software Engineer" in driver.title:  
            print(f"Connection successful! ({url})")
        else:
            print(f"Connection established, but unexpected content. ({url})")

        # Extract job titles (Modify selectors based on website structure)
        # jobs = driver.find_elements(By.CSS_SELECTOR, "h2")  # Example selector
        # print("\nTop 5 Job Listings:")
        # for job in jobs[:5]:  # Print first 5 job listings
        #    print(job.text)
        
        job_titles = driver.find_elements(By.XPATH, '//a[@class="usajobs-search-result--core__title search-joa-link"]')
        for jobs in job_titles:
            print(jobs.text)
        
        job_salaries = driver.find_elements(By.XPATH, '//li[@class="usajobs-search-result--core__item"]')
        for salaries in job_salaries:
            print(salaries.text)

        locations = driver.find_elements(By.XPATH, '//div[@class="usajobs-search-result--core__location"]')
        for local in locations:
            print(local.text)

        companies = driver.find_elements(By.XPATH, '//div[@class="usajobs-search-result--core__department"]')
        for comp in companies:
            print(comp.text)

    except Exception as e:
        print(f"Error scraping {url}: {e}")

    finally:
        driver.quit()  # Close the browser

# Job listing URLs
urls = [
    "https://www.usajobs.gov/Search/Results?k=software%20engineer&p=1",
    "https://www.usajobs.gov/Search/Results?k=software%20engineer&p=2",
    "https://www.usajobs.gov/Search/Results?k=software%20engineer&p=3"
# "https://www.careerbuilder.com/jobs-software-engineer-in-new-york,ny",
# "https://www.usajobs.gov/Search/Results?l=New%20York&k=software%20engineer",
# "https://www.simplyhired.com/search?q=software+engineer&l=New+York%2C+NY"
]

#usaJobsScrape(urls[0])

# Run scraper for each URL
for url in urls:
    print(f"\nScraping: {url}")
    usaJobsScrape(url)
