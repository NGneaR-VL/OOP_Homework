from functools import total_ordering


@total_ordering
class Student:
    """Represents a student who studies courses, receives grades for homework,
    and can rate lectures given by lecturers.
    """
    def __init__(self, name, surname, gender):
        """Initialize a student with name, surname, and gender.
        
        Args:
            name (str): Student's first name.
            surname (str): Student's last name.
            gender (str): Student's gender.
        """
        self.__name = name
        self.__surname = surname
        self.__gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def __str__(self):
        """Return a formatted string with student's information."""
        return f"Имя: {self.__name}\
            \nФамилия: {self.__surname}\
            \nСредняя оценка за домашние задания: {own_average_grade(self.grades)}\
            \nКурсы в процессе изучения: {', '.join(self.courses_in_progress)}\
            \nЗавершенные курсы: {', '.join(self.finished_courses)}"

    def __eq__(self, other):
        """Compare two students by their average grade for equality."""
        if not isinstance(other, Student):
            return "COMPARE ERROR"
        return own_average_grade(self.grades) == own_average_grade(other.grades)

    def __lt__(self, other):
        """Compare two students by their average grade for less than."""
        if not isinstance(other, Student):
            return "COMPARE ERROR"
        return own_average_grade(self.grades) < own_average_grade(other.grades)

    @property
    def name(self):
        """Get the student's first name (read-only)."""
        return self.__name

    @property
    def surname(self):
        """Get the student's last name (read-only)."""
        return self.__surname

    @property
    def gender(self):
        """Get the student's gender (read-only)."""
        return self.__gender

    def add_finished_course(self, course):
        """Add a course to the list of finished courses.
        
        Args:
            course (str): Name of the course.
        
        Returns:
            str: Error message if course already exists, otherwise None.
        """
        if course not in self.finished_courses:
            self.finished_courses.append(course)
        else:
            return "add_finished_course ERROR"

    def add_courses_in_progress(self, course):
        """Add a course to the list of courses in progress.
        
        Args:
            course (str): Name of the course.
        
        Returns:
            str: Error message if course already exists, otherwise None.
        """
        if course not in self.courses_in_progress:
            self.courses_in_progress.append(course)
        else:
            return "add_courses_in_progress ERROR"

    def rate_lecture(self, lecturer, course, grade):
        """Rate a lecture given by a lecturer for a specific course.
        
        Args:
            lecturer (Lecturer): The lecturer to rate.
            course (str): The course name.
            grade (int): Rating from 0 to 10.
        
        Returns:
            str: Error message if validation fails, otherwise None.
        """
        if (isinstance(lecturer, Lecturer) and
            course in lecturer.courses_attached and
            course in self.courses_in_progress and
            0 <= grade <= 10):
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'ERROR!'


class Mentor:
    """Base class for mentors (lecturers and reviewers)."""

    def __init__(self, name, surname):
        """Initialize a mentor with name and surname.
        
        Args:
            name (str): Mentor's first name.
            surname (str): Mentor's last name.
        """
        self.__name = name
        self.__surname = surname
        self.courses_attached = []

    def mentor_add_course(self, course):
        """Add a course to the mentor's list of attached courses.
        
        Args:
            course (str): Name of the course.
        
        Returns:
            str: Error message if course already exists, otherwise None.
        """
        if course not in self.courses_attached:
            self.courses_attached.append(course)
        else:
            return "mentor_add_course ERROR"

    @property
    def name(self):
        """Get the mentor's first name (read-only)."""
        return self.__name

    @property
    def surname(self):
        """Get the mentor's last name (read-only)."""
        return self.__surname


@total_ordering
class Lecturer(Mentor):
    """Represents a lecturer who gives lectures and receives grades from students."""

    def __init__(self, name, surname):
        """Initialize a lecturer with name and surname.
        
        Args:
            name (str): Lecturer's first name.
            surname (str): Lecturer's last name.
        """
        super().__init__(name, surname)
        self.grades = {}

    def __str__(self):
        """Return a formatted string with lecturer's information."""
        return f"Имя: {self.name}\
            \nФамилия: {self.surname}\
            \nСредняя оценка за лекции: {own_average_grade(self.grades)}"

    def __eq__(self, other):
        """Compare two lecturers by their average grade for equality."""
        if not isinstance(other, Lecturer):
            return "COMPARE ERROR"
        return own_average_grade(self.grades) == own_average_grade(other.grades)

    def __lt__(self, other):
        """Compare two lecturers by their average grade for less than."""
        if not isinstance(other, Lecturer):
            return "COMPARE ERROR"
        return own_average_grade(self.grades) < own_average_grade(other.grades)


class Reviewer(Mentor):
    """Represents a reviewer who grades students' homework."""

    def __str__(self):
        """Return a formatted string with reviewer's information."""
        return f"Имя: {self.name}\
            \nФамилия: {self.surname}"

    def rate_hw(self, student, course, grade):
        """Rate a student's homework for a given course.
        
        Args:
            student (Student): The student to grade.
            course (str): The course name.
            grade (int): Rating (presumably 0-10, but no check here).
        
        Returns:
            str: Error message if validation fails, otherwise None.
        """
        if (isinstance(student, Student) and
            course in self.courses_attached and
            course in student.courses_in_progress):
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'rate_hw function ERROR'


def own_average_grade(grades_dict):
    """Calculate the average grade from a dictionary of course-grade lists.
    
    Args:
        grades_dict (dict): Keys are course names, values are lists of grades.
    
    Returns:
        float: Average of all grades, or 0 if no grades exist.
    """
    all_grades = []
    for grades_list in grades_dict.values():
        all_grades.extend(grades_list)

    if all_grades:
        return (sum(all_grades) / len(all_grades))
    else:
        return 0


def students_average_grade(students_list, course):
    """Calculate the average grade for a specific course across a list of students.
    
    Args:
        students_list (list of Student): List of student objects.
        course (str): The course name.
    
    Returns:
        float: Average grade for that course, or 0.0 if no grades.
    """
    all_grades = []
    for student in students_list:
        if course in student.grades:
            all_grades.extend(student.grades[course])
    if all_grades:
        return sum(all_grades) / len(all_grades)
    else:
        return 0.0


def mentors_average_grade(lecturers_list, course):
    """Calculate the average grade for a specific course across a list of lecturers.
    
    Args:
        lecturers_list (list of Lecturer): List of lecturer objects.
        course (str): The course name.
    
    Returns:
        float: Average grade for that course, or 0.0 if no grades.
    """
    all_grades = []
    for lecturer in lecturers_list:
        if course in lecturer.grades:
            all_grades.extend(lecturer.grades[course])
    if all_grades:
        return sum(all_grades) / len(all_grades)
    else:
        return 0.0
    

if __name__ == "__main__":
    # Создаём студентов
    student1 = Student("Иван", "Иванов", "М")
    student2 = Student("Пётр", "Петров", "М")
    student1.add_courses_in_progress("Python")
    student1.add_courses_in_progress("JavaScript")
    student2.add_courses_in_progress("Python")
    student2.add_courses_in_progress("GIT")
    student1.add_finished_course("GIT")
    student2.add_finished_course("JavaScript")

    # Создаём лекторов
    lecturer1 = Lecturer("Олег", "Булыгин")
    lecturer2 = Lecturer("Тимур", "Анвартдинов")
    lecturer1.mentor_add_course("Python")
    lecturer1.mentor_add_course("C++")
    lecturer2.mentor_add_course("Python")
    lecturer2.mentor_add_course("JavaScript")
    
    # Создаём экспертов
    reviewer1 = Reviewer("Владимир", "Смирнов")
    reviewer2 = Reviewer("Елена", "Сидорова")
    reviewer1.mentor_add_course("Python")
    reviewer1.mentor_add_course("JavaScript")
    reviewer2.mentor_add_course("Python")
    reviewer2.mentor_add_course("GIT")

    # Эксперты ставят оценки студентам
    reviewer1.rate_hw(student1, "Python", 9)
    reviewer1.rate_hw(student1, "JavaScript", 10)
    reviewer2.rate_hw(student2, "Python", 8)
    reviewer2.rate_hw(student2, "GIT", 9)

    # Студенты оценивают лекторов
    student1.rate_lecture(lecturer1, "Python", 8)
    student1.rate_lecture(lecturer1, "C++", 7)
    student2.rate_lecture(lecturer2, "Python", 10)
    student2.rate_lecture(lecturer2, "JavaScript", 9)

    # Выводим информацию
    print("\U0001F4BB === Студенты ===")
    print(student1, "\n")
    print(student2, "\n")

    print("\U0001F4BB === Лекторы ===")
    print(lecturer1, "\n")
    print(lecturer2, "\n")

    print("\U0001F4BB === Ревьюверы ===")
    print(reviewer1, "\n")
    print(reviewer2, "\n")

    # Сравнение лекторов
    print(f"Лектор {lecturer1.name} {lecturer1.surname} лучше, чем лектор {lecturer2.name} {lecturer2.surname}?", lecturer1 > lecturer2)
    print(f"Средние оценки лекторов: {own_average_grade(lecturer1.grades)} и {own_average_grade(lecturer2.grades)} соответственно!")

    # Сравнение студентов
    print(f"Студент {student1.name} {student1.surname} лучше, чем студент {student2.name} {student2.surname}?", student1 > student2)
    print(f"Средние оценки студентов: {own_average_grade(student1.grades)} и {own_average_grade(student2.grades)} соответственно!")

    # Функции подсчёта средних оценок
    print("\nСредняя оценка за ДЗ по Python у всех студентов:",
          students_average_grade([student1, student2], "Python"))
    print("Средняя оценка за лекции по Python у всех лекторов:",
          mentors_average_grade([lecturer1, lecturer2], "Python"))