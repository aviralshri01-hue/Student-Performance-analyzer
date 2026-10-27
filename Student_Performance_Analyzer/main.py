
import csv
import os
import pandas as pd
import matplotlib.pyplot as plt

FILE_NAME = "students.csv"
students = []


# Calculate grade
def calculate_grade(percentage):
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 50:
        return "D"
    else:
        return "F"


# Load saved student records
def load_students():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                student = {
                    "Name": row["Name"],
                    "Roll No": row["Roll No"],
                    "Python": float(row["Python"]),
                    "DBMS": float(row["DBMS"]),
                    "C++": float(row["C++"]),
                    "Maths": float(row["Maths"]),
                    "Total": float(row["Total"]),
                    "Percentage": float(row["Percentage"]),
                    "Grade": row["Grade"],
                    "Result": row["Result"]
                }

                students.append(student)


# Save student records
def save_students():
    if not students:
        print("No student records to save.")
        return

    with open(FILE_NAME, "w", newline="") as file:
        writer = csv.DictWriter(
            file, fieldnames=students[0].keys()
        )
        writer.writeheader()
        writer.writerows(students)

    print("Student records saved successfully!")


# Add a new student
def add_student():
    print("\n========== ADD STUDENT ==========")

    name = input("Enter student name: ").strip()
    roll_no = input("Enter roll number: ").strip()

    if not name or not roll_no:
        print("Name and roll number cannot be empty.")
        return

    for student in students:
        if student["Roll No"] == roll_no:
            print("This roll number already exists!")
            return

    try:
        python = float(input("Enter Python marks (0-100): "))
        dbms = float(input("Enter DBMS marks (0-100): "))
        cpp = float(input("Enter C++ marks (0-100): "))
        maths = float(input("Enter Maths marks (0-100): "))

        marks = [python, dbms, cpp, maths]

        if any(mark < 0 or mark > 100 for mark in marks):
            print("Marks must be between 0 and 100.")
            return

    except ValueError:
        print("Please enter valid numeric marks.")
        return

    total = sum(marks)
    percentage = total / 4
    grade = calculate_grade(percentage)

    if percentage >= 50:
        result = "PASS"
    else:
        result = "FAIL"

    student = {
        "Name": name,
        "Roll No": roll_no,
        "Python": python,
        "DBMS": dbms,
        "C++": cpp,
        "Maths": maths,
        "Total": total,
        "Percentage": percentage,
        "Grade": grade,
        "Result": result
    }

    students.append(student)
    save_students()

    print("\n========== STUDENT RESULT ==========")
    print("Name:", name)
    print("Roll No:", roll_no)
    print("Total Marks:", total, "/ 400")
    print("Percentage:", round(percentage, 2), "%")
    print("Grade:", grade)
    print("Result:", result)


# Display all students
def view_students():
    print("\n========== ALL STUDENTS ==========")

    if not students:
        print("No student records found.")
        return

    print(
        f"{'Name':<15}{'Roll No':<12}{'Total':<10}"
        f"{'Percentage':<12}{'Grade':<8}{'Result':<10}"
    )
    print("-" * 67)

    for student in students:
        print(
            f"{student['Name']:<15}"
            f"{student['Roll No']:<12}"
            f"{student['Total']:<10.0f}"
            f"{student['Percentage']:<12.2f}"
            f"{student['Grade']:<8}"
            f"{student['Result']:<10}"
        )


# Search student by roll number
def search_student():
    print("\n========== SEARCH STUDENT ==========")
    roll_no = input("Enter roll number: ").strip()

    for student in students:
        if student["Roll No"] == roll_no:
            print("\nStudent Found!")

            for key, value in student.items():
                print(f"{key}: {value}")

            return

    print("Student not found!")


# Class analysis
def class_analysis():
    print("\n========== CLASS ANALYSIS ==========")

    if not students:
        print("No student records available.")
        return

    total_students = len(students)

    average = sum(
        student["Percentage"] for student in students
    ) / total_students

    topper = max(
        students,
        key=lambda student: student["Percentage"]
    )

    passed = sum(
        1 for student in students
        if student["Result"] == "PASS"
    )
    failed = total_students - passed

    print("Total Students:", total_students)
    print("Class Average:", round(average, 2), "%")
    print("Topper:", topper["Name"])
    print("Topper Percentage:", topper["Percentage"], "%")
    print("Students Passed:", passed)
    print("Students Failed:", failed)


# Pandas data analysis
def pandas_analysis():
    print("\n========== PANDAS DATA ANALYSIS ==========")

    if not students:
        print("No student records available.")
        return

    df = pd.DataFrame(students)

    print("\nStudent Data Table:")
    print(df.to_string(index=False))

    subjects = ["Python", "DBMS", "C++", "Maths"]

    print("\n========== SUBJECT AVERAGES ==========")
    print(df[subjects].mean().round(2))

    print("\n========== PERFORMANCE STATISTICS ==========")
    print("Average Percentage:", round(df["Percentage"].mean(), 2), "%")
    print("Highest Percentage:", df["Percentage"].max(), "%")
    print("Lowest Percentage:", df["Percentage"].min(), "%")

    topper_index = df["Percentage"].idxmax()
    print("Topper:", df.loc[topper_index, "Name"])

    print("\n========== RESULT SUMMARY ==========")
    print(df["Result"].value_counts())


# Subject-wise marks bar chart
def subject_marks_chart():
    print("\n========== SUBJECT MARKS CHART ==========")

    if not students:
        print("No student records available.")
        return

    roll_no = input("Enter student roll number: ").strip()

    for student in students:
        if student["Roll No"] == roll_no:
            subjects = ["Python", "DBMS", "C++", "Maths"]
            marks = [
                student["Python"],
                student["DBMS"],
                student["C++"],
                student["Maths"]
            ]

            plt.figure(figsize=(8, 5))
            plt.bar(subjects, marks)
            plt.title("Subject-wise Marks - " + student["Name"])
            plt.xlabel("Subjects")
            plt.ylabel("Marks")
            plt.ylim(0, 100)
            plt.tight_layout()
            plt.show()
            return

    print("Student not found!")


# Student percentage comparison chart
def performance_chart():
    if not students:
        print("No student records available.")
        return

    names = [student["Name"] for student in students]
    percentages = [
        student["Percentage"] for student in students
    ]

    plt.figure(figsize=(8, 5))
    plt.bar(names, percentages)
    plt.title("Student Performance Comparison")
    plt.xlabel("Students")
    plt.ylabel("Percentage")
    plt.ylim(0, 100)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


# Pass and fail pie chart
def result_pie_chart():
    if not students:
        print("No student records available.")
        return

    passed = sum(
        1 for student in students
        if student["Result"] == "PASS"
    )
    failed = sum(
        1 for student in students
        if student["Result"] == "FAIL"
    )

    values = [passed, failed]
    labels = ["Pass", "Fail"]

    if sum(values) == 0:
        print("No results available.")
        return

    plt.figure(figsize=(6, 6))
    plt.pie(
        values,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90
    )
    plt.title("Student Pass and Fail Analysis")
    plt.show()


# Clear all student records
def clear_student_records():
    print("\n========== CLEAR STUDENT RECORDS ==========")

    if not students and not os.path.exists(FILE_NAME):
        print("There are no student records to clear.")
        return

    confirm = input(
        "Delete ALL student records permanently? (yes/no): "
    ).strip().lower()

    if confirm == "yes":
        students.clear()

        fieldnames = [
            "Name", "Roll No", "Python", "DBMS", "C++",
            "Maths", "Total", "Percentage", "Grade", "Result"
        ]

        with open(FILE_NAME, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

        print("All student records have been cleared!")

    else:
        print("Operation cancelled. Student records are safe.")


# Main menu
def main():
    load_students()

    print("Saved student records loaded:", len(students))

    while True:
        print("\n========================================")
        print(" STUDENT RESULT & PERFORMANCE ANALYZER")
        print("========================================")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Search Student")
        print("4. Class Analysis")
        print("5. Pandas Data Analysis")
        print("6. Subject Marks Chart")
        print("7. Student Performance Chart")
        print("8. Pass/Fail Pie Chart")
        print("9. Save Records")
        print("10. Exit")
        print("11. Clear All Student Records")

        choice = input("Enter your choice (1-11): ").strip()

        if choice == "1":
            add_student()

        elif choice == "2":
            view_students()

        elif choice == "3":
            search_student()

        elif choice == "4":
            class_analysis()

        elif choice == "5":
            pandas_analysis()

        elif choice == "6":
            subject_marks_chart()

        elif choice == "7":
            performance_chart()

        elif choice == "8":
            result_pie_chart()

        elif choice == "9":
            save_students()

        elif choice == "10":
            print("Thank you for using the Student Analyzer!")
            break

        elif choice == "11":
            clear_student_records()

        else:
            print("Invalid choice. Please enter a number from 1 to 11.")


if __name__ == "__main__":
    main()
