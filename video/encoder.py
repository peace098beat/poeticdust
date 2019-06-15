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



def probe(filename, cmd='ffprobe', **kwargs):
    args = ["ffprobe", "-show_format", "-show_streams", "-of", "json"]
    args += [filename]

    p =subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    
    if p.returncode != 0:
        print("myprobe err:", err[0:40])
        raise Exception("ffprobe error")

    return(json.loads(out.decode("utf-8")))


def probe_video_size(filename):

    body = probe(filename)

    streams = body["streams"]

    for media in streams:
        if "width" in media:
            w = media["width"]
            h = media["height"]
            return (w, h)


def change_dirname(filename, new_dirname):

    basename = os.path.basename(filename)
    dirname = os.path.dirname(filename)

    new_filename = os.path.join(new_dirname, basename)

    return new_filename

def encoder(filename, overwrite=True):
    """
    音声ファイルを除去
    映像をH264にする
    """

    # outputfile
    # dirname = os.path.dirname(filename)
    # base = os.path.basename(filename)
    # ext = os.path.basename(filename).split(".")[1]
    # _outfilename = base + "." + ext
    # outfilename = os.path.join("encoded", base)

    outfilename = change_dirname(filename, "encoded")


    if os.path.exists(outfilename) and overwrite==False:
        print("[INFO] {} is exists. process skip".format(outfilename))
        return None

    args = ["ffmpeg"]
    args += ["-i", filename]
    args += ["-codec:v", "h264"]
    args += ["-an"]
    args += [outfilename]

    if overwrite:
        args += ["-y"]

    p =subprocess.Popen(args, shell=True)
    out, err = p.communicate()
    
    if p.returncode != 0:
        print("encoded err:", args)
        print("encoded err:", err)
        raise Exception("encoded error")



if __name__ == '__main__':


    import glob
    import shutil

    err_cnt = 0
    
    paths = glob.glob( os.path.join("transposed", "*.mp4" ) )
    N = len(paths)

    for i, path in enumerate(paths):

        print("[{:03d}][Encode]".format(i, path))

        encoder(path, overwrite=False)


    # 成功率を表示
    paths = glob.glob( os.path.join("encoded", "*.mp4" ) )
    Nt = len(paths)     
    print("[Stat] {} / {}".format(Nt, N))

