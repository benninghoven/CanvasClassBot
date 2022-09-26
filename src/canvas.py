from canvasapi import Canvas

# To install CanvasAPI (https://github.com/ucfopen/canvasapi)
# pip install canvasapi

# Canvas API URL
API_URL = "https://canvas.instructure.com/"

# Guild keys [guild_id][api_key]
guild_keys = {
    0: 0
}


def set_api_key(guild_id, api_key):
    """Sets API key for guild"""
    guild_keys.update({guild_id: api_key})


def list_assignments(course):
    """Returns list of public assignments for course
        Returns null if no assignments found"""

    assignments = list()

    for assignment in course.get_assignments():
        assignments.append(str(assignment))

    return assignments


def list_courses(api_key):
    """Returns list of courses for current user
        Returns null if no courses found"""

    canvas = Canvas(API_URL, api_key)
    user = canvas.get_current_user()
    courses = list()

    for course in user.get_courses():
        courses.append(course.name)

    return courses


def search_course(api_key, query):
    """Returns first instance of course matching course_name
        Returns null if query is not found"""

    canvas = Canvas(API_URL, api_key)
    user = canvas.get_current_user()

    courses = list()

    for course in user.get_courses():
        if query.lower() in str(course.name).lower():
            courses.append(course)

    return courses
