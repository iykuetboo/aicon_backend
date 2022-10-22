import requests
import json
import sys

# url = 'https://aicon-maker-backend.herokuapp.com/aiconapi/reserve'
# url = 'http://localhost:8000/aiconapi/reserve'
url = 'http://localhost:8000/aiconapi/reserve_from_question'

sess = requests.session()

# headers = {'Content-type': 'application/json',  'X-CSRFToken': csrftoken}
headers = {'Content-type': 'application/json'}

# 送信データ
prm = {'tags': [0,1,1,2,0,1,1,0]}

# JSON変換
params = json.dumps(prm)

# POST送信
res = sess.post(url, data=params, headers=headers)
# 戻り値を表示
if res.status_code == 200:
    print(json.loads(res.text))
else:
    print(res)
