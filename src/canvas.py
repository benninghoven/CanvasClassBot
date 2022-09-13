from canvasapi import Canvas

# To install CanvasAPI (https://github.com/ucfopen/canvasapi)
# pip install canvasapi

# Canvas API URL
API_URL = "https://canvas.instructure.com/"
# Canvas API key
API_KEY = "349~NTHNMprd3AAqhwgIY8veN9PrZvH8VZ8TUaouLIpyYBDCHwdQ0VX1ebOaIC8RRYUt"

# Initialize a new Canvas object
canvas = Canvas(API_URL, API_KEY)

# Initialize user
user = canvas.get_current_user()


def list_assignments(course):
    """Returns list of public assignments for course
        Returns null if no assignments found"""

    assignments = list()

    for assignment in course.get_assignments():
        assignments.append(str(assignment))

    if len(assignments) == 0:
        return None
    else:
        return assignments


def list_courses():
    """Returns list of courses for current user
        Returns null if no courses found"""

    courses = list()

    for course in user.get_courses():
        courses.append(course.name)

    if len(courses) == 0:
        return None
    else:
        return courses


def find_course(query):
    """Returns first instance of course matching course_name"""

    for course in user.get_courses():
        if query.lower() in str(course.name).lower():
            return course


user_input = input("Input course name: ")
set_course = find_course(user_input)

assignments = list_assignments(set_course)
courses = list_courses()
