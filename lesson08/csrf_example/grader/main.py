import os
import base64
import random


from flask import Flask, request, session
from model import Grade

app = Flask(__name__)
app.secret_key = b''


@app.route('/', methods=['GET', 'POST'])
def home():
    # If the session does not include a CSRF token, then add one.
    if 'csrf_token' not in session:
        session['csrf_token'] = str(random.randint(10000000, 99999999))

    if request.method == 'POST':
        # Only save the grade if the form submission includes a CSRF token,
        # and it matches the token in the session.
        if request.form.get('csrf_token', None) == session['csrf_token']:
            g = Grade(
                student=request.form['student'],
                assignment=request.form['assignment'],
                grade=request.form['grade'])
            g.save()

    body = """
<html>
<body>
<h1>Enter Grades</h1>
<h2>Enter a Grade</h2>
<form method="POST">
    <label for="student">Student</label>
    <input type="text" name="student"><br>
    <label for="assignment">Assignment</label>
    <input type="text" name="assignment"><br>
    <label for="grade">Grade</label>
    <input type="text" name="grade"><br>
    <input type="hidden" name="csrf_token" value="{}">
    <input type="submit" value="Submit">
</form>

<h2>Existing Grades</h2>
""".format(session['csrf_token'])
    for g in Grade.select():
        body += """
<div class="grade">
{}, {}: {}
</div>
""".format(g.student, g.assignment, g.grade)

    return body


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6779))
    app.run(host='0.0.0.0', port=port)
