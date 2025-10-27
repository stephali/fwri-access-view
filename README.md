# FWRI Access View

A Python Flask web application created for the Florida Fish and Wildlife Research Institute (FWRI), a division of the Florida Fish and Wildlife Conservation Commission (FWC), as part of the Data Administration Analyst written interview.  

The app provides a clear, visual overview of employee facility access logs, linking each entry to the corresponding staff profile and security camera snapshot.

---

## Features
- Displays access logs for all employees  
- Access events are shown in chronological order (latest → oldest)  
- Each record includes security snapshots, employee profile pictures, date/time, entry type (entering or exiting), and employee details  
- Expandable "View" button reveals the employee’s full profile information and scanner ID  
- Search and filter by employee name, date range, entry type, or status  
- Highlights active vs. inactive employees for quick identification  
- Runs locally - no database or internet connection required  


---

## How to Run

### Step 1 - Download the Project
*Option A* - Git Clone
```bash
git clone https://github.com/stephali/fwri-access-view.git
cd fwri-access-view
```
*Option B* - Download Zip 
1. Go to the GitHub repository page: https://github.com/stephali/fwri-access-view.git
2. Click the green “Code” button → choose “Download ZIP”.
3. Unzip the file to a folder on your computer.
4. Open that folder in VS Code or another code editor.

### Step 2 - Set Up Python
Make sure you have Python 3.9 or newer installed.

To check, open Command Prompt (Windows) or Terminal (Mac/Linux) and run:
  ``python --version``
  
If Python isn’t installed, download it from https://www.python.org/downloads/   

### Step 3 -  Install Flask
This app only requires Flask.  

You can install it by running:
```bash
pip install flask
```
### Step 4 -  Run the App
From inside the project folder, run:
```bash
python app.py
```
You'll see output like:
```bash
Running on http://127.0.0.1:5000
```
Open that link in your web browser, this launches the FWRI Access View Dashboard.


*Note: This repository is shared for review purposes only and contains no sensitive or production data.*
