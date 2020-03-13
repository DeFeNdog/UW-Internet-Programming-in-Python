import re
import traceback
import operator


def index():
    body = """
<h1>Calculator Instructions</h1>
<div>
<ul>
    <li>Max of 3 operators</li>
    <li>Absolute path example: http://localhost:8080/operation/#/#/</li>
</ul>
</div>
<table cellpadding="10">
    <tr>
        <th>Relative Path</th>
        <th>Operation</th>
        <th>Arguments</th>
        <th>Expected</th>
    </tr>
    <tr>
        <th>/multiply/3/5</th>
        <th>multiply</th>
        <th>3, 5</th>
        <th>15</th>
    </tr>
    <tr>
        <th>/add/23/42</th>
        <th>add</th>
        <th>23, 42</th>
        <th>65</th>
    </tr>
    <tr>
        <th>/subtract/23/42</th>
        <th>subtract</th>
        <th>23, 42</th>
        <th>-19</th>
    </tr>
    <tr>
        <th>/divide/22/11</th>
        <th>divide</th>
        <th>22, 11</th>
        <th>2</th>
    </tr>
</table>

<h2>Supported Operations</h2>
<table>
    <tr><td>multiply</td></tr>
    <tr><td>add</td></tr>
    <tr><td>subtract</td></tr>
    <tr><td>divide</td></tr>
</table>
<style>
    td, th {
        border: 1px solid #999;
        padding: 0.5rem;
        text-align: left;
    }
    table {
        border-collapse: collapse;
        table-layout: fixed;
        text-align: left;
    }
</style>
"""
    return body


def page(operation, args, result):
    symbols = {
        'multiply': '*',
        'add': '+',
        'subtract': '-',
        'divide': '/'
    }
    calculation = [operation, args[0], symbols[operation], args[1], result]
    body = """
<h1>Calculator</h1>
<p>{}: {} {} {} = {}</p>
<a href="/">Back to instructions</a>
"""

    return body.format(*calculation)


def resolve_path(path):
    body = result = None

    calcs = {
        'multiply': operator.mul,
        'add': operator.add,
        'subtract': operator.sub,
        'divide': operator.truediv
    }

    path = path.strip('/').split('/')

    if path[0] == '/' or path[0] == '':
        body = index()
        return body, result
    else:
        if (len(path)) != 3:
            raise ValueError

    operator_name = path[0]
    args = list(map(int, path[1:]))

    if any(args) == 0:
        raise ValueError

    try:
        result = calcs[operator_name](args[0], args[1])
        body = page(operator_name, args, result)
    except KeyError:
        raise NameError

    return body, result


def application(environ, start_response):
    # TODO (bonus): Add error handling for a user attempting
    # to divide by zero.
    headers = [("Content-type", "text/html")]

    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError

        body, result = resolve_path(path)

        if body is None and result is None and path != '/':
            raise ValueError

        status = "200 OK"

    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except ValueError:
        status = "412 Precondition Failed"
        body = """
          <h1>Arguments Incorrect</h1>
          <a href="/">Refer to Instructions</a>
        """
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
        print(traceback.format_exc())
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
