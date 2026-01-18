import sys
import csv
from jinja2 import Template
import matplotlib.pyplot as plt

students = {}
courses = {}


def dict_update(d, key1, key2, value):
    if key1 not in d:
        d[key1] = {}
    d[key1][key2] = value


f = open('data.csv', 'r')
reader = csv.DictReader(f)
for row in reader:
    dict_update(students, int(row['Student id']), int(row['Course id']),
                int(row['Marks']))
    dict_update(courses, int(row['Course id']), int(row['Student id']),
                int(row['Marks']))
f.close()

student_templates = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IIT@ds</title>
</head>
<body>
    <h1>Student Details</h1>
    <table border="1">
        <tr>
            <th>Student id</th>
            <th>Course id</th>
            <th>Marks</th>
        </tr>
        {% for key,value in student_details %}
        <tr>
            <td>{{student_id}}</td>
            <td>{{key}}</td>
            <td>{{value}}</td>
        </tr>
        {% endfor %}
        <tr>
            <td colspan="2">Total Marks</td>
            <td>{{student_marks}}</td>
        </tr>
    </table>
</body>
</html>
'''

course_templates = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IIT@ds</title>
</head>
<body>
    <h1>Course Details</h1>
    <table border="1">
        <tr>
            <th>Average Marks</th>
            <th>Maximum Marks</th>
        </tr>
        <tr>
            <td>{{avg}}</td>
            <td>{{max}}</td>
        </tr>
    </table>

    <img src="histogram.png" alt="">
</body>
</html>
'''

error_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IIT@ds</title>
</head>
<body>
    <h1>Wrong Inputs</h1>
    <p>Please enter valid inputs chutiye..!</p>
</body>
</html>
'''
argv_id = int(sys.argv[2])

try:
    if sys.argv[1] == '-s':
        student_temp = Template(student_templates)
        output = student_temp.render(student_details=students[argv_id].items(),
                                     student_marks=sum(
                                         students[argv_id].values()),
                                     student_id=argv_id)
        outputfile = open('progress.html', 'w')
        outputfile.write(output)
        outputfile.close()

    elif sys.argv[1] == '-c':

        plt.hist(courses[argv_id].values())
        plt.xlabel('Marks')
        plt.ylabel('Frequency')
        plt.savefig('histogram.png')

        course_temp = Template(course_templates)
        output = course_temp.render(avg=sum(courses[argv_id].values()),
                                    max=max(courses[argv_id].values()))
        outputfile = open('progress.html', 'w')
        outputfile.write(output)
        outputfile.close()
except Exception:
    outputfile = open('progress.html', 'w')
    outputfile.write(error_template)
    outputfile.close()