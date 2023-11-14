"""
A function which provides a simple terminal interface for making mass changes to a directory/folder of text files.
"""

from os import listdir, path
import string_tools, print_tools

def change_all_text_files(dir_path:str, modifier_func, confirm:bool=True):
    """A simple terminal interface for making mass changes to a directory/folder of text files.
    - provide a directory/folder path to `dir_path`
    - provide a function which will be used to modify the text to `modifier_func` 
    - if `confirm` is True, will display the modifed text and ask for confirmation before actually updating the file
    """
    # 1) Setup constants:
    DIR = path.realpath(dir_path)
    assert path.isdir(DIR), f'"{dir_path}" is a not a path to a folder/directory'
    assert callable(modifier_func), "`modifer_func` argument must be a callable function/method"
    DIR_CONTENTS = listdir(DIR)
    # 2) Go through each file in directory, and apply modifer function to it:
    for content in DIR_CONTENTS:
        content_path = path.join(DIR, content)                  # get file/sub-directory/folder path
        if path.isfile(content_path):                           # determine if file, or folder
            cont_type = "file"
        elif path.isdir(content_path):
            cont_type = "directory/folder"
        else:
            cont_type = "neither file nor directory/folder"     # not sure if this is even possible, but the code is here anyway!
        print('\n' + '-'*50 + '\n')                             # print the data nicely
        print_tools.print_dict_nicely({
            'Name:':                    content,
            'Type:':                    cont_type,
        })
        if cont_type == "directory/folder":                     # if the data is a directory, continue
            continue
        # modify each file:
        with open(content_path, "r+", encoding='utf-8') as file:
            data = file.read()                                  # read the file data
            modified_data = modifier_func(data)                 # modify the file data using the provided function
            if data == modified_data:                           # if the data is unchanged, continue to the next file
                continue
            print_tools.print_dict_nicely({                     # print the data nicely again
                'Orginal File Contents:':   string_tools.box_text(data),
                'New File Contents:':       string_tools.box_text(string_tools.highlight_line_changes_simple(data, modified_data))
            })

            if confirm:                                         # if `confirm` is True, ask user if okay to make the change
                i = input("\nmake change? (enter y/Y to change): ")
                if not i.lower() == 'y':
                    continue
            file.seek(0)
            file.write(modified_data)                           # write the updated data to the file

##########################

# UPDATE THIS FUNCTION TO ALSO WORK RECURSIVELY
"""    - if `recusrive` is True, will also try to modfiy all text files nested within sub-directory/folders"""
# can use os.walk, or just keep using list_dir and self-referential function which calls itself when encountering a dir/folder
