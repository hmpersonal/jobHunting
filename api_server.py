# -*- coding: utf-8 -*-
import random
import http.server as s
import json

class MyHandler(s.BaseHTTPRequestHandler):
    def do_POST(self):
        self.make_data()
    #def do_GET(self):
    #    self.make_data()
    def make_data(self):
        # 受信情報
        content_len=int(self.headers.get('content-length'))
        requestBody = json.loads(self.rfile.read(content_len).decode('utf-8'))
        print(requestBody)

        # 返信を組み立て
        # とりあえず６割ぐらい成功する確率で
        dead_or_alive = random.randint(1, 100)
        print(dead_or_alive)
        if 60 >= dead_or_alive:
            #成功
            response = {"success" : "true",
                        "message" : "success",
                        "estimated_data" : { "class" : 3, "confidence" : 0.8683}
                        }
        else:
            #失敗
            response = {"success" : "false",
                        "message" : "Error:E50012",
                        "estimated_data" : {}
                        }

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        responseBody = json.dumps(response)
        self.wfile.write(responseBody.encode('utf-8'))

host = 'localhost'
port = 8080
httpd = s.HTTPServer((host, port), MyHandler)
print('サーバを起動しました。ポート:%s' % port)
httpd.serve_forever()