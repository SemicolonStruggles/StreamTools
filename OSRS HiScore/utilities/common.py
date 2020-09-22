from pathlib import Path


def getFileContents(path):
    file = open(path, "r", encoding='utf-8')
    contents = file.read()
    file.close()
    return contents


def getBaseDir():
    return Path(__file__).parents[1]


def buildPath(path):
    return str(Path(getBaseDir(), path))


def toAbsolutePath(path):
    path = Path(path)
    if not path.is_absolute():
        path = Path(getBaseDir(), path)
    return str(path)
