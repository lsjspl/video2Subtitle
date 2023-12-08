from googletranslatepy import Translator

translator = Translator(proxies="http://127.0.0.1:10809")
#

# print(translator.translate('hello.',dest="zh-cn"))
# # <Translated src=ko dest=en text=Good evening. pronunciation=Good evening.>
# print(translator.translate('안녕하세요.', dest='ja'))
# # <Translated src=ko dest=ja text=こんにちは。 pronunciation=Kon'nichiwa.>
# print(translator.translate('veritas lux mea', src='la'))

def handler(text):
    return translator.translate(text, dest="zh-cn")


print(handler("hellow"))