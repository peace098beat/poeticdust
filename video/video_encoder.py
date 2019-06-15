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
    outfilename = os.path.join("thumb", _outfilename)

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


    debug = "581460059_874673.mp4"




    import glob
    import shutil

    # ファイル名に"."が複数ある場合は"_"に置換
    paths = glob.glob( "*.mp4" )
    for path in paths:

        parts = path.split(".")
        if len(parts) == 3:
            old_name = path
            new_name = parts[0] + "_" + parts[1] + "." + parts[2]
            os.rename(old_name, new_name)
            print("[rename] ", new_name)

    err_cnt = 0
    paths = glob.glob( "*.mp4" )
    for path in paths:
        print("[Rotate] ", path)
        
        # 縦長の映像を左回転
        try:
            w, h = probe_video_size(path)
            if w < h:
                transpose(path)
            else:
                print("copy")
                shutil.copy(path, os.path.join("transpose",os.path.basename(path)))

        except (KeyError, IndexError) as e:
            err_cnt+=1
            print(e.args)
            with open("error.log", "a") as fp:
                fp.write("{}".format(e))

    exit()
    paths = glob.glob( "*.mp4" )
    for path in paths:

        # サムネイルを作成
        thumbnail(path)

    print("fin")



