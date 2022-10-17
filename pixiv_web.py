import socketserver as socketserver
from http.server import SimpleHTTPRequestHandler
import imp
import requests as req
import json
import time
import random 
import os 


ip = ['20.213.247.195','13.74.59.33','145.40.121.101','45.167.125.97','157.100.12.138','173.244.48.9','51.79.205.165','190.15.103.66','45.42.177.50','8.219.64.236']
url='https://www.pixiv.net/ajax/search/illustrations/'
headers = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Mobile Safari/537.36 Edg/105.0.1343.42',
    #'cookie': '自己的cookie'
}

like=[]
il_url = []
pixiv_url = []

def bubbleSort(arr, arr2, arr3):
    n = len(arr)   
    for i in range(n):        
        for j in range(0, n-i-1): 
            if int(arr[j]) < int(arr[j+1]) :
                arr[j], arr[j+1] = arr[j+1], arr[j]
                arr2[j], arr2[j+1] = arr2[j+1], arr2[j]
                arr3[j], arr3[j+1] = arr3[j+1], arr3[j]

def pixiv_get(keyword, page, rating_count):
    for a in range(1,page+1):
        params = {
            'p':str(a),
            'type': 'illust_and_ugoira',
            'word': keyword,
            'mode': 'all',
            'order': 'date_d',
            's_mode': 's_tag_full',
            'lang': 'zh_tw'
        }
        web = req.get(url+params['word']+'?', headers=headers , params=params, proxies={'http':ip[random.randint(0,9)]})
        js=web.json()['body']['illust']['data']
        time.sleep(random.uniform(1, 2))

        for i in js:
            url2='https://www.pixiv.net/touch/ajax/illust/details?'
            params2 ={
                'illust_id':i['id'],
                'ref': 'https://www.pixiv.net/manage/requests',
                'lang': 'zh_tw'
            }
            web2 =req.get(url2, headers=headers, params=params2, proxies={'http':ip[random.randint(0,9)]})
            if int(web2.json()['body']['illust_details']['rating_count']) > rating_count:
                like.append(web2.json()['body']['illust_details']['rating_count'])
                z = i['url'].replace('i.pximg.net', 'i.pixiv.cat')
                il_url.append(z)
                pixiv_url.append("https://www.pixiv.net/artworks/"+ i['id'])                
            else:
                pass    
        print('第' + str(a) + '頁')    

    bubbleSort(like, il_url, pixiv_url)


    '''name = 1
    for d in il_url:
        jpg = req.get(d)     # 使用 requests 讀取圖片網址，取得圖片編碼
        f = open(f'download/text_{name}.jpg', 'wb')    # 使用 open 設定以二進位格式寫入圖片檔案
        f.write(jpg.content)   # 寫入圖片的 content
        f.close()              # 寫入完成後關閉圖片檔案
        name += 1      需要下載圖片在加   '''


    html1 = """
    <html lang="zh-Hant-TW">
    <head>
    <meta charset="UTF-8">
    </head>
    <body>

    <p id="demo"></p>
    <script>
    """
    w = 'url=['
    u = 'img=['
    for i1 in il_url:
        u+='''"'''+i1+'''"'''+','
    u+=']'
    for i2 in pixiv_url:
        w+='''"'''+i2+'''"'''+','
    w+=']'

    html2 = """
    img_num = img.length; //讀出陣列總筆數

    img_html = "<ul>";

    for (i = 0; i < img_num; i++) {
    console.log(i);

    img_html += "<a href="+url[i]+"><img src="+img[i]+"></a>"; 

    }
    img_html +="</ul>";

    console.log(img_html);

    document.getElementById("demo").innerHTML = img_html ;
    </script>

    </body>
    </html>
    """

    class MyHandler(SimpleHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            output = html1+u+'\n'+w+html2

            self.wfile.write(output.encode('utf-8'))


    os.system('"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" http://localhost:8080')
    print('完成')
    socketserver.TCPServer(('127.0.0.1', 8080), MyHandler).serve_forever() 


pixiv_get('cyberpunk',10 , 500) #第一個輸入關鍵字(str)，第二個輸入要爬取頁數(int)(未登入狀態僅能爬取十頁)，第三個輸入只下載多少讚數以上的圖片(int)
