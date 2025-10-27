from flask import Flask, render_template, request
import json
from datetime import datetime

app = Flask(__name__)

def format_date_time(d):
    """Format YYYY-MM-DD -> MM/DD/YYYY; return '' if missing/bad."""
    if not d:
        return ""
    try:
        return datetime.strptime(d, "%Y-%m-%d").strftime("%m/%d/%Y")
    except ValueError:
        return ""

@app.route('/')
def index():
    # === Load JSON data ===
    with open('data/employees.json', encoding='utf-8') as f:
        employees = json.load(f)
    with open('data/keycardentries.json', encoding='utf-8') as f:
        entries = json.load(f)
    with open('data/images.json', encoding='utf-8') as f:
        images = json.load(f)
    with open('data/categories.json', encoding='utf-8') as f:
        categories = json.load(f)

    # === Convert lists to dictionaries ===
    employees_by_keycard = {e["KeyCardId"]: e for e in employees}
    images_by_id = {i["ImageId"]: i for i in images}
    categories_by_id = {c["categoryId"]: c["categoryName"] for c in categories}

    combined_entries = []

    # === Build combined entry data ===
    for entry in entries:
        employee = employees_by_keycard.get(entry["KeyCardId"])
        if not employee:
            continue

        # Entry type name (Entering / Exiting)
        entry_type = categories_by_id.get(entry["EntryCategoryId"], "Unknown")

        # Format event datetime (MM/DD/YYYY HH:MM:SS AM/PM)
        date_time_raw = entry.get("EntryDateTime", "")
        try:
            date_time_obj = datetime.strptime(date_time_raw, "%Y-%m-%dT%H:%M:%SZ")
            formatted_date_time = date_time_obj.strftime("%m/%d/%Y %I:%M:%S %p")
        except ValueError:
            formatted_date_time = date_time_raw or ""

        # Get employee profile image from Base64
        profile_image = images_by_id.get(employee.get("ProfilePictureId"))
        profile_image_src = (
            f"data:image/{profile_image['ImageExtension']};base64,{profile_image['ImageData']}"
            if profile_image else None
        )

        # Security snapshot
        # Attempt to load actual Base64 image, will appear broken because of mock data

        #security_image = images_by_id.get(entry.get("SecurityImageId"))
        #if security_image:
        #    ext = security_image["ImageExtension"].lower()
        #    if ext == "jpg":
        #        ext = "jpeg"
        #    security_image_src = f"data:image/{ext};base64,{security_image['ImageData']}"

        # Security image fallback 
        security_image_src = "/static/images/gray.png"

        # Format birth and start dates
        birth_date = format_date_time(employee.get("BirthDate"))
        start_date = format_date_time(employee.get("StartDate"))

        # Complete access event entry
        combined_entries.append({
            "datetime": formatted_date_time,
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

        # === Sort entries by date/time (latest first) ===
        combined_entries.sort(
            key=lambda e: datetime.strptime(e["datetime"], "%m/%d/%Y %I:%M:%S %p"),
            reverse=True
        )

    # === Filtering logic ===
    search = request.args.get('search', '').strip().lower()
    employee_query = request.args.get('employee', '').strip().lower()

    start_date = request.args.get('start_date', '')       # Request start_date and initialize HHMMSS to min value.
    if(start_date):
        start_date += " 00:00:00"

    end_date = request.args.get('end_date', '')           # Request end_date and initialize HHMMSS to max value.
    if(end_date):
        end_date += " 23:59:59" 


    filtered = combined_entries

    # Global search: match anything visible in the table
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

    # Filter by date range
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

    # === Render the filtered entries ===
    return render_template('index.html', entries=filtered)

if __name__ == '__main__':
    app.run(debug=True)
