import os

from faster_whisper import WhisperModel
import logging


# or run on GPU with INT8
# model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
# or run on CPU with INT8
# model = WhisperModel(model_size, device="cpu", compute_type="int8")
def start(folder_path, computeType):
    logging.basicConfig()
    logging.getLogger("faster_whisper").setLevel(logging.DEBUG)
    # model_size = "large-v3"
    model_size = "medium"
    print(f"加载{model_size}。。。。")
    # Run on GPU with FP16
    model = WhisperModel(model_size, device="cuda", compute_type=computeType)
    result_array1, result_array2 = walkFiles(folder_path)
    for videoPath, srtPath in zip(result_array1, result_array2):
        create(videoPath, srtPath, model)


def walkFiles(folder_path):
    videoPaths = list()
    srtPaths = list()
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for file_name in files:
            videoPath = os.path.join(root, file_name)
            if videoPath.lower().endswith(".mp4"):
                srtPath = os.path.join(root, os.path.splitext(os.path.basename(videoPath))[0] + ".srt")
                if os.path.exists(srtPath):
                    print("跳过"+srtPath)
                    continue
                videoPaths.append(videoPath)
                srtPaths.append(srtPath)
    return videoPaths, srtPaths


def create(videoPath, srtPath, model):
    segments, info = model.transcribe(
        audio=videoPath,
        beam_size=5,
        # language="zh",
        # initial_prompt="简体",
        # vad_parameters=dict(min_silence_duration_ms=500) ,
        condition_on_previous_text=True,
        vad_filter=True,
        suppress_tokens = [],
        temperature=0,
    )
    print("Detected language '%s' with probability %f" % (info.language, info.language_probability))
    print(videoPath)
    print(srtPath)



    tmp=os.path.join(os.path.dirname(srtPath),"tmp.srt")
    if os.path.exists(tmp):
        os.remove(tmp)
    index = 0
    with open(tmp, 'w', encoding='utf-8') as file:
        for segment in segments:
            index = index + 1
            text = segment.text
            content = "[%.2fs -> %.2fs] %s" % (segment.start, segment.end, text)
            print(content)
            file.write(f"{index}\n{segment.start} --> {segment.end}\n{text}\n\n")

    os.rename(tmp, srtPath)
