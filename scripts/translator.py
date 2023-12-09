from googletranslatepy import Translator

trans: Translator
delimiter = ";"


def init(proxy=""):
    global trans  # Use the global 'trans' variable
    print("使用代理：" + proxy)
    trans = Translator(proxies=proxy)


def handler(text):
    results = split_string_with_delimiter(text)
    texts = []
    for result in results:
        texts.append(trans.translate(result, dest="zh-cn"))

    return delimiter.join(texts).replace("；", delimiter)


def split_string_with_delimiter(input_str, max_length=5000):
    """
    将输入字符串按照指定的分隔符分割，每段不超过指定长度
    """
    result = []
    current_segment = ""

    for part in input_str.split(delimiter):
        if len(current_segment) + len(part) + len(delimiter) <= max_length:
            current_segment += part + delimiter
        else:
            result.append(current_segment[:-len(delimiter)])  # 去掉末尾的分隔符
            current_segment = part + delimiter

    if current_segment and current_segment != delimiter:
        result.append(current_segment[:-len(delimiter)])  # 处理最后一段

    return result
