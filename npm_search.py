import requests

def search_npm(api_key, queries):
    ret = set()
    for query in queries:
        r = requests.get(f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx=626e50bc7dd2043a2&q={query}&fields=items(link)")
        res = r.json()
        if 'items' not in res:
            print("Error")
            print(queries)
            return []
        results = [item['link'].split('package/')[-1].split('/v/')[0].split('?')[0] for item in res['items']][:5]
        for result in results:
            ret.add(result)
    return list(ret)
