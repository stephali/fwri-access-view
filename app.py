from flask import Flask, render_template, request
import json
from datetime import datetime

app = Flask(__name__)

def fmt_iso_date(d):
    """Format YYYY-MM-DD -> MM/DD/YYYY; return '' if missing/bad."""
    if not d:
        return ""
    try:
        return datetime.strptime(d, "%Y-%m-%d").strftime("%m/%d/%Y")
    except ValueError:
        return ""

@app.route('/')
def index():
    # === LOAD JSON DATA ===
    with open('data/employees.json', encoding='utf-8') as f:
        employees = json.load(f)
    with open('data/keycardentries.json', encoding='utf-8') as f:
        entries = json.load(f)
    with open('data/images.json', encoding='utf-8') as f:
        images = json.load(f)
    with open('data/categories.json', encoding='utf-8') as f:
        categories = json.load(f)

    # === CONVERT LISTS TO DICTIONARIES ===
    employees_by_keycard = {e["KeyCardId"]: e for e in employees}
    images_by_id = {i["ImageId"]: i for i in images}
    categories_by_id = {c["categoryId"]: c["categoryName"] for c in categories}

    combined_entries = []

    # === BUILD COMBINED ENTRY DATA ===
    for entry in entries:
        employee = employees_by_keycard.get(entry["KeyCardId"])
        if not employee:
            continue

        # Entry type name (Entering / Exiting)
        entry_type = categories_by_id.get(entry["EntryCategoryId"], "Unknown")

        # Format event datetime (MM/DD/YYYY HH:MM:SS AM/PM)
        dt_raw = entry.get("EntryDateTime", "")
        try:
            dt_obj = datetime.strptime(dt_raw, "%Y-%m-%dT%H:%M:%SZ")
            formatted_dt = dt_obj.strftime("%m/%d/%Y %I:%M:%S %p")
        except ValueError:
            formatted_dt = dt_raw or ""

        # Get employee profile image from Base64
        profile_img = images_by_id.get(employee.get("ProfilePictureId"))
        profile_image_src = (
            f"data:image/{profile_img['ImageExtension']};base64,{profile_img['ImageData']}"
            if profile_img else None
        )

        # Fallback for security snapshot
        security_image_src = "/static/images/gray.png"

        # Format birth and start dates
        birth_date = fmt_iso_date(employee.get("BirthDate"))
        start_date = fmt_iso_date(employee.get("StartDate"))

        combined_entries.append({
            "datetime": formatted_dt,
            "employee_name": f"{employee.get('FirstName', '')} {employee.get('LastName', '')}",
            "title": employee.get("WorkTitle", ""),
            "email": employee.get("WorkEmail", ""),
            "birth_date": birth_date,
            "start_date": start_date,
            "keycard_id": employee.get("KeyCardId", ""),
            "employee_id": employee.get("EmployeeId", ""),
            "scanner_id": entry.get("ScannerId", ""),
            "entry_type": entry_type,
            "is_active": "Active" if employee.get("IsActive") else "Inactive",
            "profile_image_src": profile_image_src,
            "security_image_src": security_image_src
        })

        # === SORT ENTRIES BY DATE/TIME (LATEST FIRST) ===
        combined_entries.sort(
            key=lambda e: datetime.strptime(e["datetime"], "%m/%d/%Y %I:%M:%S %p"),
            reverse=True
        )

    # === FILTERING LOGIC ===
    search = request.args.get('search', '').strip().lower()
    employee_query = request.args.get('employee', '').strip().lower()
    
    start_date = request.args.get('start_date', '')       # Request start_date and initialize HHMMSS to min value.
    if(start_date):
        start_date += " 00:00:00"

    end_date = request.args.get('end_date', '')         # Request end_date and initialize HHMMSS to max value.
    if(end_date):
        end_date += " 23:59:59" 


    filtered = combined_entries

    # 1️⃣ Global search: match anything visible in the table
    if search:
        filtered = [
            e for e in filtered
            if search in e['employee_name'].lower()
            or search in e['email'].lower()
            or search in e['title'].lower()
            or search in e['datetime'].lower()
            or search in e['entry_type'].lower()
            or search in e['is_active'].lower()
            or search in e['scanner_id'].lower()
            or search in e['keycard_id'].lower()
        ]


    # 2️⃣ Filter by employee name
    if employee_query:
        filtered = [
            e for e in filtered
            if employee_query in e['employee_name'].lower()
        ]

    # 3️⃣ Filter by date range
    if start_date or end_date:
        def to_dt(s):
            try:
                return datetime.strptime(s, "%m/%d/%Y %I:%M:%S %p")
            except:
                return None

        start_dt = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S") if start_date else None
        end_dt = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S") if end_date else None

        tempList = []
        for element in filtered:
            tempDate = to_dt(element['datetime'])
            if (tempDate and (tempDate >= start_dt) and (tempDate <= end_dt)):
                tempList.append(element)

        filtered = tempList

    # === RENDER THE FILTERED ENTRIES ===
    return render_template('index.html', entries=filtered)

if __name__ == '__main__':
    app.run(debug=True)
