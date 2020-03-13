import requests
from bs4 import BeautifulSoup

response = requests.get("http://unkno.com/")
soup = BeautifulSoup(response.content, "html.parser")
fact = soup.find(id="content")
print(fact.getText())
