import json
from abc import ABC, abstractmethod

from pathlib import Path

database = "school+data.json"
data = {"Student" : [], "Teacher" : []}

if Path(database).exists():
    with open(database, 'r') as f:
        contant = f.read()
        if contant:
            data = json.loads(contant)

def save():
    with open(database, 'w') as f:
        json.dump(data, f, indent=4)

class Person(ABC):

    @abstractmethod
    def get_roles(self):
        pass

    @abstractmethod
    def register(self):
        pass

    @abstractmethod
    def show_details(self):
        pass

    @staticmethod
    def Validate_email(email):
        if "@" in email and "." in email:
            return True
        else:
            return False


class Student(Person):
    def get_roles(self):
        return "Student"
    
    def register(self):
        name = input("Your Name: ")
        age = int(input("Your Age: "))
        email = input("Your Email ID: ")
        parentemail = input("Parents Email ID: ")
        roll_no = int(input("Your Roll No:"))

        if not Person.Validate_email(email):
            print("Student Email ID is invaild")
            return
        
        if not Person.Validate_email(parentemail):
            print("Parent Email ID is in vaild")
            return
        
        for i in data['Student']:
            if i ['roll_no'] == roll_no:
                print("Student already exist")
                return
            
        data['Student'].append({
            "name" : name,
            "age" : age,
            "email" : email,
            "parentemail" : parentemail,
            "roll_no" : roll_no,
            "grades" : {}
        })
        save()

    def show_details(self):
        roll_no = int(input("Enter your roll no: "))
        for s in data["Student"]:
            if s["roll_no"] == roll_no:
                grades = s["grades"]
                avg = sum(grades.values()) / len(grades) if grades else 0

                print(f"\n  Name  : {s['name']}")
                print(f" Roll no : {s['roll_no']}")
                print(f" Grades  : {"grades"}")
                print(f" Average : {avg:.1f}")
                return

    def add_grade(self):
        roll_no = int(input("Enter the roll number: "))
        subject = input("Subject: ")
        marks = float(input("Enter marks: "))

        for i in data['Student']:
            if i["roll_no"] == roll_no:
                i['grades'][subject] = marks
                save()
                print("Grade added successfully")
                return
        print("Student not found")

class Teacher(Person):
    def get_roles(self):
        return "Teacher"
    
    def register(self):
        name = input("Enter your name: ")
        age = int(input("Enter your name: "))
        email = input("Enter your email id: ")
        emp_id = int(input("Enter your employee id: "))
        subject = input("Which subject you teach: ")

        if not Person.Validate_email(email):
            print("Email ID is not vaild")
            return
        
        for e in data['Teacher']:
            if e ['emp_id'] == emp_id:
                print("Employee id is already register")
                return
            
        data['Teacher'].append({
            "name" : name,
            "age" : age,
            "email" : email,
            "emp_id" : emp_id,
            "subject" : subject
        })
        save()

    def show_details(self):
        emp_id = int(input("Enter your employee id: "))

        for t in data["Teacher"]:
            if t['emp_id'] == emp_id:
                print(f"\n Name    : {t['name']}")
                print(f"   Subject : {t['subject']}")
                print(f"   Emp ID  : {t['emp_id']}")
                return
        print("Teacher is not found")


stud = Student()
tec = Teacher()

print("Press 1 to register a Student")
print("Press 2 to register a Teacher")
print("Press 3 to add grades")
print("Press 4 to show student details")
print("Press 5 to show teacher details")

choice = int(input("Please tell me your choice: "))

if choice == 1:
    stud.register()
elif choice == 2:
    tec.register()
elif choice == 3:
    stud.add_grade()
elif choice == 4:
    stud.show_details()
elif choice == 5:
    tec.show_details()