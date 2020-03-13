#!/usr/bin/env python
import cgi
import cgitb

cgitb.enable()

form = cgi.FieldStorage()
operands = form.getlist('operand')

try:
    total = sum(map(int, operands))
    body = "Your total is: {}".format(total)
except (ValueError, TypeError):
    body = "Unable to calculate a sum: please provide integer operands."

print("Content-type: text/plain")
print()
print(body)