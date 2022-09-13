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
    """Lists public assignments for course"""

    i = 1
    for assignment in course.get_assignments():
        print("  " + str(i) + ") " + str(assignment))
        i += 1

    if i == 1:
        print("  None")


def list_courses():
    """Lists courses for current user"""

    i = 1
    for course in user.get_courses():
        print(str(i) + ") " + course.name)
        i += 1


def find_course(query):
    """Finds first instance of course matching course_name"""

    for course in user.get_courses():
        if query.lower() in str(course.name).lower():
            return course


user_input = input("Input course name: ")
set_course = find_course(user_input)

list_assignments(set_course)
list_courses()
