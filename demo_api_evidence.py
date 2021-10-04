# -*- coding: UTF-8 -*-

import time
import json
import random
import base64
import rsa
import traceback
import logging
from io import BytesIO
import tarfile
import requests

UP_URL = "http://quzheng.baidu.com/iprweb/v1/api_evidences"
DOWN_URL = "http://quzheng.baidu.com/iprweb/v1/api_download"
SHARE_URL = "http://quzheng.baidu.com/iprweb/v1/api_shares"
counter = {
    'badrequest': 0,
}

# TODO 替换成百度取证签发的key、value
headers = {"key": "airuike_", "value": "8c4473e9-a950-45d2-bad3-06356e978394"}

# TODO 替换成百度取证签发的RSA公钥
public_key_pem = '''
-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC79fP+Kl/HW081QrvbzCt8naYx
0Lgchdah4kzJrjhPSNRElbDuCwmPltHvewa/LLy6BL0VXhKQXiyvGn2tWOA4+rHc
r8TaX2izSYVyCXrX/PCQhTP0g/7+V7bzlHu2CaLPjTSoUGxUDnUV1qhHqnXtU0Jb
rRpkd+x4Ie9V/loROQIDAQAB
-----END PUBLIC KEY-----
'''
publicKey = rsa.key.PublicKey.load_pkcs1_openssl_pem(public_key_pem)
length = 100

# TODO 替换成自己的RSA 私钥
private_key_pem = '''
-----BEGIN RSA PRIVATE KEY-----
MIICXgIBAAKBgQDTkSgkKB9CVOTe5kib9BNTEUh8/onsQPyRMEBW+F1MIJ8rFr4t
TfJmTZhotAN7xbSsDHLlqhwuWSjizHt1bfJ5Avn4jmpX2DDDMVQhee4/Akqijtf1
ba1U6KWYSwW5zMWBa2n4dkyWWQBaAlgXDQWGRHsqSWdZbJKzi1rq6UwZgQIDAQAB
AoGBAI6SDz7uWsJUezdKcDvIKw2bZAH3dfJjiNA+d90j2ZtnkFt1JAtbr7IJMF++
j2plPO+EJBlonT0OkGLl8Xyc7vwrDxHtv2BZ0RVzKW8ewnCrtcUMqN9/sQB//hqO
z1uiGSYhW1ZOTd73GqJfhwPAYxBFfRkFqRH3wvJFB0L9rhcBAkEA+K8sd2LxPScy
Bv+JtUPlj/r8ns2b0lIjHN2xfguiM4GL/85oSkfKXdWYOka87QRryVat4T/XmurK
XFIdVHNVCQJBANnKdI6R51Q9w4BbrLRPXqC3SV0k385RG3wqzLAHgL16WjhJsbx3
6NG5TDzTcuQ2tNQ9U77KF3VkbUyoWRCV9rkCQCfpRUOr13evELJa1KkIypD/AQgj
i3yHvibl1ZSbHV8SzXsyjz5Mo0fH/fRsYenQKdRYWvOpoVq1j+CdNSPWlrECQQCm
gfOU4JXEwSfL5crnW9sT8q1jSgLV4QqrZqlxV3sk4ftCF42McvyMAyf3RQ4Mzop3
zZ9OOYGv3aT2u6rEVHL5AkEA8IMQ/u1ATTmCdD/Uf29eayUKrvUnwLAqgmXrz3T5
Eha64PDxVFS84DClayHwSZDlf36mYm37BF6UEOCRIrKtPw==
-----END RSA PRIVATE KEY-----
'''
privateKey = rsa.key.PrivateKey.load_pkcs1(private_key_pem)
decryptLen = 128


def put(url):
    """
        提交取证任务
        :param url: 待取证url
    """
    if not url.startswith('http'):
        url = 'http://' + url
    clue = ''
    referer = "http://www.baidu.com/s?wd=%d" % (random.randint(0, 100))
    req = {
        "source_uid": "6a2370dc0b8f8328fc1d8111eb98cb",  # TODO 替换成百度取证签发的source_uid
        "url": url,
        "mode": "advanced",     # TODO 高级参数，浏览器类型可以根据接口文档自行修改
        "device_type": "0",
        "browser_type": "1",
        "screen_type": "3",
        "enable_flash": "1",
        "on_complete_delay": "10",
        "scheduled_hour": "-1",
        "scheduled_minute": "-1",
        "gzc": "0",
        "referer": referer,
        "use_agency": "0",
        "agency": "0",
        "url_type": 0,
        "check_addr": '',
        "check_ip": ''
    }

    body = json.dumps(req)
    # 先进行rsa加密后,进行base64加密, 提供的rsa公钥只能加密100个字符, 因此分段对原文进行加密, 然后再拼接起来
    rsaDataList = []
    for i in range(0, len(body), length):
        end = i + length
        rsaDataList.append(rsa.encrypt(str.encode(body[i:end]), publicKey))
    rsaData = b''.join(rsaDataList)
    encryptedBody = base64.b64encode(rsaData)

    errCode = -1
    taskIdStr = "noid"

    for x in range(1):
        try:
            result = requests.post(UP_URL, encryptedBody, headers=headers)
            res = json.loads(result.text)
            if "err_code" in res:
                errCode = res["err_code"]
                if res["err_code"] != 0:
                    counter['badrequest'] += 1
            if "data" in res and len(res['data']) > 0:
                data = base64.b64decode(res["data"])
                # 先进行base64解密, 然后进行rsa解密, 提供的rsa私钥只能解密128个字符, 因此分段对密文解密, 然后再拼接
                decrypteData = []
                for i in range(0, len(data), decryptLen):
                    decrypteData.append(rsa.decrypt(data[i:i + decryptLen], privateKey).decode('utf-8'))
                taskId = "".join(decrypteData)
                taskId = json.loads(taskId)
                if "task_id" in taskId:
                    logging.info("%s\turl:%s\ttask_id:%s" % (
                        time.strftime("%Y-%m-%d#%H:%M:%S", time.localtime()), url, taskId["task_id"]))
                    taskIdStr = taskId["task_id"]
                    time.sleep(1)
                    break
        except Exception as e:
            counter['badrequest'] += 1
            logging.error("%s:url(%s) catch exception:%s,[%d]" % (
                time.strftime("%Y-%m-%d#%H:%M:%S", time.localtime()), url, e, x))
            logging.error(traceback.format_exc())
            time.sleep(1 + x * 2)

    return taskIdStr


def download(url, task_id):
    """
        下载证据包
    """
    req = {
        "task_id": task_id
    }

    body = json.dumps(req)
    # 先进行rsa加密后,进行base64加密, 提供的rsa公钥只能加密100个字符, 因此分段对原文进行加密, 然后再拼接起来
    # _data = base64.b64encode(RSAToken.RSA_Long_Encrypt(publicKey, json.dumps(_body)))
    rsaData = rsa.encrypt(body, publicKey)
    encryptedBody = base64.b64encode(rsaData)

    resources = ""
    html = ""

    try:
        con = requests.get(DOWN_URL, data=encryptedBody, headers=headers, timeout=5).content
        fileobj = BytesIO(con)
        tar = tarfile.open(fileobj=fileobj)
        html = tar.extractfile("离线页面.html").read()
        # resources = tar.getnames()
    except Exception as e:
        counter['badrequest'] += 1
        logging.error("%s:url(%s) catch exception:%s" % (time.strftime("%Y-%m-%d#%H:%M:%S", time.localtime()), url, e))
        logging.error(traceback.format_exc())

    return html


def share(url, task_id):
    """
        生成分享链接
    """
    req = {
        "task_id": task_id
    }

    body = json.dumps(req)
    # 先进行rsa加密后,进行base64加密, 提供的rsa公钥只能加密100个字符, 因此分段对原文进行加密, 然后再拼接起来
    # _data = base64.b64encode(RSAToken.RSA_Long_Encrypt(publicKey, json.dumps(_body)))
    rsaData = rsa.encrypt(body, publicKey)
    encryptedBody = base64.b64encode(rsaData)
    surl = None
    for c in range(3):
        try:
            r = requests.post(SHARE_URL, data=encryptedBody, headers=headers, timeout=15)
            x = json.loads(r.text)
            # print x
            if x.get('err_code', -1) == 0:
                encrypt_text = base64.b64decode(x['data'])
                # 先进行base64解密, 然后进行rsa解密, 提供的rsa私钥只能解密128个字符, 因此分段对密文解密, 然后再拼接
                decrypteData = []
                for i in range(0, len(encrypt_text), decryptLen):
                    decrypteData.append(rsa.decrypt(encrypt_text[i:i + decryptLen], privateKey))
                sdata = "".join(decrypteData)
                jsdata = json.loads(sdata)
                surl = "http://quzheng.baidu.com/s/%s" % (jsdata['share_code'])
                break
        except Exception as e:
            logging.error("%s:url(%s) catch exception:%s,[%d]" % (
                time.strftime("%Y-%m-%d#%H:%M:%S", time.localtime()), url, e, c))
            logging.error(traceback.format_exc())
            time.sleep(1 + c * 2)
    return surl


def query(task_id):
    """
        查询任务状态
    """
    URL = "http://quzheng.baidu.com/iprweb/v1/api_evidences"
    req = {
        "task_ids": [task_id]
    }
    status = 0
    try:
        body = json.dumps(req).encode('utf-8')
        rsaData = rsa.encrypt(body, publicKey)
        encryptedBody = base64.b64encode(rsaData)
        for x in range(1):
            res = requests.get(URL, data=encryptedBody, headers=headers, timeout=(6, 24))
            res = json.loads(res.text)
            if "data" in res:
                data = base64.b64decode(res["data"])
                decrypteData = []
                for i in range(0, len(data), decryptLen):
                    decrypteData.append(rsa.decrypt(data[i:i + decryptLen], privateKey))
                r = b"".join(decrypteData)
                j = json.loads(r)
                # status:
                # 0 = wait
                # 1 = finished
                # 4 = failed
                status = j.get(task_id, 4)
                break
    except Exception as e:
        logging.exception("evidence_api send ret Exception [{}]".format(e))
        return (status, task_id)
    logging.info("query success status [{}] eid [{}]".format(status, task_id))
    print(status, task_id)
    return (status, task_id)


def main():
    # url = "https://shanqian.cn/evidence/signCertificate"
    # task_id = put(url=url)
    # print(task_id)

    task_id = "faf5bea82b1011ebb35da0369f31730c"
    query(task_id)


if __name__ == '__main__':
    main()
