import os
import requests
import time
import math
import dingdingconfig as dd


def download_video(url, file_path):
    try:

        headers = {
            "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/89.0.4389.128 Safari/537.36'}

        pre_content_length = 0

        # 循环接收视频数据

        while True:  # 若文件已经存在，则断点续传，设置接收来需接收数据的位置

            if os.path.exists(file_path):
                headers['Range'] = 'bytes=%d-' % os.path.getsize(file_path)

            res = requests.get(url, stream=True, headers=headers)

            content_length = int(res.headers['content-length'])

            # 若当前报文长度小于前次报文长度，或者已接收文件等于当前报文长度，则可以认为视频接收完成

            if content_length < pre_content_length or (
                    os.path.exists(file_path) and os.path.getsize(file_path) >= content_length):
                break

            pre_content_length = content_length

            # 写入收到的视频数据
            # print(res.content)

            with open(file_path, 'wb') as file:

                file.write(res.content)

                file.flush()

                print('receive data，file size : %d   total size:%d' % (os.path.getsize(file_path), content_length))
        return os.path.getsize(file_path)
    except Exception as e:

        dic = {'url': url, 'file_path': file_path}

        print("下载失败:", dic)


def downloading(m3u8_path, file_path):
    m3u8_length = len(m3u8_path)
    print('共需下载{}个ts文件'.format(m3u8_length))
    for i, v in enumerate(m3u8_path):
        print(v)
        k = i + 1
        if m3u8_length < 100:
            if k < 10:
                k = '0' + str(k)
        elif 100 < m3u8_length < 1000:
            if k < 10:
                k = '00' + str(k)
            elif 10 <= k < 100:
                k = '0' + str(k)
        elif 1000 < m3u8_length < 10000:
            if k < 10:
                k = '000' + str(k)
            elif 10 <= k < 100:
                k = '00' + str(k)
            elif 100 <= k < 1000:
                k = '0' + str(k)
        # print(k)
        file_name = '/' + str(k) + '.ts'
        res = download_video(v, file_path + file_name)
        print('当前已下载第{}个文件, 大小 = {}'.format(i + 1, res))


def main():
    start = time.time()

    request_url_header = "https://dtliving-sh.dingtalk.com/live_hp/"
    header = '文件名'  # 标题
    doc_name = '目录'
    path = '/home/ming/Documents/{}/{}'  # 本地目录创建

    map1 = dd.ts_path.replace("\n", "").split("#EXTINF:")
    map1.pop(0)
    map2 = []
    for m1 in map1:
        m2 = m1.split(",")
        map2.append(request_url_header + m2[1])

    if os.path.exists(path.format(doc_name, header)):
        pass
    else:
        os.mkdir(path.format(doc_name, header))

    downloading(map2, path.format(doc_name, header))

    end = time.time() - start
    print('下载完成，耗时：{}分{}秒'.format(int(end // 60), math.ceil(end % 60)))


if __name__ == '__main__':
    main()


# https://dtliving-sz.dingtalk.com/live_hp/fd275a57-1d50-4ae6-913f-9abaa849abc4_merge.m3u8?app_type=win&auth_key=1621476429-0-0-e2edac91ffde0b3e9346368efe7ea5a3&cid=5aa5de1834f7bdd695d9f40eac157b31&token=9f50b7559674af91dce8d8f47c9765ab-FqJjqI2bzQ93l_ha1sJtInj2gjeWNFkraLqvqN3d3X0sRnZ-ggk1-wyfhM64DEFc2dTtrEmp1TdULyewIiJH4k9QOf3xQzJaf3GCKfDt8Y=&token2=933924287fc4fbe4f080659a3b0d5b4f90aiKE0AN-YOTGG6wHCJ3cqcSLvM_U-VeIP1uH8mfl-_IuTQup9j6GtFU5mr-2AwGrmQn7HpLshyaW2l6DjVt-SikVpKZFUcMEtlD2bgwIg&version=6.0.12-Release.4140363