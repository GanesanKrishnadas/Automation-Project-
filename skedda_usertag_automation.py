# Imports


import os
import re
import pandas as pd
from playwright.sync_api import sync_playwright

# Constants
EMAIL = "#############" # user id
PASSWORD = "##############" # user password
SLOWMOTION = 100 # login speed
TIMEOUT = 750 # page interaction speed

# Define the directory where downloads will be saved
download_dir = os.path.join(os.getcwd(), 'downloads')

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def on_download(event):
    ensure_directory_exists(download_dir)
    # Save the downloaded file to the specified directory
    event.save_as(os.path.join(download_dir, event.suggested_filename))

# Launch browser
with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False, slow_mo=SLOWMOTION)
    context = browser.new_context()
    page = context.new_page()

    # Set up download event listener
    page.on("download", on_download)
    # Navigate to login page of skedda
    page.goto("https://app.skedda.com/account/login")
    # Locate user email input
    Email_input = page.wait_for_selector("//input[@id='login-email']")
    # Type user email
    Email_input.type(EMAIL)
    # Locate user password input
    Password_input = page.wait_for_selector("//input[@id='login-password']")
    # Type user password
    Password_input.type(PASSWORD)
    # Locate login button
    Login_button = page.wait_for_selector("//button[@type='submit']")
    # Click login button
    Login_button.click()
    # Locate user icon
    User_icon = page.wait_for_selector("//a[@title='Users']")
    # Click user icon
    User_icon.click()
    # Locate export button
    export_button = page.wait_for_selector("//button[@class='btn dropdown-toggle btn-input']")
    # Click export button
    export_button.click()
    # Wait for options 
    page.wait_for_timeout(TIMEOUT)
    # Locate CSV file button
    Csv_button = page.wait_for_selector("button.dropdown-item:has-text('as CSV')")
    # Click csv button
    Csv_button.click()

    # Ensure download completes before closing the browser
    page.wait_for_timeout(TIMEOUT)

    # Wait for the downloaded file to be fully saved
    downloaded_file_path = None
    while not downloaded_file_path or os.path.getsize(downloaded_file_path) == 0:
        page.wait_for_timeout(TIMEOUT)  
        downloaded_file_path = os.path.join(download_dir, os.listdir(download_dir)[0])

    # Once the file is fully downloaded, proceed to read it
    df = pd.read_csv(downloaded_file_path)

    # Iterate through each email address in the DataFrame
    for index, row in df.iterrows():
        # Use regular expression to replace whitespace with an empty string and convert to lowercase
        cleaned_email = re.sub(r'\s', '', row['Email']).lower()
        df.at[index, 'User Email'] = cleaned_email
    
    # Filter users who don't have any tag assigned
    df = df[df['Tags'].isna()]
    
    # Identify user type based on email domain
    def identify_user_type(email):
        if "@student.sl.on.ca" in email:
            return "Student"
        elif "@sl.on.ca" in email:
            return "slc"
        else:
            return "Unknown"
        
    #users_without_tags
    df['User Type'] = df['User Email'].apply(identify_user_type)
    
    # Loop through each user and assign tags
    for index, user in df.iterrows():
        user_type = identify_user_type(user['User Email'])
        if user_type != "Unknown":
            # Click on the user row and then on "Edit user"
            user_row = page.get_by_role("row", name=user['User Email'])
            user_row.get_by_role("button").click()
            page.wait_for_timeout(TIMEOUT)
            page.get_by_role("link", name="Edit user").click()
            page.wait_for_timeout(TIMEOUT)
            
            # Click on "Custom tags" and select appropriate tag
            page.get_by_label("CUSTOM TAGS").click()
            page.get_by_role("checkbox", name=user_type).click()

            # Click on "Save changes" button
            page.get_by_text("Save changes Cancel").click()
            page.get_by_role("button", name="Save changes").click()
            page.wait_for_timeout(TIMEOUT)
            # Update 'Tags' column in DataFrame
            df.at[index, 'Tags'] = "Yes"
    
    # Fill 'No' for users without tags assigned
    df['Tags'].fillna("No")
    
    browser.close()

    # Display the DataFrame with the new column
    print(df)
