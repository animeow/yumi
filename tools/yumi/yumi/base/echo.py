from yumi.modulecontext import ModuleContext
from yumi.modulebase import Module


class Echo(Module):
    @staticmethod
    def do(args: list, context: ModuleContext):
        msg = " ".join(args)
        context.stdout.write(msg + "\n")
        return msg


Modules = {
    "echo": Echo
}