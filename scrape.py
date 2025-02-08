from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup

def scrape_website_chromedriver(website):
    """
    Scrapes the HTML content from a given website using Chrome WebDriver.
    
    Args:
        website (str): The URL of the website to scrape.
        
    Returns:
        str: The HTML source code of the webpage.
    """
    print("Launching chrome browser")
    chrome_driver_path = "./chromedriver"
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=ChromeService(chrome_driver_path), options=options)
    
    try:
        driver.get(website)
        print("Page Loaded...")
        html = driver.page_source
        time.sleep(10)
        
        return html
    
    finally:
        driver.quit()
      
      
def scrape_website(website):
    """
    Scrapes the HTML content from a given website using Selenium's built-in driver management.
    """
    print("Launching Chrome browser")
    
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-gpu")  # For better stability

    driver = webdriver.Chrome(service=ChromeService(), options=options)
    
    try:
        driver.get(website)
        print("Page Loaded...")
        html = driver.page_source
        return html
    finally:
        driver.quit()
          
def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    body_content = soup.find('body')
    if body_content:
        return str(body_content)
    return ""

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, 'html.parser')
    
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()
        
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )
    
    return cleaned_content

def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]
    
    
    
    