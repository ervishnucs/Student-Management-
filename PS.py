import json

students = {}

def register_student(student_id, name, batch):
    if student_id not in students:
        students[student_id] = {
            "name": name,
            "batch": batch,
            "attendance": {
                "total_days": 0,
                "present_days": 0
            },
            "terms": {}
        }
    else:
        print("Student already registered.")

def add_term_result(student_id, term_name, subject_marks_dict):
    if student_id in students:
        if term_name not in students[student_id]["terms"]:
            students[student_id]["terms"][term_name] = subject_marks_dict
        else:
            print("Term already exists for this student.")
    else:
        print("Student not registered.")

def update_subject_mark(student_id, term, subject, new_mark):
    if student_id in students:
        if term in students[student_id]["terms"]:
            if subject in students[student_id]["terms"][term]:
                students[student_id]["terms"][term][subject] = new_mark
            else:
                print("Subject not found.")
        else:
            print("Term not found.")
    else:
        print("Student not registered.")

def record_attendance(student_id, present_days, total_days):
    if student_id in students:
        students[student_id]["attendance"] = {
            "total_days": total_days,
            "present_days": present_days
        }
    else:
        print("Student not registered.")

def calculate_average(student_id):
    if student_id not in students:
        print("Student not registered.")
        return 0
    total = count = 0
    for term_marks in students[student_id]["terms"].values():
        for mark in term_marks.values():
            total += mark
            count += 1
    return total / count if count else 0

def calculate_attendance_percentage(student_id):
    if student_id in students:
        attendance = students[student_id]["attendance"]
        total_days = attendance.get("total_days", 0)
        present_days = attendance.get("present_days", 0)
        if total_days > 0:
            return (present_days / total_days) * 100
        else:
            print("Total days cannot be zero.")
            return 0
    else:
        print("Student not registered.")
        return 0

def get_topper_by_term(term):
    topper = None
    max_average = 0
    for student_id, student in students.items():
        if term in student["terms"]:
            marks = student["terms"][term]
            average = sum(marks.values()) / len(marks)
            if average > max_average:
                max_average = average
                topper = student_id
    return topper

def rank_students_by_overall_average(batch):
    ranking = []
    for student_id, student in students.items():
        if student["batch"] == batch:
            avg = calculate_average(student_id)
            ranking.append((student_id, student["name"], avg))
    ranking.sort(key=lambda x: x[2], reverse=True)
    return ranking

def generate_student_report(student_id):
    if student_id not in students:
        print("Student not registered.")
        return

    student = students[student_id]
    print(f"\n--- Report for {student['name']} ({student_id}) ---")
    print(f"Batch: {student['batch']}")
    print(f"Attendance: {calculate_attendance_percentage(student_id):.2f}%\n")
    print("Marks:")
    for term, subjects in student["terms"].items():
        print(f"  {term}:")
        for subject, mark in subjects.items():
            print(f"    {subject}: {mark}")
    print(f"\nOverall Average: {calculate_average(student_id):.2f}")
    print(f"Topper in {student['batch']} for Term 1: {get_topper_by_term('Term 1')}\n")

def export_data_to_json(filename):
    try:
        with open(filename, "w") as f:
            json.dump(students, f)
        print(f"Data exported successfully to '{filename}'")
    except Exception as e:
        print(f"Error exporting data: {e}")

def import_data_from_json(filename):
    global students
    try:
        with open(filename, "r") as f:
            students = json.load(f)
        print(f"Data imported successfully from '{filename}'")
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from '{filename}'")


register_student("S1001", "Alice", "2024")
register_student("S1002", "Bob", "2024")

record_attendance("S1001", 180, 200)

add_term_result("S1001", "Term 1", {"Math": 88, "Physics": 92, "English": 81})
add_term_result("S1002", "Term 1", {"Math": 85, "Physics": 89, "English": 79})

generate_student_report("S1001")

export_data_to_json("students_export.json")
import_data_from_json("students_export.json")

ranked = rank_students_by_overall_average("2024")
for i, (sid, name, avg) in enumerate(ranked, 1):
    print(f"{i}. {name} ({sid}) - Avg: {avg:.2f}")
