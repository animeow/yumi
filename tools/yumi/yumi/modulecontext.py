import sys


class ModuleContext(object):
    root_dir: str
    working_dir: str
    temp_dir: str
    local_conf: dict
    def __init__(self):
        self.stdin = sys.stdin
        self.stdout = sys.stdout
        self.stderr = sys.stderr