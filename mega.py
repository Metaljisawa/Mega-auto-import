from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



    # Open the Mega.nz website
    driver.get('https://mega.nz/login')

    # Find the email input field, enter your email, and click Next
    email_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[name="login"]')))
    email_input.send_keys(email)
    email_input.submit()

    # Find the password input field, enter your password, and click Login
    password_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[name="password"]')))
    password_input.send_keys(password)
    password_input.submit()

    # Wait for the login process to complete (you may need to adjust the wait time based on your internet connection)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.fm-file-upload input[type="file"]')))

    # Return the driver instance for further use
    return driver

def import_document(driver, file_path):
    # Find the file input field and send the file path
    file_input = driver.find_element(By.CSS_SELECTOR, '.fm-file-upload input[type="file"]')
    file_input.send_keys(file_path)

    # Wait for the file to finish uploading (you may need to adjust the wait time based on your file size and internet connection)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.fm-tree-panel .tranfer-filetype-txt')))

    # Print a success message
    print('Document uploaded successfully!')

    # Close the browser window when finished
    driver.quit()

if __name__ == '__main__':
    # Set your Mega.nz login credentials
    email = 'your@email.com'
    password = 'yourpassword'

    # Set the file path of the document to import
    file_path = '/path/to/document.txt'

    # Log in to Mega.nz
    driver = login_to_mega(email, password)

    # Import the document
    import_document(driver, file_path)
