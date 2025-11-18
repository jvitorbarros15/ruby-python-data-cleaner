# PublicationCleaner

PublicationCleaner is a Ruby on Rails application that allows users to upload their own CSV files and run a custom Python data-cleaning pipeline. It displays the cleaned dataset (top/head rows) directly in the browser and allows users to download the final processed Excel or CSV result.

The project was created to solve a real-world problem: cleaning large university publication datasets with thousands of entries, removing duplicates, correcting invalid month formats, and organizing the final table into a reliable output.

---

## Features

- Upload CSV files through the web interface  
- Run a Python cleanup script on demand  
- Avoids automatically running code when the page loads  
- Produces a cleaned Excel or CSV file for download  
- Displays the first rows of the cleaned data inside the page  
- Securely ignores private datasets using `.gitignore`  
- Structured MVC separation between Rails controllers, views, and Python scripts  

---

## How It Works

1. The user navigates to the **Data** page (`/data`).  
2. A file upload form allows the user to choose a CSV file.  
3. When clicking **“Run Cleaning”**, Rails:  
   - Uploads the CSV to `tmp/uploads/`  
   - Executes `check_publications_cleaning.py` via a system call  
4. The Python script reads the uploaded file, performs transformations, and outputs:  
   - A cleaned CSV file  
   - A cleaned Excel file  
5. Rails reads the cleaned CSV and shows the top rows in the browser.  
6. The user can download the full cleaned output.

---

## Installation

### Requirements
- Ruby on Rails 7+  
- Python 3.x  
- Pandas  
- macOS, Linux, or WSL

### Setup


git clone https://github.com/jvitorbarros15/ruby-python-data-cleaner.git
cd PYTHONPLS
bundle install
Install Python packages:
pip install pandas openpyxl

Run the Rails server:
bin/rails server

# Usage

1. Visit:  
   **http://localhost:3000/**
2. Go to **Data > Upload File**
3. Select a `.csv` file
4. Press **Run Cleaning**
5. View the sample output table
6. Download the full cleaned file

---

# Project Structure

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
uploads/ # User CSV uploads
outputs/ # Cleaned result files

# .gitignore

This project intentionally ignores sensitive dataset files:

Boo2.csv
publications_audit.xlsx
tmp/uploads/*
tmp/outputs/*
*.pyc

This ensures private university data is never committed to the repository.

---

# Python Script Overview

The cleaning pipeline performs:

- Removal of exact duplicate rows  
- Detection and resolution of duplicate titles  
- Normalization of month data or marking corrections when needed  
- Guarantee that each title ends with exactly one clean record  
- Saving a final cleaned dataset as both CSV and XLSX  
- Printing warnings or summary results for auditing

# Next Steps

- Allow users to upload their own datasets (multiple files, version history, and preview before processing)  
- Improve CSS styling for a cleaner, more professional UI and better table visualization  
- Let users choose what cleaning or filtering operations they want to apply (duplicate removal, month normalization, title conflict resolution, column selection, custom rules, etc.) 
