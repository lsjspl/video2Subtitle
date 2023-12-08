from googletranslatepy import Translator

trans: Translator


def init(proxy=""):
    global trans  # Use the global 'trans' variable
    print("使用代理：" + proxy)
    trans = Translator(proxies=proxy)


def handler(text):
    return trans.translate(text, dest="zh-cn")
