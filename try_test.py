import requests

url = 'http://127.0.0.1:8000/detail_comment'

payload = {'rating': 3, 'name_of_stuff': 12, 'comment': 'test_req'}

req = requests.post(url=url, auth=('nick', 123), data=payload)

res = req
print(res)
