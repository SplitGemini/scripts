import os
import sys
import regex as re
import subprocess
import utils

"""
crf值实在太玄学了，只能靠经验
原视频2000k，crf设为23大概也是2000k，每减小6翻倍
"""
def twoPass(path, bitrate, output):
    passlogfile = os.path.splitext(path)[0]
    command = 'ffmpeg -y -hide_banner -i "{}" -strict -2 -passlogfile "{}" -c:v libx264 -r 23.976 -pass 1 -an -f rawvideo "NUL"'.format(path, passlogfile, bitrate)
    subprocess.run(command)
    command = 'ffmpeg -y -hide_banner -i "{}" -c:v libx264 -r 23.976 -pass 2 -b:v {} -preset slow -b:a 128k -profile:v high -passlogfile "{}" "{}"'.format(path, bitrate, passlogfile, output)
    subprocess.run(command)
    if os.path.exists(passlogfile+'-0.log'):
        os.remove(passlogfile+'-0.log')
        os.remove(passlogfile+'-0.log.mbtree')


def getOriginBitrate(path):
    result = subprocess.Popen('ffprobe -hide_banner "{}"'.format(path), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    alist = [x.decode('utf-8').replace('\n', '').strip() for x in result.stdout.readlines()]
    for i in alist:
        if not "Video" in i:
            continue
        #  Stream #0:0: Video: mpeg4 (DX50 / 0x30355844), yuv420p, 720x544 [SAR 1:1 DAR 45:34], 1348 kb/s ......
        # 从这里面匹配出数据速率，即码率
        bitrate = re.match(r"Stream #[0-9]:[0-9](?:\([\w\-]+\))?: Video:.*?(?<=, )([0-9]+)(?= kb/s).*", i, re.I|re.L)
        if bitrate:
            return bitrate.group(1)
        else:
            continue
    print('Have not catched bitrate...')
    sys.exit(0)


def crfTransfer(path, crf, output):
    command = 'ffmpeg -y -hide_banner -i "{}" -c:v libx264 -crf {} -preset slow -profile:v high -r 23.976 -c:a aac -b:a 128k "{}"'.format(path, crf, output)
    subprocess.run(command)


def codecCopy(path, output):
    command = 'ffmpeg -y -hide_banner -i "{}" -codec copy "{}"'.format(path, output)
    subprocess.run(command)
    
    
def resolveBitrate(bitrate, k):
    if k:
        if 'k' == bitrate.lower()[-1]:
            return bitrate.lower()
        else:
            return bitrate+'k'
    else:
        return bitrate.lower().replace('k','')

def resolveFile(p, args):
    """procees media file"""
    print("Start transfer video \"{}\"\n".format(p))
    if args.output:
        if not os.path.exists(os.path.dirname(args.output)):
            os.mkdir(os.path.dirname(args.output))
        output = os.path.join(os.path.dirname(args.output), os.path.basename(p))
    else:
        output = os.path.splitext(p)[0]+'_compresion.mp4' \
                    if os.path.exists(os.path.splitext(p)[0]+'.mp4') \
                    else os.path.splitext(p)[0]+'.mp4'
    if args.bitrate:
        twoPass(p, resolveBitrate(args.bitrate, True) \
            if not args.bitrate == '0' \
            else resolveBitrate(getOriginBitrate(p), True), output)
    elif args.crf:
        crfTransfer(p, args.crf, output)
    elif os.path.splitext(p)[-1].lower() == '.ts':
        codecCopy(p, output)
    else:
        crfTransfer(p, 23, output)


def main():
    import argparse
    parser = argparse.ArgumentParser(description='转换且压缩该文件夹下的视频到mp4格式')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-2', '--bitrate', nargs='?', const='0',
            help='Use 2pass, Specified a bitrate or not for output videos, else use crf(default).Default use origin bitrate.')
    group.add_argument('-c', '--crf', type=int, nargs='?', const=23,
            help='Crf of output videos, recommand in range 18-28, default is 23')
    parser.add_argument('-o', '--output',
            help='Specified an output directory.')
    parser.add_argument('-in', '--include', action="store_true", default=False,
            help='Include mp4, mkv, webm videos.')
    # any paths
    parser.add_argument('paths', nargs='*', default=[], help='Input paths', metavar='Any input paths.')
    args = parser.parse_args()

    
    video_types = ['.wmv', '.avi', '.ts', '.rmvb', '.asf', '.flv', '.mov'] 
    if args.include :
        video_types.extend(['.mp4', '.mkv', '.webm'])
        
    print("Config: \n\tMode: {},\n\tOutput Direrctory: \"{}\",\
           \n\tNow surported video types list:\n\t {}\n"
         .format("2 Pass, bitrate={}".format(
                    resolveBitrate(args.bitrate, True) \
                        if args.bitrate != '0' \
                        else "Use origin video bitrate") \
                            if args.bitrate \
                            else "CRF, value={}".format(args.crf if args.crf  else '23'), 
                 args.output if args.output  else "Use origin video same dierctory",
                 video_types))
    paths = set(args.paths)
    if len(paths) != 0:
        dirs = []
        for dir in paths:
            if os.path.exists(dir):
                if os.path.isdir(dir):
                    dirs.append(dir)
                elif os.path.splitext(dir)[-1].lower() in video_types:
                    resolveFile(dir, args)
                else:
                    print("Path \"{}\" not surported, check if it's a video or \"-in\" argument is setted.".format(dir))
            else:
                print("Path \"{}\" doesn't exists.".format(dir))
    else:
        dirs = [os.getcwd()]
    for cwd in dirs:
        print("CWD: \"{}\"".format(cwd))
        for p in os.listdir(cwd):
            p = os.path.join(cwd ,p)
            if os.path.isfile(p):
                if os.path.splitext(p)[-1].lower() in video_types:
                    resolveFile(p, args)
                    print("\nTransfered video \"{}\" to \"{}\"\n".format(p, output))
        print('Finished.')


if __name__ == '__main__':
    main()
    utils.waitIfNotInWindowsTerminal()
