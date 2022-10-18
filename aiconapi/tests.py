from django.test import TestCase

# Create your tests here.

import requests
import json
import sys

url = "http://127.0.0.1:8000/aiconapi/check_result_nodb"
sess = requests.session()

print(sess.get(url))

csrftoken = sess.cookies['csrftoken']

# ヘッダ
headers = {'Content-type': 'application/json',  "X-CSRFToken": csrftoken}
# headers = {'Content-type': 'application/json'}

# 送信データ
prm = {"id": sys.argv[-1], "user": "nima"}

# JSON変換
params = json.dumps(prm)

# POST送信
res = sess.post(url, data=params, headers=headers)
# 戻り値を表示
print(res)
if res.status_code == 200:
    print(json.loads(res.text))
    