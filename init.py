from scripts import hander, translator, translatorFileName

path = r"C:\Users\lsjspl\aaa\【教程】Blender_超写实角色"

#配置和初始化翻译代理
translator.init(proxy="http://127.0.0.1:10809")
#处理视频字幕
hander.start(path, "float32", "medium")

# 翻译和重命名文件名
translatorFileName.handler(path)
