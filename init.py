from scripts import hander, translator

path = r"D:\Mr5\Downloads\【教程】Blender ：超写实角色"

translator.init(proxy="http://127.0.0.1:10809")
hander.start(path, "float32", "medium")

# 翻译和重命名文件名
# translatorFileName.handler(path)
