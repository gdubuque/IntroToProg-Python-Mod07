# ------------------------------------------------------------------------------------------ #
# Title: Assignment07
# Desc: This assignment demonstrates using data classes with structured error handling
# Change Log: (Who, When, What)
#   R.Root, 2030/01/01/, Created Script
#   G.DuBuque, 2024/08/12, Updated Script for Assignment 07, added Data classes
#                          Person and Student
# ------------------------------------------------------------------------------------------ #
import json

# Data --------------------------------------------------------------------- #
# Define the global Constants (GD)
MENU: str = '''
---- Course Registration Program ----
  Select from the following menu:  
    1. Register a Student for a Course.
    2. Show current data.  
    3. Save data to a file.
    4. Exit the program.
----------------------------------------- 
'''
FILE_NAME: str = "Enrollments.json"

# Define the global Variables (GD)
students: list = []     # List of Student objects (GD)
menu_choice: str = ''   # Hold the choice made by the user.


# Data Classes-------------------------------------------------------------- #
class Person:
    """
    A data class to represent a person.

    Properties:
    first_name (str): The person's first name.
    last_name (str): The person's last name.

    ChangeLog: (Who, When, What)
    G.DuBuque, 2024/08/12, Created Class
    """
    def __init__(self, first_name: str = '', last_name: str = ''):
        self.first_name = first_name
        self.last_name = last_name

    @property
    def first_name(self):
        return self.__first_name.title()    # Optionally format as title case (GD)

    @first_name.setter
    def first_name(self, value: str):
        if value.isalpha() or value == '':  # Check for format errors (GD)
            self.__first_name = value
        else:
            raise ValueError('First name must not contain numbers.')

    @property
    def last_name(self):
        return self.__last_name.title()  # Optionally format as title case (GD)

    @last_name.setter
    def last_name(self, value: str):
        if value.isalpha() or value == '':  # Check for format errors (GD)
            self.__last_name = value
        else:
            raise ValueError('Last name must not contain numbers.')

    def __str__(self):
        """
        :return: The Person's attributes in a CSV string
        """
        return f'{self.first_name},{self.last_name}'


class Student(Person):
    """
    A data class to represent a Student. Inherits from Person.

    Properties:
    first_name (str): The student's first name.
    last_name (str): The student's last name.
    course_name (str): The course name the student is registered for.

    ChangeLog: (Who, When, What)
    G.DuBuque, 2024/08/12, Created Class
    """

    def __init__(self, first_name: str = '', last_name: str = '', course_name: str = ''):
        super().__init__(first_name, last_name)
        self.course_name = course_name

    @property
    def course_name(self):
        return self.__course_name.title()   # Optionally format as title case (GD)

    @course_name.setter
    def course_name(self, value: str):
        value_list = value.split()  # Slit course name into title and number (GD)
        # Check for format errors, must be in the form of "Name Number" (GD)
        if len(value_list) == 2 and value_list[0].isalpha() and value_list[1].isnumeric():
            self.__course_name = value
        else:
            raise ValueError("Course name must be in the form of 'Name Number'")

    def __str__(self):
        """
        return: The Student's attributes in a CSV string
        """
        return f'{super().__str__()},{self.course_name}'

    def get_data_dict(self):
        """
        return: The Student's attributes in a dictionary.
        For working with JSON data.
        """
        return {"FirstName": self.first_name, "LastName": self.last_name, "CourseName": self.course_name}


# Processing --------------------------------------------------------------- #
class FileProcessor:
    """
    A collection of processing layer functions that work with Json files

    ChangeLog: (Who, When, What)
    R.Root, 2030/01/01, Created Class
    G.DuBuque, 2024/08/12, Updated Class to use the Student data Class,
                            the students list is now a list of Student objects.
    """
    @staticmethod
    def read_data_from_file(file_name: str, student_data: list):
        """ This function reads data from a json file and loads it into a list of Student objects

        ChangeLog: (Who, When, What)
        R.Root, 2030/01/01, Created function
        G.DuBuque, 2024/08/12, Updated function to use a list of Student objects

        :param file_name: string data with name of file to read from
        :param student_data: list of Student objects created from JSON file data (GD)

        :return: list of Student objects (GD)
        """

        try:
            file = open(file_name, "r")
            student_json_data = json.load(file)
            file.close()

            # For each student in the JSON list, create a Student object from the JSON data
            # and add the Student object to the students list. (GD)
            for student in student_json_data:
                student_data.append(Student(student['FirstName'],
                                            student['LastName'],
                                            student['CourseName']))

        except ValueError as e:     # Check for Value Errors when creating Student objects (GD)
            IO.output_error_messages("There was a problem with the format of the data!", e)
        except FileNotFoundError as e:  # Added file check (GD)
            IO.output_error_messages("Text file must exist before running this script!", e)
        except Exception as e:
            IO.output_error_messages(message="Error: There was a problem with reading the file.", error=e)

        finally:
            if not file.closed:
                file.close()
        return student_data

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list):
        """ This function writes data to a json file with data from a list of Student objects

        ChangeLog: (Who, When, What)
        R.Root, 2030/01/01, Created function
        G.DuBuque, 2024/08/12, Updated function to use a list of Student objects

        :param file_name: string data with name of file to write to
        :param student_data: list of Student objects to write data to JSON file (GD)

        :return: None
        """

        try:
            student_json_data: list = []    # Temporary list of student JSON data (GD)
            # Get the dictionary data from each Student object in the list and add it
            # to the JSON list (GD)
            for student in student_data:
                student_json_data.append(student.get_data_dict())

            file = open(file_name, "w")
            json.dump(student_json_data, file)
            file.close()
            print("The following data was saved to the file!")
            IO.output_student_and_course_names(student_data=student_data)
        except Exception as e:
            message = "Error: There was a problem with writing to the file.\n"
            message += "Please check that the file is not open by another program."
            IO.output_error_messages(message=message, error=e)
        finally:
            if not file.closed:
                file.close()


# Presentation ------------------------------------------------------------- #
class IO:
    """
    A collection of presentation layer functions that manage user input and output

    ChangeLog: (Who, When, What)
    R.Root, 2030/01/01, Created function
    G.DuBuque, 2024/08/12, Updated Class methods to use a list of Student objects

    """

    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        """ This function displays a custom error messages to the user

        ChangeLog: (Who, When, What)
        R.Root, 2030/01/01, Created function

        :param message: string with message data to display
        :param error: Exception object with technical message to display

        :return: None
        """
        print(message, end="\n\n")
        if error is not None:
            print("-- Technical Error Message -- ")
            print(error, error.__doc__, type(error), sep='\n')

    @staticmethod
    def output_menu(menu: str):
        """ This function displays the menu of choices to the user

        ChangeLog: (Who, When, What)
        R.Root, 2030/01/01, Created function
        G.DuBuque, 2034/08/12, Removed extra lines

        :return: None
        """

        print(menu)

    @staticmethod
    def input_menu_choice():
        """ This function gets a menu choice from the user

        ChangeLog: (Who, When, What)
        R.Root, 2030/01/01, Created function

        :return: string with the users choice
        """
        choice = "0"
        try:
            choice = input("Enter your menu choice number: ")
            if choice not in ("1", "2", "3", "4"):  # Note these are strings
                raise Exception("Please, choose only 1, 2, 3, or 4")
        except Exception as e:
            IO.output_error_messages(e.__str__())  # Not passing e to avoid the technical message

        return choice

    @staticmethod
    def output_student_and_course_names(student_data: list):
        """ This function displays the student and course names to the user

        ChangeLog: (Who, When, What)
        R.Root, 2030/01/01, Created function
        G.DuBuque, 2024/08/12, Updated function to use a list of Student objects

        :param student_data: list of Student objects (GD)

        :return: None
        """

        print("-" * 50)
        for student in student_data:
            print(f'Student {student.first_name} {student.last_name} '
                  f'is enrolled in {student.course_name}')
        print("-" * 50)

    @staticmethod
    def input_student_data(student_data: list):
        """ This function gets the student's first name and last name, with a course name from the user

        ChangeLog: (Who, When, What)
        R.Root, 2030/01/01, Created function
        G.DuBuque, 2024/08/12, Updated function to use a list of Student objects

        :param student_data: list of Student objects (GD)

        :return: list of Student objects (GD)
        """

        try:
            student_first_name = input("Enter the student's first name: ")
            student_last_name = input("Enter the student's last name: ")
            course_name = input("Please enter the name of the course: ")

            student = Student(student_first_name, student_last_name, course_name)

            student_data.append(student)
            print()
            print(f"You have registered {student.first_name} {student.last_name} for {student.course_name}.")
        except ValueError as e:  # Check for Value Errors when creating Student objects (GD)
            IO.output_error_messages("There was a problem with the format of the data!", e)
        except Exception as e:
            IO.output_error_messages(message="Error: There was a problem with your entered data.", error=e)
        return student_data


# Main body of script ------------------------------------------------------ #

# When the program starts, read the file data into a list of Student objects (GD)
# Extract the data from the file
students = FileProcessor.read_data_from_file(file_name=FILE_NAME, student_data=students)

# Present and Process the data
while True:
    IO.output_menu(menu=MENU)   # Present the menu of choices

    menu_choice = IO.input_menu_choice()    # Get menu choice

    if menu_choice == "1":  # Input user data
        students = IO.input_student_data(student_data=students)
        continue

    elif menu_choice == "2":    # Present the current data
        IO.output_student_and_course_names(students)
        continue

    elif menu_choice == "3":    # Save the data to a file
        FileProcessor.write_data_to_file(file_name=FILE_NAME, student_data=students)
        continue

    elif menu_choice == "4":    # Stop the program
        break  # out of the loop

print("Program Ended")
