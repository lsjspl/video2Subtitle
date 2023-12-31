import os

from faster_whisper import WhisperModel
import logging
from scripts import translator


# or run on GPU with INT8
# model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
# or run on CPU with INT8
# model = WhisperModel(model_size, device="cpu", compute_type="int8")
def start(folder_path, computeType, modelSize="medium"):
    logging.basicConfig()
    logging.getLogger("faster_whisper").setLevel(logging.DEBUG)
    # model_size = "large-v3"
    # model_size = "medium"
    model_size = modelSize
    print(f"加载{model_size}。。。。")
    # Run on GPU with FP16
    model = WhisperModel(model_size, device="cuda", compute_type=computeType)
    result_array1, result_array2 = walkFiles(folder_path)
    for videoPath, srtPath in zip(result_array1, result_array2):
        create(videoPath, srtPath, model)


def walkFiles(folder_path):
    videoPaths = list()
    srtPaths = list()
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            videoPath = os.path.join(root, file_name)
            if videoPath.lower().endswith(".mp4"):
                srtPath = os.path.join(root, os.path.splitext(os.path.basename(videoPath))[0] + ".srt")

                if os.path.exists(srtPath):
                    print("跳过" + srtPath)
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
        vad_parameters=dict(min_silence_duration_ms=500),
        condition_on_previous_text=True,
        vad_filter=True,
        temperature=0,
    )

    print("Detected language '%s' with probability %f" % (info.language, info.language_probability))
    print(videoPath)
    print(srtPath)

    srtSourcePath = os.path.join(os.path.dirname(srtPath),
                                 f"{os.path.splitext(os.path.basename(videoPath))[0]}_{info.language}.srt")
    tmp = os.path.join(os.path.dirname(srtPath), "tmp.srt")

    texts = []
    times = []
    index = 0

    if os.path.exists(srtSourcePath):
        os.remove(srtSourcePath)

    with open(srtSourcePath, 'w', encoding='utf-8') as file:
        for segment in segments:
            print(segment.text)
            texts.append(segment.text)
            index = index + 1
            time = f"{index}\n{seconds_to_srt_time(segment.start)} --> {seconds_to_srt_time(segment.end)}"
            times.append(time)
            file.write(f"{time}\n{segment.text}\n\n")

    results = translator.handler(translator.delimiter.join(texts))
    print(translator.delimiter.join(texts))
    print(results)

    if os.path.exists(tmp):
        os.remove(tmp)

    with open(tmp, 'w', encoding='utf-8') as file:
        for time, text, result in zip(times, texts, results.split(translator.delimiter)):
            file.write(f"{time}\n{result}\n\n")

    os.rename(tmp, srtPath)


def seconds_to_srt_time(seconds):
    milliseconds = int(seconds * 1000)
    hours, milliseconds = divmod(milliseconds, 3600000)
    minutes, milliseconds = divmod(milliseconds, 60000)
    seconds, milliseconds = divmod(milliseconds, 1000)
    return "{:02d}:{:02d}:{:02d},{:03d}".format(hours, minutes, seconds, milliseconds)
