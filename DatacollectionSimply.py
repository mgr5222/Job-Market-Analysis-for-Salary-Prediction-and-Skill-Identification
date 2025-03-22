import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configure Chrome options to keep the browser open
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# Path to ChromeDriver (Update if necessary, if driver location unknown, run locateChromeDriver.py)
chrome_driver_path = r"C:\Users\mrami\.cache\selenium\chromedriver\win64\134.0.6998.88\chromedriver.exe"

def scrape_simplyhired_jobs(url, chrome_options, max_pages=40, output_file="job_listings.csv"):
    """Scrapes job listings from SimplyHired and extracts location and qualifications."""
    
    # Initialize WebDriver
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    job_listings = []

    try:
        driver.get(url)

        # Wait for the page to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Verify if the page contains expected content
        if "Software Engineer" in driver.title:
            print(f"Connection successful! ({url})")
        else:
            print(f"Connected, but the content is unexpected. ({url})")

        # Loop through job pages
        for _ in range(max_pages):
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            # Locate job title buttons
            job_buttons = driver.find_elements(By.XPATH, '//a[@class="chakra-button css-1djbb1k"]')

            for button in job_buttons:
                button.click()
                time.sleep(2)  # Allow time for the job details to load

                # Extract job location and company name
                try:
                    location_element = driver.find_element(By.XPATH, '//div[@data-testid="viewJobCompanyDetailsContainer"]')
                    location_text = location_element.text.strip() if location_element.text.strip() else "N/A"
                except Exception:
                    location_text = "N/A"

                # Extract job qualifications
                try:
                    qualifications_elements = driver.find_elements(By.XPATH, '//span[@data-testid="viewJobQualificationItem"]')
                    qualifications_text = [q.text.strip() for q in qualifications_elements if q.text.strip()] or ["N/A"]
                except Exception:
                    qualifications_text = ["N/A"]

                # Extract salary information
                try:
                    salary_element = driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/div/div[2]/div/div/div[2]/div/div/div/aside/div/div[1]/div/div[1]/div')
                    salary_text = salary_element.text.strip() if salary_element.text.strip() else "N/A"
                except Exception:
                    salary_text = "N/A"

                # print(salary_text)

                job_listings.append((button.text, location_text, qualifications_text, salary_text))
                

            try:
                # Wait for job details to be fully loaded
                WebDriverWait(driver, 10).until(
                    EC.visibility_of_all_elements_located((By.TAG_NAME, "aside"))
                )
                WebDriverWait(driver, 10).until(
                    EC.visibility_of_all_elements_located((By.TAG_NAME, "header"))
                )
            except Exception as e:
                print(f"Error while waiting for job details: {e}")
                break  # Stop scraping if page elements do not load properly

            # Locate and click the "Next" button to proceed to the next page
            try:
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//a[@aria-label="Next page"]'))
                )
                next_button.click()
                time.sleep(2)  # Allow time for the page to load after clicking
            except Exception as e:
                print(f"Could not click 'Next' button: {e}")
                break  # Stop if pagination fails

    except Exception as e:
        print(f"Error while scraping {url}: {e}")

    finally:
        # print(job_listings)
        driver.quit()  # Close the browser
        
        # Save results to CSV
        with open(output_file, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Job Title", "Location", "Qualifications", "Salary"])  # Header row
            writer.writerows(job_listings)

        print(f"Scraped data saved to {output_file}")

# Run the scraper
url = "https://www.simplyhired.com/search?q=software+engineer&l=New+York%2C+NY"
scrape_simplyhired_jobs(url, chrome_options)
