from yumi.modulecontext import ModuleContext
from yumi.modulebase import Module
from yumi.api import init_global


class Initializer(Module):
    @staticmethod
    def do(args: list, context: ModuleContext):
        return init_global(context.working_dir)


Modules = {
    "init": Initializer
}