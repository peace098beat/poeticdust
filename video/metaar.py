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

def change_ext(filename, new_ext):
    dirname = os.path.dirname(filename)
    basename = os.path.basename(filename).split(".")[0]
    ext = os.path.basename(filename).split(".")[1]
    return os.path.join(dirname, basename + new_ext)


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
    print(body)
    w = body["streams"][1]["width"]
    h = body["streams"][1]["height"]

    return (w, h)



def transpose(filename, overwrite=True):
    """90単位で回転
    $ ffmpeg -i input.mp4 -vf "transpose=1" output.mp4
    """

    # outputfile
    dirname = os.path.dirname(filename)
    base = os.path.basename(filename)
    # ext = os.path.basename(filename).split(".")[1]
    # _outfilename = base + "." + ext
    outfilename = os.path.join("transposed", base)


    if os.path.exists(outfilename) and overwrite==False:
        print("[INFO] {} is exists. process skip".format(outfilename))
        return None

    args = ["ffmpeg"]
    args += ["-i", filename]
    args += ["-vf", "transpose=3"]
    args += [outfilename]
    if overwrite:
        args += ["-y"]

    p =subprocess.Popen(args, shell=True)
    out, err = p.communicate()
    
    if p.returncode != 0:
        print("transpose err:", args)
        print("transpose err:", err)
        raise Exception("transpose error")



if __name__ == '__main__':


    import glob
    import shutil

    err_cnt = 0
    
    paths = glob.glob( os.path.join("origin", "*.mp4" ) )
    N = len(paths)

    for i, path in enumerate(paths):

        # 縦長の映像を左回転
        info = probe(path)
        print(info)

        dumpfile = change_ext(path, ".meta")

        with open(dumpfile, "w") as fp:
            # json.dump(info, fp)
            json.dump(info, fp, indent=4, sort_keys=True, separators=(',', ': '))
