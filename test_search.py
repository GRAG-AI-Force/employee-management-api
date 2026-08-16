import urllib.request
import urllib.parse

try:
    url = (
        "http://localhost:8000/api/v1/employees/search?q="
        + urllib.parse.quote("a\x00b")
        + "&limit=59&skip=46633"
    )
    req = urllib.request.Request(url)
    res = urllib.request.urlopen(req)
    print(res.status, res.read())
except Exception as e:
    print(e)
