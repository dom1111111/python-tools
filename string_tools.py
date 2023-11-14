"""
Miscellaneous functions for manipulating strings and/or making them easier to look at for printing
"""

from colorama import Back, Fore

def box_text(text:str):
    """Add a box around text! Can be single or multiline string.
    
    NOTE: This will may look very weird if text-wrapping is enabled on your terminal.
    Please disable this to get normal looking results.
    """
    H_LINE = "─"
    V_LINE = "│"
    TL_CORNER = "┌"
    TR_CORNER = "┐"
    BL_CORNER = "└"
    BR_CORNER = "┘"

    lines = text.splitlines()                                           # split text into single lines of text (doesn'taffect anything if not multi-line text)
    max_length = max(len(line) for line in lines)                       # get the length of the longest line
    boxed_text = TL_CORNER + (H_LINE * max_length) + TR_CORNER + '\n'   # add the top of the box
    boxed_text += ''.join((V_LINE + line + (' ' * (max_length - len(line))) + V_LINE + '\n') for line in lines) # add sides of the box to each line
    boxed_text += BL_CORNER + (H_LINE * max_length) + BR_CORNER + '\n'  # add the bottom of the box
    return boxed_text

def get_clean_keyvalue_spacing(key:str, val:str, margin:int=30) ->int:
    """Get a string of a key and value with consistent spacing, for cleaner, easy to read printing.
    
    ex: something like this:
    - height:_21
    - width:_34
    
    becomes:
    - height:___21
    - width:____34

    (excpet the `_` are just whitespace)
    """
    assert isinstance(key, str) and isinstance(val, str), "`key` and 'val` must be strings" # ensure args are right type of value
    assert not '\n' in key, "`key` must be a single line string"                            # ensure `key` is a single line string
    space = " " * margin                                                                    # get whitespace string based on `margin`
    after_key_space = " " * (margin - len(key))                                             # get whitespace string that should be after key
    if '\n' in val:
        complete_str = ''
        for i, line in enumerate(l for l in val.split('\n') if l):                          # if it's a multi-line string, split it by the line-break ('\n'), excluding any lines which are blank
            if i == 0:
                complete_str += key + after_key_space + line + '\n'
            else:
                complete_str += space + line + '\n'
        return complete_str.removesuffix('\n')                                              # return complete string with last added line-break removed
    return key + after_key_space + val

def highlight_line_changes_simple(original:str, modified:str) -> tuple:
    """supply an original mutli-line string, and a modified version of that string, and get back the modifed text with the parts that are different highlighted"""
    highlighted_modified = [] 
    for org, mod in zip(original.split('\n'), modified.split('\n')):
        if org != mod:
            mod = Back.YELLOW + Fore.BLACK + mod + Back.RESET + Fore.RESET
        highlighted_modified.append(mod)
    return "\n".join(highlighted_modified)

# INCOMPLETE
def highlight_line_changes(original:str, modified:str) -> tuple:
    """supply an original mutli-line string, and a modified version of that string, and get back the modifed text with the parts that are different highlighted"""
    highlighted_modified = []
    original_lines = original.split('\n')
    modified_lines = modified.split('\n')
    # need to match all equivalent lines *in order*, and then highlight the modified lines which don't have an equivalents

    for mod_line in modified_lines:
        pass

    # for org_i, org_line in enumerate(original_lines):
    #     mod_i = modified_lines.index(org_line)
    #     if org_i == mod_i:
    #         highlighted_modified.append(org_line)
    #     if org != mod:
    #         mod = Back.YELLOW + Fore.BLACK + mod + Back.RESET + Fore.RESET
    #     highlighted_modified.append(mod)
    # return "\n".join(highlighted_modified)