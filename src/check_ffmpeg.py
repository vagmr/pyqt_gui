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
from py7zr import SevenZipFile


def download_ffmpeg():
    print("检测到ffmpeg依赖缺失，准备下载...")
    url = "https://i-020.wwentua.com:446/02202300164417410bb/2024/02/20/8819d16ebdc07bf36f34ccbef58c0933.7z?st=xjNxRvj517R-xZDu-vbl6w&e=1708444450&b=CT0MalQ5ViNRYVFgA30DMFV6&fi=164417410&pid=18-141-190-145&up=2&mp=0&co=0"
    ffmpeg_dir = "dependence"
    from VChange import config_file_save_path
    ffmpeg_archive = path.join(config_file_save_path, ffmpeg_dir)
    file_path = path.join(ffmpeg_archive, "ffmpeg.7z")
    if not path.exists(ffmpeg_archive):
        makedirs(ffmpeg_dir)
        print("创建依赖目录完成，开始下载ffmpeg...")
    if path.isfile(file_path):
        print("开始解压ffmpeg...")
        try:
            with SevenZipFile(file_path, mode="r") as z:
                z.extractall(ffmpeg_archive)
        except Exception:
            raise Exception("解压失败,请尝试手动解压")
        return
    res = get(url, stream=True)
    total_size = int(res.headers.get("content-length", 0))
    block_size = 1024
    with open(file_path, "wb") as file, tqdm(
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
    with SevenZipFile(file_path, mode="r") as z:
        z.extractall(ffmpeg_archive)
    print("解压成功")


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
