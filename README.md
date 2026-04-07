# Automation-Project-
Automates the process of user tagging in Skedda using Python and Playwright. Downloads and cleans user data, then assigns tags automatically based on email domains.

📄 Automated User Tagging (Skedda)

🔹 Overview

This project automates user tagging in Skedda using Python and Playwright.
It downloads user data, cleans emails, identifies user types, and assigns tags automatically.
________________________________________
🔹 Tools

•	Python

•	Pandas

•	Playwright
________________________________________
🔹 How it Works

•	Logs into Skedda

•	Downloads users as CSV

•	Cleans email data

•	Finds users without tags

•	Assigns tags based on email:

o	@student.sl.on.ca → Student

o	@sl.on.ca → SLC
________________________________________
🔹 How to Run

1.	Clone the project
https://github.com/GanesanKrishnadas/Automation-Project-.git
2.	Install requirements
pip install pandas playwright
playwright install
3.	Add your login details in the script
EMAIL = "your_email"
PASSWORD = "your_password"
4.	Run the script
python main.py
________________________________________
🔹 Output

•	CSV file downloaded

•	Users automatically tagged



