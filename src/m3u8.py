"""
@文件        :m3u8lib.py
@说明        :m3u8文件解析处理库 
@时间        :2024/04/21 18:32:30
@作者        :vagmr
@版本        :1.1
"""

from typing import Union
import m3u8
import os
import requests
import concurrent.futures
import sys


class M3u8Lib:
    """
    m3u8文件解析处理类

    methods:
     -parse_m3u8(m3u8_file_path:str) -> m3u8.M3U8: 解析m3u8文件

    """

    def __init__(self) -> None:
        super().__init__()
        self.downloadPath = ''
        self.fileName = ''

    def change_path(self, downloadPath, fileName='video'):
        """
        修改下载路径和文件名


        :param downloadPath: 下载文件的根目录
        :param fileName: 文件名
        :return: None
        """
        self.downloadPath = downloadPath
        self.fileName = fileName

    def parse_m3u8(self, m3u8_file_path: str) -> Union[m3u8.M3U8, None]:
        """
        解析m3u8文件

        :param m3u8_file_path: m3u8文件路径
        :return: m3u8.M3U8对象
        """
        m3u8_obj = m3u8.load(m3u8_file_path)
        # 判断是否为变体播放列表
        if m3u8_obj.is_variant:
            m3u8_obj = m3u8_obj.playlists
            # 取第一个子播放列表
            if len(m3u8_obj) > 0:
                sub_obj = m3u8_obj[0]
                # 取子播放列表的绝对路径
                subM3u8Url = sub_obj.absolute_uri
                # 递归解析子播放列表
                return self.parse_m3u8(subM3u8Url)
            else:
                return None
        else:
            return m3u8_obj

    def getUrlLastPath(self, url):
        """
        获取url最后一级路径


        :param url: url字符串
        :return: 最后一级路径字符串
        """
        return url.split('/')[-1]

    def getFileUrlsAndPaths(self, playlist: m3u8.M3U8):
        allUrls = []
        allFilePaths = []
        tempPath = self.tempPath(self.downloadPath, self.fileName)
        for seg in playlist.segments:
            if seg == None:
                break
            allUrls.append(seg.absolute_uri)
            na = tempPath + '/' + self.getUrlLastPath(seg.absolute_uri)
            allFilePaths.append(na)

        for key in playlist.keys:
            if key == None:
                break
            allUrls.append(key.absolute_uri)
            na = tempPath + '/' + self.getUrlLastPath(key.absolute_uri)
            allFilePaths.append(na)
        return allUrls, allFilePaths

    def tempPath(self, downloadPath, fileName):
        """
        构造一个临时路径,用于存储下载的文件

        :param downloadPath: 下载文件的根目录
        :param fileName: 文件名
        :return: 临时路径字符串
        """
        return downloadPath + '/' + fileName + '_temp'
    # 创建本地m3u8文件，用于ffmpeg的ts合并以及转码mp4

    def createNativeM3u8File(self, playlist, m3u8Path):

        for seg in playlist.segments:
            if seg == None:
                break
            seg.uri = self.getUrlLastPath(seg.absolute_uri)

        for key in playlist.keys:
            if key == None:
                break
            key.uri = self.getUrlLastPath(key.absolute_uri)

        playlist.dump(m3u8Path)

    def print_progress(self, file_path, bytes_received, file_size):
        """
        打印下载进度

        :param file_path: 文件路径
        :param bytes_received: 已下载字节数
        :param file_size: 文件大小
        :return: None
        """
        percent = min(100, int(bytes_received * 100 / file_size))
        bar_length = 20
        filled_length = int(bar_length * percent // 100)
        bar = '=' * filled_length + '-' * (bar_length - filled_length)
        sys.stdout.write(f"\r[{bar}] {percent}% {file_path}")
        sys.stdout.flush()
        if percent == 100:
            sys.stdout.write("\n")

    def download_file(self, url, file_path):
        """
        下载单个文件

        :param url: 文件URL
        :param file_path: 保存路径
        :return: None
        """
        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                total_size = int(response.headers.get('content-length', 0))
                block_size = 1024
                progress = 0
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=block_size):
                        if chunk:
                            f.write(chunk)
                            progress += len(chunk)
                            self.print_progress(
                                file_path, progress, total_size)
        except Exception as e:
            print(f"Error downloading {url}: {e}")

    def download_files(self, urls, file_paths, max_workers=8):
        """
        并行下载多个文件

        :param urls: 文件URL列表
        :param file_paths: 保存路径列表
        :param max_workers: 最大线程数
        :return: None
        """
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(self.download_file, url, file_path)
                       for url, file_path in zip(urls, file_paths)]
            concurrent.futures.wait(futures)
            print("All files downloaded successfully!")


if __name__ == '__main__':
    pass
