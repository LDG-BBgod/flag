import hashlib, hmac, base64, time
import requests, json
import traceback
import datetime

def sendMessageFunc (content):

    def getSigningKey():

        timestamp = str(int(time.time() * 1000))

        access_key = "Lyf4UlLYnAqvptuxG9Oq"
        secret_key = "O8DxN19g9zaRZ335Wgx5FCzQfXPIbZfkLR5dng4C"
        secret_key = bytes(secret_key, 'UTF-8')

        method = "POST"
        
        uri = "/sms/v2/services/ncp:sms:kr:289661419957:gabot/messages"

        message = method + " " + uri + "\n" + timestamp + "\n" + access_key
        message = bytes(message, 'UTF-8')
        signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
        return signingKey
 

    headers = {
        "Contenc-type": "application/json; charset=utf-8",
        "x-ncp-apigw-timestamp": str(int(time.time() * 1000)),
        "x-ncp-iam-access-key": 'Lyf4UlLYnAqvptuxG9Oq',
        "x-ncp-apigw-signature-v2": getSigningKey(),
        }
    body = {
        'type': 'SMS',
        'contentType': 'COMM',
        'countryCode': '82',
        'from': '01054088229',
        'content': content,
        'messages': [{
            'to': '01054088229',
        }],
    }
    
    return requests.post('https://sens.apigw.ntruss.com/sms/v2/services/ncp:sms:kr:289661419957:gabot/messages', json=body, headers=headers)

def save_error_log(error_message):
    try:
        log_file_path = "error_log.txt"

        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


        error_log = f"Time: {current_time}\n"
        error_log += f"Error Message: {error_message}\n"
        error_log += traceback.format_exc()

        with open(log_file_path, "a") as file:
            file.write(error_log)
            file.write("\n\n\n")

    except Exception as e:
        pass



def check_website(url):

    try:
        response = requests.get(url)

        if response.status_code == 200:
            pass
        else:
            content = url + ': 사이트 에러 로그확인'
            sendMessageFunc(content)
            save_error_log(response.content)    

    except requests.exceptions.RequestException as erra:
        content = url + ': 익셉션 에러 로그확인'
        sendMessageFunc(content)
        save_error_log("AnyException : " + str(erra))

urls = [
    "https://cabot.co.kr",
    "https://cabo.kr",
    "https://gabot.co.kr",
]

for url in urls:

    check_website(url)