from faster_whisper import WhisperModel
from opencc import OpenCC
import logging

def traditional_to_simplified(traditional_text):
    cc = OpenCC('t2s')  # 't2s' 表示从繁体到简体
    simplified_text = cc.convert(traditional_text)
    return simplified_text


#pip install faster-whisper
logging.basicConfig()
logging.getLogger("faster_whisper").setLevel(logging.DEBUG)
model_size = "large-v3"

# Run on GPU with FP16
model = WhisperModel(model_size, device="cuda", compute_type="int8")

# or run on GPU with INT8
# model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
# or run on CPU with INT8
# model = WhisperModel(model_size, device="cpu", compute_type="int8")

segments, info = model.transcribe(audio="D:\Mr5\Downloads\【教程】Blender ：超写实角色\视频教程+中文字幕\第2章\C02L18_pore-depth-testing.mp4",
                                  beam_size=5,
                                  language="zh"
                                  )

print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

for segment in segments:
    print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, traditional_to_simplified(segment.text)))