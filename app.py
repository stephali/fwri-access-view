from flask import Flask, render_template
import json
import os

app = Flask(__name__)

@app.route('/')
def index():
    # Load all JSON data
    with open('data/employees.json') as f:
        employees = json.load(f)
    with open('data/keycardentries.json') as f:
        entries = json.load(f)
    with open('data/images.json') as f:
        images = json.load(f)
    with open('data/categories.json') as f:
        categories = json.load(f)

    # Helper: Convert lists to dictionaries for easy lookup
    employees_by_keycard = {e["KeyCardId"]: e for e in employees}
    images_by_id = {i["ImageId"]: i for i in images}
    categories_by_id = {c["categoryId"]: c["categoryName"] for c in categories}

    # Build a combined list for template
    combined_entries = []
    for entry in entries:
        employee = employees_by_keycard.get(entry["KeyCardId"])
        security_image = images_by_id.get(entry["SecurityImageId"])
        entry_type = categories_by_id.get(entry["EntryCategoryId"], "Unknown")

        if employee and security_image:
            combined_entries.append({
                "datetime": entry["EntryDateTime"],
                "employee_name": f"{employee['FirstName']} {employee['LastName']}",
                "title": employee["WorkTitle"],
                "email": employee["WorkEmail"],
                "keycard_id": employee["KeyCardId"],
                "employee_id": employee["EmployeeId"],
                "scanner_id": entry["ScannerId"],
                "entry_type": entry_type,
                "is_active": "Active" if employee["IsActive"] else "Inactive",
                "profile_pic_id": employee["ProfilePictureId"],
                "security_image_id": entry["SecurityImageId"]
            })

    return render_template('index.html', entries=combined_entries)

if __name__ == '__main__':
    app.run(debug=True)
