#from django.views.generic import TemplateView
# 
#class IndexTemplateView(TemplateView):
#    template_name = "index.html"
import json
import requests
import datetime
from datetime import datetime
from requests.exceptions import RequestException, ConnectionError, HTTPError, Timeout
from django.http import JsonResponse
from django.shortcuts import render
from myapp.models import ai_analysis_log
from django.db import IntegrityError

PARAM_URL = "http://localhost:8080" # APIエンドポイント（送信先）課題上の指定は『http://example.com/』

def index(request):
    return render(request, "index.html")

def send_receive_request(request):

    # POSTのみに対応
    if request.method == 'POST':

        # フォームから送られた文字列をて取得 ※エスケープ処理省略
        input_text = request.POST.get("input_text", '')

        # 送信データ作成(json)
        request_data = {
            "image_path": input_text
        }

        # リクエスト時のUNIXTIMEを取得（少数以下切り捨て）
        now = datetime.now().replace(microsecond = 0)
        request_timestamp = int(now.timestamp())

        try:
            # テーブルモデルのインスタンス生成
            tbl = ai_analysis_log()

            # 登録値をセット
            tbl.imagePath = input_text
            tbl.requestTimestamp = request_timestamp
            # データを登録
            tbl.save()
            print("データ登録に成功しました。")
        except IntegrityError as e:
            print(f"データ登録に失敗しました: {e}")
        except Exception as e:
            print(f"予期せぬエラーが発生しました: {e}")

        # 更新キーとなるid(auto_increment)の値を取得
        key_id = tbl.id
        print(key_id)

        # HTTP POSTリクエストでJSONデータを送信
        response = requests.post(PARAM_URL, data = json.dumps(request_data))
        # レスポンス時のUNIXTIMEを取得（少数以下切り捨て）
        reNow = datetime.now().replace(microsecond = 0)
        response_timestamp = int(reNow.timestamp())

        # レスポンスの確認
        if 200 == response.status_code:

            # 受信したJSONデータの解析
            received_data = response.json()
            print(received_data)

            # 前回登録したデータをidをキーに指定
            tbl = ai_analysis_log.objects.get(id=key_id)

            # 更新値をセット
            tbl.success = received_data.get('success')
            tbl.message = received_data.get('message')
            if 'true' == received_data.get('success'):
                # 成功時のみセット
                tbl.cls = received_data["estimated_data"].get('class')
                tbl.confidence = received_data["estimated_data"].get('confidence')
            else:
                tbl.cls = None
                tbl.confidence = None
            tbl.responseTimestamp = response_timestamp
            
            tbl.save()

            return render(request, "index.html", {'message': "正常に終了しました。"})
        else:
            #レスポンスが不正な場合
            return render(request, "index.html", {'message': f"HTTPリクエストが失敗しました。ステータスコード: {response.status_code}"})

    return render(request, 'index.html')