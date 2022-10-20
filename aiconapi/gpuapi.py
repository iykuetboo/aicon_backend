import urllib.request
import urllib.parse
import asyncio
import time
from django.conf import settings

def send_to_gpu(prompt,id,reqAddtionalHeaders={}):
    # 特定HEADER送信の例です。このサンプルに未使用
    data = urllib.parse.urlencode({"prompt": prompt,"id":id})
    data = data.encode('utf-8')
    cnt = 0

    print(f'trial {cnt} finish')
    while cnt < 2:
        cnt = cnt+1
        try:
            req = urllib.request.Request(settings.GPU_PATH, data,reqAddtionalHeaders)

            with urllib.request.urlopen(req, timeout=5) as f:
                print(f.read().decode('utf-8'))
            
            return True
        except:
            print(f'failed to send prompt to gpu, retrying... \nprompt:{prompt}')
            time.sleep(1)
        print(f'trial {cnt} finish')
    return False
        
