import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# options to keep browser open
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# Path to ChromeDriver (Change this if necessary)
# chrome_driver_path = r"C:\Users\mrami\.cache\selenium\chromedriver\win64\134.0.6998.88\chromedriver.exe" # laptop driver location
chrome_driver_path = r"C:\Users\mrami\.cache\selenium\chromedriver\win64\134.0.6998.88\chromedriver.exe"   # desktop driver location

def simplyScrape(url, choptions):
     # Initialize WebDriver
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=choptions)

    locations = []

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
            
        # scan through 10 pages for final test  
        # REMEBER TO CHANGE THIS VARIABLE  
        for _ in range(3):
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            # create a list of buttons that the website uses
            job_title_buttons = driver.find_elements(By.XPATH, '//a[@class="chakra-button css-1djbb1k"]')
           
            # iterate through buttons to find information about jobs
            for button in job_title_buttons:
                
                button.click()
                time.sleep(1) # give some time for page to load
                location = driver.find_element(By.XPATH, '//div[@data-testid="viewJobCompanyDetailsContainer"]') # retrieves jobs location and company name
                # locations.append(location.text)
                # print(locations)
                Qualifications = driver.find_elements(By.XPATH, '//span[@data-testid="viewJobQualificationItem"]') # retrieve job qualifications

                qualifications_text = [q.text for q in Qualifications]  # Extract text from qualifications
                location_text = location.text  # Extract text from location

                listing = []  
                listing.append((location_text, qualifications_text))  # Append tuple of extracted text

            try:
                
                WebDriverWait(driver, 10).until(
                    EC.visibility_of_all_elements_located((By.TAG_NAME, "aside"))) # wait for job information to appear
                WebDriverWait(driver, 10).until(
                    EC.visibility_of_all_elements_located((By.TAG_NAME, "header"))) # wait for job information to appear
  
            except Exception as e:
                print(f"Could not click Next button: {e}")
                break  # Stop if the button cannot be clicked
        
            # Locate the "Next" button each time before clicking
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//a[@aria-label="Next page"]'))
            )

            next_button.click()
            time.sleep(2)  # Give time for the page to load after clicking


    except Exception as e:
       print(f"Error scraping {url}: {e}")

    finally:
        print(locations)
        #driver.quit()  # Close the browser

url = "https://www.simplyhired.com/search?q=software+engineer&l=New+York%2C+NY"
simplyScrape(url, chrome_options)
