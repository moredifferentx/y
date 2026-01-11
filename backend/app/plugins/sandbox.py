import builtins


SAFE_BUILTINS = {
    "str": str,
    "int": int,
    "float": float,
    "dict": dict,
    "list": list,
    "set": set,
    "len": len,
    "print": print,
}


def sandbox_globals():
    return {
        "__builtins__": SAFE_BUILTINS,
    }
