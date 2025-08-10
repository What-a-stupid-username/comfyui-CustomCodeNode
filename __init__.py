from .nodes import *

WEB_DIRECTORY = "./web"

NODE_CLASS_MAPPINGS = {
    "CustomCodeNodeImg": CustomCodeNodeImg,
    "CustomCodeNodeString": CustomCodeNodeString,
    "CustomCodeNode" : CustomCodeNode,
    
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CustomCodeNodeImg": "Custom Code (Image)",
    "CustomCodeNodeString": "Custom Code (String)",
    "CustomCodeNode": "Custom Code Node",
}