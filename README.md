# FWRI Access View

A Python Flask web application created for the Florida Fish and Wildlife Research Institute (FWRI) as part of the Data Administration Analyst written interview.  

The app displays employee facility security access logs, matching each entry with employee headshots and corresponding security camera snapshots.

---

## Features
- View access logs for all employees
- Each log includes date/time, entry type (entering/exiting), and employee details
- Expandable “View” button shows the employee's information and the scanner ID
- Search and filter by employee name, date, type of entry, status
- Active vs inactive employee status indicators
- Runs locally

---

## How to Run

### Step 1 - Download the Project
Option A - Git Clone
```bash
  git clone https://github.com/stephali/fwri-access-view.git
  cd fwri-access-view
```
Option B - Download Zip 
1. Go to the GitHub repository page: https://github.com/stephali/fwri-access-view.git
2. Click the green “Code” button → choose “Download ZIP”.
3. Unzip the file to a folder on your computer.
4. Open that folder in VS Code or another code editor.

### Step 2 - Set Up Python
Make sure you have Python 3.9 or newer installed.

To check, open Command Prompt (Windows) or Terminal (Mac/Linux) and run:
  ``python --version``
  
If Python isn’t installed, download it from https://www.python.org/downloads/   

### Step 3 - Create a Virtual Environment (optional but recommended)
```bash
  python -m venv venv
```
Then activate it:

Windows -
```bash
  venv\Scripts\activate
```
Mac/Linux -
```bash
  source venv/bin/activate
```
### Step 4 -  Install Flask
```bash
  pip install flask
```
### Step 5 -  Run the App
From inside the project folder, run:
```bash
  python app.py
```
You'll see output like:
```bash
Running on http://127.0.0.1:5000
```
Open that link in your web browser, this launches the FWRI Access View Dashboard.
  
