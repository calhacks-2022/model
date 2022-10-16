import requests
from bs4 import BeautifulSoup

repo = "expressjs/express"
page_num = 3
url = 'https://github.com/{}/network/dependents'.format(repo)

for i in range(page_num):
    print("GET " + url)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    data = [
        "{}/{}".format(
            t.find('a', {"data-repository-hovercards-enabled":""}).text,
            t.find('a', {"data-hovercard-type":"repository"}).text
        )
        for t in soup.findAll("div", {"class": "Box-row"})
    ]

    print(data)
    print(len(data))
    paginationContainer = soup.find("div", {"class":"paginate-container"}).find('a')
    if paginationContainer:
        url = paginationContainer["href"]
    else:
        break