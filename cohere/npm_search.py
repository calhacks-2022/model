import requests

API_KEY = ""
with open('../apikey.txt') as f:
    API_KEY = f.readline()

def search_npm(queries):
    ret = set()
    for query in queries:
        r = requests.get(f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx=626e50bc7dd2043a2&q={query}&fields=items(link)")
        res = r.json()
        results = [item['link'].split('/')[-1] for item in res['items']]
        for result in results:
            ret.add(result)
    return ret

if __name__ == "__main__":
    print(list(search_npm(["react", "react-dropdown"])))