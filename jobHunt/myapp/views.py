#from django.views.generic import TemplateView
# 
#class IndexTemplateView(TemplateView):
#    template_name = "index.html"
import json
import requests
import datetime
import mysql.connector
from datetime import datetime
from requests.exceptions import RequestException, ConnectionError, HTTPError, Timeout
from django.http import JsonResponse
from django.shortcuts import render

PARAM_HOST = 'localhost'
PARAM_DATABASE = 'mysql'
PARAM_USER = 'root'
PARAM_PASSWORD = 'depk7y2d'
PARAM_URL = "http://localhost:8080" # APIエンドポイント（送信先）課題上の指定は『http://example.com/』

def index(request):
    return render(request, "index.html")

def make_insert_query(type):

    if "INS_TBL" == type:
        sql = "INSERT INTO ai_analysis_log (image_path, request_timestamp) VALUES (%s, %d);"
    return sql

def make_select_query(type):
    
    if "getIncrement" == type:
        #AI値(ID)の取得
        sql = "SELECT last_insert_id() FROM ai_analysis_log;"
    return sql

def make_update_query(type):

    #一旦成否分のみ
    if "SUCCESS" == type:
        sql = "UPDATE ai_analysis_log (success, message, class, confidence, response_timestamp) VALUES (%s, %s, %d, %d, %d) WHERE id = %d"
    elif "FAILED" == type:
        sql = "UPDATE ai_analysis_log (success, message, response_timestamp) VALUES (%s, %s, %d) WHERE id = %d"
    return sql

# DB処理（例外は呼び出し元で対応）
def exec_select_query(sql, param):

    #コネクション作成
    connection = mysql.connector.MySQLConnection(
        host        =PARAM_HOST,
        database    =PARAM_DATABASE,
        user        =PARAM_USER,
        password    =PARAM_PASSWORD
    )
    cursor = connection.cursor(prepared=True)

    #実行
    if 1 < len(cursor.execute(sql, param)):
        cursor.execute(sql, param)
    else:
        cursor.execute(sql)
    rows = cursor.fetchall()

    return rows
        
# DB処理（例外は呼び出し元で対応）
def exec_query(sql, param):
    try:
        #コネクション作成
        connection = mysql.connector.MySQLConnection(
            host        =PARAM_HOST,
            database    =PARAM_DATABASE,
            user        =PARAM_USER,
            password    =PARAM_PASSWORD
        )
        cursor = connection.cursor(prepared=True)
        print(cursor)
        #実行
        cursor.execute(sql, param)
        connection.commit()

        return ''
    
    except mysql.connector.error as err:
        if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            return "ユーザ名かパスワードが不正です。"
        elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            return "データベースが存在しません。"
        else:
            return "不明なDBエラー"

def send_receive_request(request):

    # POSTのみに対応
    if request.method == 'POST':

        # フォームから送られた文字列をて取得 ※エスケープ処理省略
        input_text = request.POST.get("input_text", '')

        print(input_text)

        #送信データ作成(json)
        request_data = {
            "image_path": input_text
        }
        print(request_data)

        # リクエスト時のUNIXTIMEを取得（少数以下切り捨て）
        now = datetime.now().replace(microsecond = 0)
        request_timestamp = int(now.timestamp())

        try:
            #----------------------------------------
            #API送信前にDB登録
            #----------------------------------------
            sql = make_insert_query("INS_TBL")
            print(sql)
            param = (
                input_text,
                request_timestamp
            )
            print(param)
            print("インサート前")
            resultMsg = exec_query(sql,param)
            print("インサート後")
            #----------------------------------------
            #Auto_Incrementの値を取得
            sql = make_select_query()
            print(sql)
            result = exec_select_query(sql, '')
            
            id = None


            for tmp in result:
                id = tmp['id']
                #1レコードのみ追加している為、1回取得できればok
                if "" == id:
                    break
            print(id)

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
                #--------------------------------------------------------------------------------
                #データ処理
                # ※modelによるDB更新処理の理解が不足している為、mysql.connectorによるDB更新処理で対応
                #--------------------------------------------------------------------------------

                param = None
                resultMsg = None

                #リクエストが成功していた場合、レスポンスにあわせてDBを更新
                if 'true' == received_data.get('success'):
                    param = (
                        received_data.get('success'),
                        received_data.get('message'), 
                        received_data["estimated_data"].get('class'),
                        received_data["estimated_data"].get('confidence'),
                        response_timestamp,
                        id
                    )
                    resultMsg = exec_query(make_update_query('SUCCESS'), param)
                else:
                    param = (
                        received_data.get('success'),
                        received_data.get('message'), 
                        response_timestamp,
                        id
                    )
                    resultMsg = exec_query(make_update_query('FAILED'), param)

                #正常終了時はブランク
                if '' == resultMsg:
                    return render(request, "index.html", {'message': "正常に終了しました。"})
                else:
                    return render(request, "index.html", {'message': resultMsg})
            else:
                #レスポンスが不正な場合
                return render(request, "index.html", {'message': f"HTTPリクエストが失敗しました。ステータスコード: {response.status_code}"})

        except requests.RequestException as e:

            #APIへのリクエストが失敗した場合
            return render(request, "index.html", {'message': f"リクエストエラー: {e}"})

    return render(request, 'index.html')