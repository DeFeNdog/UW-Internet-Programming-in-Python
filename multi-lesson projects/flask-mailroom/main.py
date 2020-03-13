import os
import datetime
import logging

from peewee import *  # noqa F403
from flask import Flask, render_template, request, redirect, url_for, session
from models import db, Donor, Donation  # noqa F403
from queries import *  # noqa F403
from utilities import *  # noqa F403

now = datetime.datetime.now()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# database = SqliteDatabase('mailroom.db')  # noqa F403
# database.execute_sql('PRAGMA foreign_keys = ON;')

# app.secret_key = b''
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY').encode()


@app.route('/')
def home():
    return redirect(url_for('donors_list'))


@app.route('/donor/add', methods=['GET', 'POST'])
def donor_add():

    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        donation = float(request.form['donation'])

        q = Queries()  # noqa F403
        d = Donor()  # noqa F403
        d.first_name = first_name
        d.last_name = last_name
        q.insert_donor_donation(d, float(donation))
        return redirect(url_for('donors_list'))

    if 'first_name' not in session or 'last_name' not in session:
        return render_template('donor_add.jinja2')


@app.route('/donor/edit', methods=['GET', 'POST'])
def donor_edit():
    q = Queries()  # noqa F403
    dl = {
        'code': '',
        'first_name': '',
        'last_name': ''
    }

    if request.method == 'GET':
        code = request.args.get('code', None)
        donor = q.get_donor_by_id(code)
        dl = {
            'code': code,
            'first_name': donor.first_name,
            'last_name': donor.last_name
        }
        return render_template('donor_edit.jinja2', donor=dl)

    if request.method == 'POST':
        code = request.form['code']
        dl = {
            'code': code,
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name']
        }
        q.update_donor(code,
                       request.form['first_name'],
                       request.form['last_name'],
                       request.form['prev_name'])
        return redirect(url_for('donors_list'))


@app.route('/donor/delete',  methods=['GET'])
def donor_delete():
    code = request.args.get('code', None)
    last_name = None
    if code:
        q = Queries()  # noqa F403
        donor = q.get_donor_by_id(code)
        q.delete_donor_donations(code)
        last_name = donor.last_name
    return render_template('donor_delete.jinja2', code=code, last_name=last_name)


@app.route('/donation/add',  methods=['GET', 'POST'])
def donation_add():
    q = Queries()  # noqa F403
    dl = {
        'code': '',
        'first_name': '',
        'last_name': '',
        'donation': 0.00
    }

    if request.method == 'GET':
        code = request.args.get('code', None)
        donor = q.get_donor_by_id(code)
        dl = {
            'code': code,
            'first_name': donor.first_name,
            'last_name': donor.last_name,
            'donation': 0.00
        }
        return render_template('donation_add.jinja2', donor=dl)

    if request.method == 'POST':
        code = request.form['code']
        donation = request.form['donation']
        q = Queries()  # noqa F403
        q.insert_donation(code, donation)
        dl = {
            'code': code,
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'donation': donation
        }
        return render_template('letter_single.jinja2', donor=dl)


@app.route('/donors/list', methods=['GET'])
def donors_list():
    q = Queries()  # noqa F403
    donors = q.get_donor_multiple_summary()
    dl = []
    for d in donors:
        dl.append(
            {
                'code': d[0],
                'first_name': d[1],
                'last_name': d[2],
                'donations': d[3]
            }
        )
    return render_template('donors_list.jinja2', donors=dl)


@app.route('/donors/report')
def donors_report():
    q = Queries()  # noqa F403
    donors = q.get_donor_multiple_summary()
    dl = []
    for d in donors:
        dl.append(
            {
                'code': d[0],
                'first_name': d[1],
                'last_name': d[2],
                'donations': d[3],
                'count': d[4],
                'average': d[5]
            }
        )
    return render_template('donors_report.jinja2', donors=dl)


@app.route('/donor/report',  methods=['GET', 'POST'])
def donor_report():
    q = Queries()  # noqa F403
    dls = []
    dl = None

    if request.method == 'GET':
        donors = q.get_donors()
        for d in donors:
            dls.append(
                {
                    'code': d.code,
                    'first_name': d.first_name,
                    'last_name': d.last_name
                }
            )

    if request.method == 'POST':
        code = request.form['code']
        d = q.get_donor_single_summary(code)
        dl = {
            'code': code,
            'first_name': d[0],
            'last_name': d[1],
            'count': d[3],
            'average': d[4],
            'donations': d[2]
        }

    return render_template('donor_report.jinja2', donors=dls, donor=dl)


@app.route('/letter/multiple')
def letter_multiple():
    q = Queries()  # noqa F403
    cwd = os.getcwd()
    date = now.strftime('%Y-%m-%d')
    path = cwd + '/letters/'
    ext = '.txt'
    q = Queries()  # noqa F403
    donors = q.get_donor_multiple_summary()
    sd = sorted(donors, key=lambda d: d[3], reverse=True)
    for d in sd:
        file_path = "{}{}_{}_{}{}".format(path, date,
                                          d[1],
                                          d[2],
                                          ext)
        donations = "${0:.2f}".format(float(d[3]))
        with open(file_path, 'w') as letter:
            text = ('\n\nDear {} {},\n\n'
                    '        Thank you for your very kind '
                    'donations totaling {}.\n\n'
                    '        It will be put to very good use.\n\n'
                    '               Sincerely,\n'
                    '                  -The Team\n\n')
            body = text.format(d[1], d[2], donations)
            letter.write(body)
    return render_template('letter_multiple.jinja2')


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)
