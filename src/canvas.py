from canvasapi import Canvas

# To install CanvasAPI (https://github.com/ucfopen/canvasapi)
# pip install canvasapi

# Canvas API URL
API_URL = "https://csufullerton.instructure.com"
# Canvas API key
API_KEY = "349~RVcIDeSG49aKDSmw3Tzo3iEz2kw6Nqt0CMZOe5JyBa7Ax7d1pAZlncTMCFzkFh2X"

# Initialize a new Canvas object
canvas = Canvas(API_URL, API_KEY)

# Initialize user
user = canvas.get_current_user()
set_course = None

user_input = input("Input course name: ")

# Finds first instance of course matching course_name
for course in user.get_courses():
    if user_input.lower() in str(course.name).lower():
        set_course = course
        break

# Print course name
print("---------------------")
print(set_course.name)

# List of all assignments
i = 1
print("  Assignments")
for assignment in set_course.get_assignments():
    print("  " + str(i) + ") " + str(assignment))
    i += 1

if i == 1:
    print("  None")