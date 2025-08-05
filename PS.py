import json

class StudentManagementSystem:
    def __init__(self):
        self.students = {}

    def register_student(self, student_id, name, batch):
        if student_id not in self.students:
            self.students[student_id] = {
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

    def add_term_result(self, student_id, term_name, subject_marks_dict):
        if student_id in self.students:
            if term_name not in self.students[student_id]["terms"]:
                self.students[student_id]["terms"][term_name] = subject_marks_dict
            else:
                print("Term already exists for this student.")
        else:
            print("Student not registered.")

    def update_subject_mark(self, student_id, term, subject, new_mark):
        if student_id in self.students:
            if term in self.students[student_id]["terms"]:
                if subject in self.students[student_id]["terms"][term]:
                    self.students[student_id]["terms"][term][subject] = new_mark
                else:
                    print("Subject not found.")
            else:
                print("Term not found.")
        else:
            print("Student not registered.")

    def record_attendance(self, student_id, present_days, total_days):
        if student_id in self.students:
            self.students[student_id]["attendance"] = {
                "total_days": total_days,
                "present_days": present_days
            }
        else:
            print("Student not registered.")

    def calculate_average(self, student_id):
        if student_id not in self.students:
            print("Student not registered.")
            return 0
        total = count = 0
        for term_marks in self.students[student_id]["terms"].values():
            for mark in term_marks.values():
                total += mark
                count += 1
        return total / count if count else 0

    def calculate_attendance_percentage(self, student_id):
        if student_id in self.students:
            attendance = self.students[student_id]["attendance"]
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

    def get_topper_by_term(self, term):
        topper = None
        max_average = 0
        for student_id, student in self.students.items():
            if term in student["terms"]:
                marks = student["terms"][term]
                average = sum(marks.values()) / len(marks)
                if average > max_average:
                    max_average = average
                    topper = student_id
        return topper

    def rank_students_by_overall_average(self, batch):
        ranking = []
        for student_id, student in self.students.items():
            if student["batch"] == batch:
                avg = self.calculate_average(student_id)
                ranking.append((student_id, student["name"], avg))
        ranking.sort(key=lambda x: x[2], reverse=True)
        return ranking

    def generate_student_report(self, student_id):
        if student_id not in self.students:
            print("Student not registered.")
            return

        student = self.students[student_id]
        print(f"\n--- Report for {student['name']} ({student_id}) ---")
        print(f"Batch: {student['batch']}")
        print(f"Attendance: {self.calculate_attendance_percentage(student_id):.2f}%\n")
        print("Marks:")
        for term, subjects in student["terms"].items():
            print(f"  {term}:")
            for subject, mark in subjects.items():
                print(f"    {subject}: {mark}")
        print(f"\nOverall Average: {self.calculate_average(student_id):.2f}")

    def export_data_to_json(self, filename):
        try:
            with open(filename, "w") as f:
                json.dump(self.students, f)
            print(f"Data exported successfully to '{filename}'")
        except Exception as e:
            print(f" Error exporting data: {e}")

    def import_data_from_json(self, filename):
        try:
            with open(filename, "r") as f:
                self.students = json.load(f)
            print(f"Data imported successfully from '{filename}'")
        except FileNotFoundError:
            print(f"File '{filename}' not found.")
        except json.JSONDecodeError:
            print(f"Error decoding JSON from '{filename}'")

s = StudentManagementSystem()


s.register_student("S1001", "Alice", "2024")
s.register_student("S1002", "Bob", "2024")


s.record_attendance("S1001", 180, 200)


s.add_term_result("S1001", "Term 1", {"Math": 88, "Physics": 92, "English": 81})
s.add_term_result("S1002", "Term 1", {"Math": 85, "Physics": 89, "English": 79})

s.generate_student_report("S1001")


s.export_data_to_json("students_export.json")


s.import_data_from_json("students.json")


ranked = s.rank_students_by_overall_average("2024")
for i, (sid, name, avg) in enumerate(ranked, 1):
    print(f"{i}. {name} ({sid}) - Avg: {avg:.2f}")
