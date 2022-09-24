from canvasapi import Canvas

# To install CanvasAPI (https://github.com/ucfopen/canvasapi)
# pip install canvasapi

# Canvas API URL
API_URL = "https://canvas.instructure.com/"
# Canvas API key
API_KEY = "349~NTHNMprd3AAqhwgIY8veN9PrZvH8VZ8TUaouLIpyYBDCHwdQ0VX1ebOaIC8RRYUt"


def set_api_key(key):
    global API_KEY
    API_KEY = key


def list_assignments(course):
    """Returns list of public assignments for course
        Returns null if no assignments found"""

    assignments = list()

    for assignment in course.get_assignments():
        assignments.append(str(assignment))

    return assignments


def list_courses():
    """Returns list of courses for current user
        Returns null if no courses found"""

    canvas = Canvas(API_URL, API_KEY)
    user = canvas.get_current_user()

    courses = list()

    for course in user.get_courses():
        courses.append(course.name)

    return courses


def find_course(query):
    """Returns first instance of course matching course_name
        Returns null if query is not found"""

    canvas = Canvas(API_URL, API_KEY)
    user = canvas.get_current_user()

    course_query = None

    for course in user.get_courses():
        if query.lower() in str(course.name).lower():
            course_query = course

    return course_query
