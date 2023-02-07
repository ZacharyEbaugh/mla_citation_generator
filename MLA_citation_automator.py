from selenium import webdriver
import pyperclip
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

options = Options()
# options.add_argument("--headless")
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36")
driver = webdriver.Chrome(options=options)

# # Open the browser
driver.get("https://www.scribbr.com/citation/generator/mla/")
time.sleep(3)

# Open a new file to write to later on
no_citations = open("./no_citations.txt", "w")

# Open a new file to write correct citations to
correct_citations = open("./correct_citations.txt", "w")

# Loop over file and store all lines in a list
with open("./list_links.txt", "r") as links:
    lines = links.readlines()

# Loop over lines and get the citation
for link in lines:
    # Check if link is blank line, continue
    if link == "\n":
        continue
    # Find the search bar and enter the search term
    search_bar = driver.find_element(by=By.ID, value="autocite-search")
    search_bar.click()
    time.sleep(3)

    # Fill search_bar with the search term
    search_bar.send_keys(link)
    time.sleep(2)

    # Find the search button and click it
    search_button = driver.find_element(by=By.ID, value="autocite-search")
    search_button.submit()
    time.sleep(5)

    # If the citation can load and exists after 5 seconds, get the citation
    try:
        # Find the first result and click it
        first_result = driver.find_element(by=By.XPATH, value="//button[@class = 'button button-md button-high-contrast button-blue']")
        first_result.click()
        time.sleep(5)

        # Find the citation and copy it
        citation = driver.find_element(by=By.XPATH, value="//button[@class = 'button button-sm button-outline button-navy-blue']")
        citation.click()
        time.sleep(3)

        try: 
            # Choose the citation format
            citation_location = driver.find_element(by=By.XPATH, value="//button[@class ='state-checked:border-transparant space-y-4 rounded-lg border p-4 shadow-sm state-checked:bg-blue-5 state-checked:ring-2 state-checked:ring-blue-9 state-unchecked:border-navy-blue-7'][3]")
            citation_location.click()
            time.sleep(1)

            # Copy the citation
            MLAcitation = driver.find_element(by=By.XPATH, value="//button[@class ='button button-md button-solid button-blue']")
            MLAcitation.click()
            time.sleep(2)
        except:
            print("No criteria needed")
            # # Write to correct_citations file
            # correct_citations.write(pyperclip.paste() + "\n")
    except:
        # If the citation can't load, write the link to the file
        no_citations.write(link + "\n\n")
        driver.get("https://www.scribbr.com/citation/generator/mla/")
        time.sleep(3)
        continue
    else:
        # Write to correct_citations file
        correct_citations.write(pyperclip.paste() + "\n\n")
            

# Close the browser
driver.quit()
