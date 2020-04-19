from aip import AipSpeech
from mutagen.mp3 import MP3
from moviepy.editor import *
import traceback

def Generatetxt(somebody,something,other_word):
    txt = '''{}{}是怎么回事呢？{}相信大家一定很熟悉，但是{}{}是怎么回事呢，下面就让小编来带着大家一起了解吧！
{}{}，其实就是{}，大家可能会很惊讶{}怎么会{}呢？但事实就是这样，小编也感到非常惊讶。
这就是关于{}{}的事情了，大家有什么想法呢，欢迎在评论区告诉小编来一起讨论哦！
    '''
    txt = txt.format(somebody,something,somebody,somebody,something,somebody,something,other_word,somebody,something,somebody,something)
    return txt
def GenerateMP3(txt):

	#这里用自己申请的百度的API一系列的
	
    APP_ID = '*********'
    API_KEY = '******************'
    SECRET_KEY = '******************'
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    result = client.synthesis(txt, 'zh', 1, {
        'vol': 4, 'per': 0, 'spd': 5
    })
    if not isinstance(result, dict):
        with open('./sound.mp3', 'wb') as f:
            f.write(result)

def get_mp3length(path):
    audio = MP3(path)
    return audio.info.length


def VideoClip(filename, start=0, end=None):
    tmp_name = filename.split('.')
    new_filename = tmp_name[0] + '_clip.' + tmp_name[1]
    video = VideoFileClip(filename)
    try:
        result = video.subclip(start, end)
        result.write_videofile(new_filename)
        video.reader.close()
        return new_filename
    except:
        traceback.print_exc()
    return None

def video_add_mp3(file_name, mp31_file,mp32_file,new_filename, time):

    video = VideoFileClip(file_name)
    audioclip = AudioFileClip(mp31_file)
    audioclip2 = AudioFileClip(mp32_file)
    compo = CompositeAudioClip([audioclip.set_start(1),
                                audioclip2.set_start(0)])
    print(type(compo))

    videoclip = video.set_audio(compo)
    videoclip = videoclip.subclip(0, time)
    try:
        videoclip.write_videofile(new_filename)
        video.reader.close()
        return new_filename
    except:
        traceback.print_exc()
    return None


if __name__ == '__main__':
    GenerateMP3(Generatetxt(somebody = '这个玩意儿',something = '生成垃圾营销号文章',other_word = '爷很无聊'))
    Mp3TimeLength = get_mp3length("sound.mp3")
    video_add_mp3("video_ori.mp4", 'sound.mp3','bgm.mp3','After.mp4',Mp3TimeLength + 2)






