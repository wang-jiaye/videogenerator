# TrushVideoGenerator

这波啊，这波是垃圾营销号视频生成。建议自己看一下源码，傻瓜操作，记得申请百度开发者API


可能是闲着太无聊，然而复习是不可能复习的，就做了一个这个玩意儿，改天进军UC和百家号（不会真有人用吧）

先看看效果：（1:20以后）


undefined

资源准备
分析一下平时能刷到的垃圾视频，可以发现有几个小特征：

文本格式固定，而且内容没有什么意义
语音是女性
视频一般都是一些什么自然风光，和文本也没有什么关联
有一个大家一听就知道是营销号的 BGM
这样的话，就可以开始找素材了
我们上B站找一段自然风光的拍摄视频

上B站找一段自然风光的拍摄视频（自己去找一个两分钟左右的，太短了不行，太长了没必要）(下文中用的video_ori.mp4)
找到营销号用的BGM（项目的Github上有我用的）（下文中的bgm.mp3）
注册百度开发者 （为了使用他们免费的文字转语音API）
生成营销号视频文案（等下你就知道了）
让我们现在就开始做吧（假设你已经有了背景视频和BGM）

生成营销号视频文案
def Generatetxt(somebody,something,other_word):
    txt = '''{}{}是怎么回事呢？{}相信大家一定很熟悉，
    但是{}{}是怎么回事呢，下面就让小编来带着大家一起了解吧！
	{}{}，其实就是{}，大家可能会很惊讶{}怎么会{}呢？但事实就是这样，
    小编也感到非常惊讶。就是关于{}{}的事情了，大家有什么想法呢，
    欢迎在评论区告诉小编来一起讨论哦！
    '''
    txt = txt.format(somebody,something,somebody,somebody,something,somebody,something,other_word,somebody,something,somebody,something)
    return txt
是不是感觉很熟悉，使用

print(Generatetxt("健身", "伤害身体", "运动过度肌肉会损伤"))
放一段生成品上来

健身伤害身体是怎么回事呢？健身相信大家一定很熟悉，但是健身伤害身体是怎么回事呢，下面就让小编来带着大家一起了解吧！
健身伤害身体，其实就是运动过度肌肉会损伤，大家可能会很惊讶健身怎么会伤害身体呢？但事实就是这样，小编也感到非常惊讶。
这就是关于健身伤害身体的事情了，大家有什么想法呢，欢迎在评论区告诉小编来一起讨论哦！

文本生成语音
首先需要安装 baidu-aip 库 (SDK)，直接pip install baidu-aip就好了

申请百度语音识别接入的开发者账号，网址：百度开发者，目的是为了获取AppID，API Key,Secret Key

这里使用的就是最简单的合成方法，具体使用可以去看他们的文档。免费生成中文语音可以用50000次，还是良心的

from aip import AipSpeech
def GenerateMP3(txt):
    #这里用你自己申请到的
    APP_ID = '**********'
    API_KEY = '**************'
    SECRET_KEY = '**************'
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    result = client.synthesis(txt, 'zh', 1, {
        'vol': 4, 'per': 0, 'spd': 5
    })
    if not isinstance(result, dict):
        with open('./sound.mp3', 'wb') as f:
            f.write(result)
我直接保存到代码文件目录的sound.mp3，可以自己修改一下各项参数。包括语音的速度，语调，音量等等。

语音+bgm+背景视频 融合
这个地方我踩了好多坑，不知道为什么我用subprocess调用ffmpeg总是出毛病，pydub库也总是报json文件错误。所以我选择了moviepy库

moviepy官方文档
这个库还是蛮好用的，就是网上的中文文案还在制作中，很多东西还得去官方文档搜英文说明。

先把代码放一下：

def video_add_mp3(file_name, mp31_file,mp32_file,new_filename, time):
    video = VideoFileClip(file_name)
    audioclip = AudioFileClip(mp31_file)
    audioclip2 = AudioFileClip(mp32_file)
    compo = CompositeAudioClip([audioclip.set_start(2),
                                audioclip2.set_start(0)])
    #print(type(compo)
    videoclip = video.set_audio(compo)
    videoclip = videoclip.subclip(0, time)
    try:
        videoclip.write_videofile(new_filename)
        video.reader.close()
        return new_filename
    except:
        traceback.print_exc()
    return None
应该很容易读懂，构建两个AudioFileClip对象，作为bgm和语音；构建一个VideoFileClip作为视频图像。然后两个音频融合，BGM先播放，语音2秒后播放，再把视频剪成参数中的time秒，这个时间和视频剪辑的函数下面会说到:

视频剪辑：

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
没什么技术含量了

获取MP3的长度：

def get_mp3length(path):
    audio = MP3(path)
    return audio.info.length
整体代码：
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
    APP_ID = '19503166'
    API_KEY = 'lbpVQwLvZdC0F0FKB3Gu6ylg'
    SECRET_KEY = 'jdK6EgQOKzkSyjVfP93CeerELedFl71u'
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


def video_add_mp3(file_name, mp31_file,mp32_file,new_filename, time):
    video = VideoFileClip(file_name)
    audioclip = AudioFileClip(mp31_file)
    audioclip2 = AudioFileClip(mp32_file)
    compo = CompositeAudioClip([audioclip.set_start(2),
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
    print(Generatetxt("健身", "伤害身体", "运动过度肌肉损伤"))
    GenerateMP3(Generatetxt("健身", "伤害身体", "运动过度肌肉损伤"))
    Mp3TimeLength = get_mp3length("sound.mp3")
    video_add_mp3("video_ori.mp4", 'sound.mp3','bgm.mp3','After.mp4',Mp3TimeLength + 3)
就这样了8
