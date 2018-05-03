from yumi.modulecontext import ModuleContext
from yumi.modulebase import Module
from yumi.api import load_root_modules


class ModulesList(Module):
    @staticmethod
    def do(args: list, context: ModuleContext):
        modules = load_root_modules(context.root_dir)
        context.stdout.write("Modules:\n")
        for module in modules:
            context.stdout.write("    " + module + "\n")
        return modules


Modules = {
    "mls": ModulesList
}