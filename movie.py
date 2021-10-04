import os
import requests
import time
import math
from threading import Thread

from concurrent.futures import ProcessPoolExecutor


def download_video(url, file_path):
    try:

        headers = {
            "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/87.0.4280.88 Safari/537.36'}

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

            with open(file_path, 'wb') as file:

                file.write(res.content)

                file.flush()

                print('receive data，file size : %d   total size:%d' % (os.path.getsize(file_path), content_length))
        return os.path.getsize(file_path)
    except Exception as e:

        dic = {'url': url, 'file_path': file_path}

        print("下载失败:", dic)


def downloading(m3u8_path, file_path):
    for i in range(1, 10000):
        k = i
        if i < 1000:
            if i < 100:
                if i < 10:
                    k = '000' + str(i)
                else:
                    k = '00' + str(i)
            else:
                k = '0' + str(i)
        res = download_video('{}/{}.ts'.format(m3u8_path, i),
                             '{}/{}.ts'.format(file_path, k))
        print('{}/{}.ts'.format(m3u8_path, i))
        print('当前已下载第{}个文件, 大小 = {}'.format(k, res))
        if type(res) is int:
            if res < 1000:
                break


def main():
    start = time.time()
    header = '3个点'    #标题
    url = 'http://alcdn.hls.xiaoka.tv/202121/c0a/a21/qLq_4JYYvGyr03lS/index.m3u8'    #m3u8地址
    path = '/Users/icourt1/Documents/阿国/{}'    #本地目录创建
    m3u8 = url.replace('/index.m3u8', '')
    if os.path.exists(path.format(header)):
        pass
    else:
        os.mkdir(path.format(header))

    # Thread(target=downloading, args=(m3u8, path.format(header))).start()
    downloading(m3u8, path.format(header))

    end = time.time() - start
    print('下载完成，耗时：{}分{}秒'.format(int(end // 60), math.ceil(end % 60)))


if __name__ == '__main__':
    main()
