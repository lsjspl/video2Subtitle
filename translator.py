from googletranslatepy import Translator

translator: Translator

def init(proxy=""):
    print("使用代理："+proxy)
    translator = Translator(proxies=proxy)


def handler(text):
    return translator.translate(text, dest="zh-cn")
