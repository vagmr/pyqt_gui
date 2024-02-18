"""
@文件        :check_ffmpeg.py
@说明        : 
@时间        :2024/02/18 16:23:28
@作者        :vagmr
@版本        :1.1
"""

from subprocess import run, PIPE
from tqdm import tqdm
from requests import get
from shutil import unpack_archive
from os import path, makedirs


def download_ffmpeg():
    print("检测到ffmpeg依赖缺失，准备下载...")
    url = "https://s-62.lanzog.com/02181600131395686bb/2023/08/12/165052748ff29c9b1ffae44fb9ebf8c5.7z?st=_smjJNxVrpalshRArL9jGg&e=1708246360&b=CT0IbghlUyYENFFgUSxTJVVlCjpRNQRjAiILYwErUTVTdA5iUj5UfwRmACw_c&fi=131395686&pid=172-233-81-80&up=2&mp=0&co=0"
    ffmpeg_dir = "dependence"
    from VChange import application_path
    ffmpeg_archive = path.join(application_path, ffmpeg_dir)
    if not path.exists(ffmpeg_archive):
        makedirs(ffmpeg_dir)
        print("创建依赖目录完成，开始下载ffmpeg...")
    res = get(url, stream=True)
    total_size = int(res.headers.get("content-length", 0))
    block_size = 1024
    with open("ffmpeg.7z", "wb") as file, tqdm(
        desc="Downloading",
        total=total_size,
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in res.iter_content(block_size):
            size = file.write(data)
            bar.update(size)
    # 解压
    print("开始解压ffmpeg...")
    unpack_archive("ffmpeg.7z", ffmpeg_archive)


def is_ffmpeg_installed():
    """
    确认ffmpeg是否已安装
    """
    try:
        result = run(["ffmpeg", "-version"],
                     stdout=PIPE, stderr=PIPE, text=True)
        print(f"ffmpeg version: {result.stdout}")
        return "ffmpeg version" in result.stdout
    except FileNotFoundError:
        return False


if __name__ == "__main__":
    download_ffmpeg()
