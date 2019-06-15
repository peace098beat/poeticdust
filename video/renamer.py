
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

def change_basename(filepath, new_basename):
    basename = os.path.basename(filepath)
    dirname = os.path.dirname(filepath)
    new_filepath = os.path.join(dirname, new_basename)
    return new_filepath


if __name__ == '__main__':

    import glob
    import shutil

    # ファイル名に"."が複数ある場合は"_"に置換
    paths = glob.glob( os.path.join("origin","*.mp4" ))

    for i, old_path in enumerate(paths):

        # new name
        new_name = "poeticdust-1905_{:03d}.mp4".format(i+1)
        new_path = change_basename(old_path, new_name)

        print(old_path, new_path)
        os.rename(old_path, new_path)

        # parts = path.split(".")
        # if len(parts) == 3:
        #     old_name = path
        #     new_name = parts[0] + "_" + parts[1] + "." + parts[2]
        #     os.rename(old_name, new_name)
        #     print("[rename] ", new_name)

    
    print("total: ", len(paths))