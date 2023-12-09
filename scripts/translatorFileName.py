import os

from scripts import translator


def handler(path):
    names = []
    paths = []
    phfixs = []

    for root, dirs, files in os.walk(path):
        for fileName in files:
            if fileName.lower().endswith(".mp4"):
                name = os.path.splitext(os.path.basename(fileName))[0]
                phfixs.append(os.path.splitext(os.path.basename(fileName))[1])
                paths.append(root)
                names.append(name)

    results = translator.handler(translator.delimiter.join(names).replace("_", " ").replace("-", " "))

    for name, result, path, phfix in zip(names, results.split(translator.delimiter), paths, phfixs):
        folder = os.path.basename(path)
        parentFolder = os.path.basename(os.path.dirname(path))
        old = f"{name}{phfix}"
        new = f"{parentFolder}_{folder}_{result}{phfix}"
        print(old)
        print(new)
        if not os.path.exists(os.path.join(path, new)):
            os.renames(os.path.join(path, old), os.path.join(path, new))
            os.renames(os.path.join(path, f"{name}.srt"), os.path.join(path, f"{parentFolder}_{folder}_{result}.srt"))
            os.renames(os.path.join(path, f"{name}_en.srt"),
                       os.path.join(path, f"{parentFolder}_{folder}_{result}_en.srt"))
