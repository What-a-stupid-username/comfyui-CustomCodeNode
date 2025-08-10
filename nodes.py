import pickle
import copy
import traceback

class CustomCodeNodeImg:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "I": ("INT", {"default": 0}),
                "F": ("FLOAT", {"default": 0.5}),
                "AlwaysExecute": ("BOOLEAN", {"default": False, "tooltip": "If True, the node will always execute, even if the input is not changed."}),
                "code": ("STRING", {"multiline": True,"default": "image0 = image0 * F"}),
            },
            "optional": {
                "image0": ("IMAGE",),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image0",)

    FUNCTION = "run"
    OUTPUT_NODE = True

    CATEGORY = "CustomCodeNode"

    @classmethod
    def IS_CHANGED(self, I, F, AlwaysExecute, code, image0=None):
        if AlwaysExecute:
            return float("nan")
        else:
            vars = [I, F, code, image0]
            hashs = hash(tuple([pickle.dumps(var) for var in vars]))
            return hashs
    
    def run(self, I, F, AlwaysExecute, code, image0=None):
        g = globals()
        l = locals()

        print("StartExecute Custom Code >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        g = globals()
        l = locals()
        try:
            code_compiled = compile(code, "<CustomCodeNode>", "exec")
            exec(code_compiled, g, l)
        except Exception as e:
            tb = traceback.extract_tb(e.__traceback__)
            print(f"{type(e).__name__}: {e}")
            for entry in tb:
                if entry.filename == "<CustomCodeNode>":
                    lineno = entry.lineno
                    line = code.splitlines()[lineno - 1]
                    print(f"  File \"{entry.filename}\", line {lineno}")
                    print(f"    {line}")
                    print(f"    {' ' * (entry.colno - 1 if entry.colno else 0)}^" if hasattr(entry, "colno") else "")  # Python 3.11+
                    raise Exception(f"Error Executing Custom Code")
        print("End Execute Custom Code <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        
        image0 = l['image0']
        return (image0,)

class CustomCodeNodeString:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "I": ("INT", {"default": 0}),
                "F": ("FLOAT", {"default": 0.5}),
                "AlwaysExecute": ("BOOLEAN", {"default": False, "tooltip": "If True, the node will always execute, even if the input is not changed."}),
                "code": ("STRING", {"multiline": True,"default": "string0 = string0"}),
            },
            "optional": {
                "string0": ("STRING",),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("string0",)

    FUNCTION = "run"
    OUTPUT_NODE = True

    CATEGORY = "CustomCodeNode"

    @classmethod
    def IS_CHANGED(self, I, F, AlwaysExecute, code, string0=None):
        if AlwaysExecute:
            return float("nan")
        else:
            hashs = hash(tuple(I, F, code, string0))
            return hashs
    
    def run(self, I, F, AlwaysExecute, code, string0=None):
        g = globals()
        l = locals()

        print("StartExecute Custom Code >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        g = globals()
        l = locals()
        try:
            code_compiled = compile(code, "<CustomCodeNode>", "exec")
            exec(code_compiled, g, l)
        except Exception as e:
            tb = traceback.extract_tb(e.__traceback__)
            print(f"{type(e).__name__}: {e}")
            for entry in tb:
                if entry.filename == "<CustomCodeNode>":
                    lineno = entry.lineno
                    line = code.splitlines()[lineno - 1]
                    print(f"  File \"{entry.filename}\", line {lineno}")
                    print(f"    {line}")
                    print(f"    {' ' * (entry.colno - 1 if entry.colno else 0)}^" if hasattr(entry, "colno") else "")  # Python 3.11+
                    raise Exception(f"Error Executing Custom Code")
        print("End Execute Custom Code <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

        string0 = l['string0']
        return (string0,)



class AnyType(str):
    """A special class that is always equal in not equal comparisons. Credit to pythongosssss"""

    def __ne__(self, __value: object) -> bool:
        return False

any_type = AnyType("*")

import re
def get_trailing_int(s):
    match = re.search(r'(\d+)$', s)
    if match:
        return int(match.group(1))
    return None

class CustomCodeNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "I": ("INT", {"default": 0}),
                "F": ("FLOAT", {"default": 0.5}),
                "AlwaysExecute": ("BOOLEAN", {"default": False, "tooltip": "If True, the node will always execute, even if the input is not changed."}),
                "code": ("STRING", {"multiline": True,"default": "print('Hello, World!')\nprint(var0)"}),
            },
        }
    
    RETURN_TYPES = tuple([any_type for i in range(64)])
    RETURN_NAMES = tuple([f"any{i}" for i in range(64)])

    FUNCTION = "run"
    OUTPUT_NODE = True

    CATEGORY = "CustomCodeNode"

    @classmethod
    def IS_CHANGED(self, I, F, AlwaysExecute, code, **kw):
        if AlwaysExecute:
            return float("nan")
        else:
            vars = [I, F, code]
            for key in kw.keys():
                vars.append(kw[key])
            hashs = hash(tuple([pickle.dumps(var) for var in vars]))
            return hashs

    def run(self, I, F, AlwaysExecute, code, **kw):

        # fill the missing variables
        var_list = []
        for key in kw.keys():
            var_list.append(get_trailing_int(key))
        num = max(var_list)+2 if len(var_list) > 0 else 1
        for i in range(num):
            if i in var_list:
                continue
            else:
                kw[f"var{i}"] = None
                var_list.append(i)

        # register the variables
        for key in kw.keys():
            exec(f"{key} = copy.deepcopy(kw['{key}'])")
        
        # execute the code
        print("StartExecute Custom Code >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        g = globals()
        l = locals()
        try:
            code_compiled = compile(code, "<CustomCodeNode>", "exec")
            exec(code_compiled, g, l)
        except Exception as e:
            tb = traceback.extract_tb(e.__traceback__)
            print(f"{type(e).__name__}: {e}")
            for entry in tb:
                if entry.filename == "<CustomCodeNode>":
                    lineno = entry.lineno
                    line = code.splitlines()[lineno - 1]
                    print(f"  File \"{entry.filename}\", line {lineno}")
                    print(f"    {line}")
                    print(f"    {' ' * (entry.colno - 1 if entry.colno else 0)}^" if hasattr(entry, "colno") else "")  # Python 3.11+
                    raise Exception(f"Error Executing Custom Code")
        print("End Execute Custom Code <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

        # update the variables
        for i in kw.keys():
            idx = get_trailing_int(i)
            exec(f"var_list[{idx}] = l['{i}']")

        return tuple(var_list)