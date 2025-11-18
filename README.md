PublicationCleaner

PublicationCleaner is a Ruby on Rails application that allows users to upload their own CSV files and run a custom Python data-cleaning pipeline. It displays the cleaned dataset (head rows) directly in the browser and allows users to download the final processed Excel or CSV result.
The project was created to solve a real-world problem: cleaning large university publication datasets with thousands of entries, removing duplicates, correcting invalid month formats, and organizing the final table into a reliable output.
Features

Upload CSV files through the web interface
Run a Python cleanup script on demand
Avoids automatically running code when the page loads
Produces a cleaned Excel or CSV file for download
Displays the first rows of the cleaned data inside the page
Securely ignores private datasets using .gitignore
Structured MVC separation between Rails controllers, views, and Python scripts
How It Works
The user navigates to the Data page (/data).
A file upload form allows the user to choose a CSV file.
When clicking the "Run Cleaning" button, Rails:
Uploads the CSV to tmp/uploads/
Executes check_publications_cleaning.py via a system call
The Python script reads the uploaded file, performs transformations, and outputs:
A cleaned CSV file
A cleaned Excel file
Rails reads the cleaned CSV and shows the top rows in the browser.
The user can download the full cleaned output.
Installation
Requirements
Ruby on Rails 7+
Python 3.x
Pandas
Mac, Linux, or WSL
Setup
git clone https://github.com/<your_username>/PublicationCleaner.git
cd PublicationCleaner
bundle install
Install Python packages:
pip install pandas openpyxl
Run the Rails server:
bin/rails server
Usage
Visit:
http://localhost:3000/
Go to Data > Upload File
Select a .csv file
Press Run Cleaning
View the sample output table
Download the full cleaned file
Project Structure
app/
  controllers/
    data_controller.rb
  views/
    data/
      index.html.erb
      show.html.erb

python/
  check_publications_cleaning.py

tmp/
  uploads/        # User CSV uploads
  outputs/        # Cleaned result files
.gitignore
This project intentionally ignores sensitive dataset files:
Boo2.csv
publications_audit.xlsx
tmp/uploads/*
tmp/outputs/*
*.pyc
This ensures private university data is never committed to the repository.
Python Script Overview
The script performs the following steps:
Removes exact duplicate rows
Detects and resolves duplicate titles
Normalizes month data or marks corrections when needed
Ensures each title ends with exactly one clean record
Saves a final cleaned dataset as both CSV and XLSX
The script prints warnings or summary results to assist with auditing.
Future Improvements
Add SQL export options
Track cleaning history per user session
Allow multiple scripts to be selected or chained
Add background job execution for large datasets
