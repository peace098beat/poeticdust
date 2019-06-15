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
    args += ["-vf", "transpose=2"]
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

        print("[{:03d}][transposer]".format(i, path))
        
        # 縦長の映像を左回転
        try:
            w, h = probe_video_size(path)
            if w < h:
                transpose(path, overwrite=False)
            else:
                dist = os.path.join("transposed",os.path.basename(path))
                if not os.path.exists(dist):
                    shutil.copy(path, dist)

        except (KeyError, IndexError) as e:
            print(path)
            err_cnt+=1
            print(e.args)
            with open("error.log", "a") as fp:
                fp.write("{}".format(e))



    # 成功率を表示
    paths = glob.glob( os.path.join("transposed", "*.mp4" ) )
    Nt = len(paths)     
    print("[Stat] {} / {}".format(Nt, N))

