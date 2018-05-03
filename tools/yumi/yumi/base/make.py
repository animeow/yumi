import subprocess
import argparse

from yumi.modulecontext import ModuleContext
from yumi.modulebase import Module


class Make(Module):
    @staticmethod
    def do(args: list, context: ModuleContext):
        return


Modules = {
    "make": Make
}