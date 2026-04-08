import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# Define the absolute path to your active index.html file
html_file_path = f"file:///{os.path.abspath('index.html').replace(chr(92), '/')}"

@pytest.fixture(scope="module")
def driver():
    # Setup Chrome WebDriver
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless') # Uncomment if you don't want the browser window to open
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    yield driver
    # Teardown
    driver.quit()

def test_form_opens_successfully(driver):
    """Check whether the form page opens successfully."""
    driver.get(html_file_path)
    assert "Student Feedback Registration Form" in driver.title
    # Check if student name input is visible
    name_input = driver.find_element(By.ID, "studentName")
    assert name_input.is_displayed()

def test_leave_mandatory_fields_blank(driver):
    """Leave mandatory fields blank and check error messages."""
    driver.get(html_file_path)
    submit_btn = driver.find_element(By.ID, "submitBtn")
    submit_btn.click()
    
    error_box = driver.find_element(By.ID, "error-message")
    assert error_box.is_displayed()
    
    error_text = error_box.text
    assert "Student Name cannot be empty" in error_text
    assert "Email cannot be empty" in error_text
    assert "Mobile Number cannot be empty" in error_text

def test_invalid_email_format(driver):
    """Enter invalid email format and verify validation."""
    driver.get(html_file_path)
    
    driver.find_element(By.ID, "studentName").send_keys("John Doe")
    driver.find_element(By.ID, "email").send_keys("invalidemail") # Invalid
    driver.find_element(By.ID, "mobile").send_keys("1234567890")
    
    submit_btn = driver.find_element(By.ID, "submitBtn")
    submit_btn.click()
    
    error_box = driver.find_element(By.ID, "error-message")
    assert error_box.is_displayed()
    assert "valid Email ID" in error_box.text

def test_invalid_mobile_number(driver):
    """Enter invalid mobile number and verify validation."""
    driver.get(html_file_path)
    
    driver.find_element(By.ID, "studentName").send_keys("John Doe")
    driver.find_element(By.ID, "email").send_keys("john.doe@example.com")
    driver.find_element(By.ID, "mobile").send_keys("123") # Invalid (not 10 digits)
    
    submit_btn = driver.find_element(By.ID, "submitBtn")
    submit_btn.click()
    
    error_box = driver.find_element(By.ID, "error-message")
    assert error_box.is_displayed()
    assert "10 digits" in error_box.text

def test_dropdown_and_radio_selection(driver):
    """Check whether dropdown selection and radio buttons work properly."""
    driver.get(html_file_path)
    
    # Select Department
    dept_select = driver.find_element(By.ID, "department")
    dept_select.click()
    option = driver.find_element(By.XPATH, "//option[@value='Computer Science']")
    option.click()
    assert dept_select.get_attribute("value") == "Computer Science"

    # Select Gender
    male_radio = driver.find_element(By.ID, "male")
    male_radio.click()
    assert male_radio.is_selected()

def test_reset_button_works(driver):
    """Check whether reset button works correctly."""
    driver.get(html_file_path)
    
    # Fill in some data
    name_input = driver.find_element(By.ID, "studentName")
    name_input.send_keys("Test Resetter")
    
    # Click reset
    reset_btn = driver.find_element(By.ID, "resetBtn")
    reset_btn.click()
    
    # Verify input is cleared
    assert name_input.get_attribute("value") == ""
    
    # Verify error messages are cleared
    error_box = driver.find_element(By.ID, "error-message")
    assert not error_box.is_displayed()

def test_valid_data_successful_submission(driver):
    """Enter valid data and verify successful submission."""
    driver.get(html_file_path)
    
    driver.find_element(By.ID, "studentName").send_keys("Sukhada Bhoyar")
    driver.find_element(By.ID, "email").send_keys("sukhu@gmail.com")
    driver.find_element(By.ID, "mobile").send_keys("1234567890")
    
    dept_select = driver.find_element(By.ID, "department")
    dept_select.send_keys("CSE")

    driver.find_element(By.ID, "female").click()
    
    # Minimum 10 words for feedback
    valid_feedback = "This is a great form that meets all the required validation parameters."
    driver.find_element(By.ID, "comments").send_keys(valid_feedback)
    
    submit_btn = driver.find_element(By.ID, "submitBtn")
    submit_btn.click()
    
    # Error message should not be displayed
    error_box = driver.find_element(By.ID, "error-message")
    assert "block" not in error_box.get_attribute("style") or error_box.text == ""
    
    # Success message should be displayed
    success_box = driver.find_element(By.ID, "success-message")
    assert success_box.is_displayed()
