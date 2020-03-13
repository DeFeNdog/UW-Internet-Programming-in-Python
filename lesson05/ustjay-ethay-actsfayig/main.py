import os
import requests
from flask import Flask, Response
from bs4 import BeautifulSoup

app = Flask(__name__)

# https://fathomless-eyrie-30647.herokuapp.com/


def get_fact():
    response = requests.get("http://unkno.com")
    soup = BeautifulSoup(response.content, "html.parser")
    facts = soup.find_all("div", id="content")

    return facts[0].getText().strip()


def post_fact(fact):
    URL = 'https://hidden-journey-62459.herokuapp.com/piglatinize/'
    payload = {
        'input_text': fact
    }
    response = requests.post(URL, data=payload)
    link = '<a href="{url}" target="_blank">{url}</a>'.format(url=response.url)

    return link


@app.route('/')
def home():
    fact = get_fact()
    body = post_fact(fact)

    return Response(response=body, mimetype="text/html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6787))
    app.run(host='0.0.0.0', port=port)
