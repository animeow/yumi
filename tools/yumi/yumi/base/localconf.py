import argparse
import json

from yumi.modulecontext import ModuleContext
from yumi.modulebase import Module


class LocalConf(Module):
    @staticmethod
    def do(args: list, context: ModuleContext):
        parser = argparse.ArgumentParser("Local conf manager")
        subparsers = parser.add_subparsers(help="Action", dest="action")

        set_parser = subparsers.add_parser("set", help="Set value")
        set_parser.add_argument(dest="key", action="store", help="Key")
        set_parser.add_argument(dest="value", action="store", help="Value")
        set_parser.add_argument("-t", "--type",
                                dest="type",
                                action="store",
                                choices=["json", "str", "int", "float", "bool"],
                                default="str",
                                required=False,
                                help="Value type")

        get_parser = subparsers.add_parser("get", help="Set value")
        get_parser.add_argument(dest="key", action="store", help="Key")

        get_parser = subparsers.add_parser("rm", help="Remove value")
        get_parser.add_argument(dest="key", action="store", help="Key")

        keys_parser = subparsers.add_parser("keys", help="List keys")

        parsed_args = parser.parse_args(args)
        if parsed_args.action == "set":
            if context.local_conf is None:
                context.local_conf = dict()
            value = parsed_args.value
            if parsed_args.type == "json": value = json.load(value)
            elif parsed_args.type == "int": value = int(value)
            elif parsed_args.type == "bool": value = bool(value)
            elif parsed_args.type == "float": value = float(value)

            context.local_conf[parsed_args.key] = value
            return value
        elif parsed_args.action == "get":
            if context.local_conf is None or parsed_args.key not in context.local_conf:
                context.stderr.write(parsed_args.key + " not found\n")
                return None
            value = context.local_conf[parsed_args.key]
            context.stdout.write(str(value) + "\n")
            return value
        elif parsed_args.action == "rm":
            if context.local_conf is None or parsed_args.key not in context.local_conf:
                context.stderr.write(parsed_args.key + " not found\n")
                return None
            value = context.local_conf.pop(parsed_args.key)
            return value
        elif parsed_args.action == "keys":
            if context.local_conf is None:
                return []
            keys = [key for key in context.local_conf]
            context.stdout.write("\n".join(keys) + "\n")
            return keys
        else: parser.print_help()


Modules = {
    "conf": LocalConf
}