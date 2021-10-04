import os
import requests
import time
import math


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


def main():
    start = time.time()
    header = 'pythonDownloads'    #标题
    #m3u8文件
    url = 'https://github.com/MustangYM/WeChatExtension-ForMac/archive/refs/tags/v2.8.4.zip'
    path = '/Users/icourt1/Downloads/{}'    #本地目录创建
    if os.path.exists(path.format(header)):
        pass
    else:
        os.mkdir(path.format(header))

    # Thread(target=downloading, args=(m3u8, path.format(header))).start()
    download_video(url, '{}/{}'.format(path.format(header), 'v2.8.4.zip'))

    end = time.time() - start
    print('下载完成，耗时：{}分{}秒'.format(int(end // 60), math.ceil(end % 60)))


if __name__ == '__main__':
    main()

