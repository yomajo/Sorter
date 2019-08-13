import os
import logging
import reset_sorter_dir


# GLOBAL VARIABLES
abs_working_dir = os.path.join(os.path.dirname(__file__), 'mess inside').replace("\\", "/")
logging.info(f'Working directory is: {abs_working_dir}')

# LOGGING SETTINGS:
logging.basicConfig(level=logging.INFO)

# FUNCTIONS:
extensions = []
def collect_extensions(path):
    '''iterates through files, folders and subfolders and returns a list of extensions'''
    for curr_path, folders, filenames in os.walk(path):
        logging.info(f'-------\nSTARTING NEW ITARATION CYCLE\n-------')
        logging.info(f'CURRENTLY IN PATH: {curr_path}')
        # if folder contains files, iterate through files and extract extensions to a list
        if len(filenames)>0:
            for filename in filenames:
                ext = filename.upper().split('.')[-1]
                if ext not in extensions: extensions.append(ext)
                extensions.sort()
    logging.info(f'Ive collected these unique extensions: \n{extensions};\n{path} contains {len(extensions)} different extensions in total')
    return extensions
            
def create_extension_folders(extensions_list):
    '''creates empty folders named after the list passed'''
    i = 0
    for ext in extensions_list:
        os.mkdir(abs_working_dir + '/' + ext)
        i += 1


def sort_this():
    '''list of functions to be executed when file is run'''
    extension_list = collect_extensions(abs_working_dir)
    create_extension_folders(extension_list)
                
                
if __name__=='__main__':
    # reset_sorter_dir.reset_messy_dir()
    sort_this()
    logging.info('-----------\nFINISHED')