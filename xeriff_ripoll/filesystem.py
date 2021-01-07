

class Filesystem:

    def read(self, path: str, mode: str) -> str:
        with open(path, mode) as f:
            return f.read()

    def write(self, path: str, mode: str, contents: str):
        with open(path, mode) as f:
            f.write(contents)