## telegram @demoj1234 - DONATES BTC: 19v1h5y5zWH3vMC17gmywsoNSH3AQEbcZs

import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

def set_element_value(driver, element, value):
    driver.execute_script("arguments[0].value = arguments[1];", element, value)

# Function to process the lines and submit the form
def processar_linhas_e_enviar(driver, lines):
    try:
        # Find the text element
        textarea = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "BalanceChecker")))

        # Sets content in text element using JavaScript
        set_element_value(driver, textarea, lines)

        # Find the button and click it
        submit_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "submit")))
        submit_button.click()

        # Wait 3 seconds to get the result
        time.sleep(3)

        # Finds the element that contains the desired result
        result_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.col.col-md-3.pe-0")))

        # Gets the text of the element
        result_text = result_element.text

        # Write text to an output file
        with open("results.txt", "a") as output_file:
            output_file.write(result_text + "\n")

        return True
    except Exception as e:
        print(f"error {e}")
        return False

# Function to move the tested lines to the tested.txt file
def mover_linhas_testadas():
    with open("check.txt", "r") as file:
        all_lines = file.readlines()
    testadas = all_lines[:400]
    restantes = all_lines[400:]
    with open("tested.txt", "a") as file:
        file.writelines(testadas)
    with open("check.txt", "w") as file:
        file.writelines(restantes)

# Chrome CFG
options = Options()

# Initializes the Selenium driver (make sure you have the appropriate WebDriver for your browser installed and in the PATH environment variable)
def main():
    while True:
        driver = webdriver.Chrome(options=options)

        # Open page
        driver.get("https://bitcoindata.science/bitcoin-balance-check")

        # Reads the first 400 lines of the checking.txt file
        with open("check.txt", "r") as file:
            all_lines = file.readlines()
            if not all_lines:
                break
            lines = all_lines[:400]
            content = "".join(lines)
            if processar_linhas_e_enviar(driver, content):
                mover_linhas_testadas()

        # Close chrome
        driver.quit()

if __name__ == "__main__":
    main()
