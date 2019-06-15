#! coding: utf-8
"""
analysis.py
fffmpgeを使って、動画を整理する
1. metaファイルを吐き出し
2. 縦横比を計算. 縦なら横にする.

:library:
    [kkroening/ffmpeg-python - github](https://github.com/kkroening/ffmpeg-python)
    [ffmpeg-pythonを使ってみた - Qiita](https://qiita.com/ayumu838/items/4f20d47ca7e9f5fbcfca)

"""
import os
import ffmpeg
import json
import subprocess


def change_dirname(filename, new_dirname):

    basename = os.path.basename(filename)
    dirname = os.path.dirname(filename)

    new_filename = os.path.join(new_dirname, basename)

    return new_filename



def thumbnail(filename):
    """ サムネイル
    ffmpeg -i video1.mp4 -vf thumbnail=300 -frames:v 1 thumbnail.jpg
    ffmpeg -i video1.mp4 -vf thumbnail=300,scale=320:-1 -frames:v 1 thumbnail-s1.jpg -y
    ffmpeg -i video1.mp4 -vf thumbnail=300,scale=320:-2 -frames:v 1 thumbnail-s2.jpg -y
    ffmpeg -i video1.mp4 -vf thumbnail=300,scale=320:-4 -frames:v 1 thumbnail-s4.jpg -y
    ffmpeg -i video1.mp4 -vf thumbnail,scale=320:-4 -frames:v 3 -vsync 0 thumbnail-s%03d.jpg -y
    """

    # outputfile
    dirname = os.path.dirname(filename)
    base = os.path.basename(filename).split(".")[0]
    _outfilename = base + "-thumb%03d.jpg"
    _outfilename = os.path.join("thumb", _outfilename)
    outfilename = change_dirname(_outfilename, "thumb")

    args = ["ffmpeg"]
    args += ["-i", filename]
    args += ["-vf", "thumbnail,scale=320:-1"]
    args += ["-frames:v", "3", "-vsync", "0"]
    args += [outfilename]
    args += ["-y"]

    p =subprocess.Popen(args)
    out, err = p.communicate()
    
    if p.returncode != 0:
        print("thumbnail args:", args)
        print("thumbnail err:", err)
        raise Exception("thumbnail error")


if __name__ == '__main__':

    import glob
    import shutil


    paths = glob.glob( os.path.join("encoded", "*.mp4" ) )

    for i, path in enumerate(paths):

        # サムネイルを作成
        thumbnail(path)

    print("fin")



