import os
import requests
from flask import Flask, send_file, Response
from bs4 import BeautifulSoup

app = Flask(__name__)

template = """{"instanceElements":[{"instancePicture":{"imageID":1999885},"instanceTexts":[{"text":"{}","placeholder":"top text","horizontalAlign":"center","verticalAlign":"near","color":"#ffffff"},{"text":"-Michael Scott","placeholder":"bottom text","horizontalAlign":"center","verticalAlign":"far","color":"#ffffff"}]}]}"""


def get_quote():
    response = requests.get("http://www.quotationspage.com/random.php")
    soup = BeautifulSoup(response.content, "html.parser")
    quotes = soup.find_all("dt", class_="quote")

    return quotes[0].getText()


def get_image(quote):
    payload = {'instanceDataJson': template.replace('{}', quote)}
    response = requests.get('https://memegenerator.net/img-preview/Instance/PreviewInstanceData', params=payload)

    return response.content


@app.route('/')
def home():
    quote = get_quote().strip()
    body = get_image(quote)

    return Response(response=body, mimetype="image/jpeg")


if __name__ == "__main__":
    port = int(os.environ.get("port", 6787))
    app.run(host='0.0.0.0', port=port)
