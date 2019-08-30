import os, shutil
import logging
import reset_sorter_dir
import filecmp

# GLOBAL VARIABLES
abs_working_dir = os.path.join(os.path.dirname(__file__), 'mess inside').replace("\\", "/")
logging.info(f'Working directory is: {abs_working_dir}')

# LOGGING SETTINGS:
logging.basicConfig(level=logging.INFO)

# FUNCTIONS:
def sort_this(path):
    '''takes an arg of path to be re-organized by file extensions.
    Iterates through files, folders and subfolders, creating and deleting folders, moving files'''
    for curr_path, _, filenames in os.walk(path, topdown=False):
        logging.info(f'CURRENTLY IN PATH: {curr_path}')
        # if folder contains files, iterate through files and sort given path
        if len(filenames)>0:
            for filename in filenames:
                target_dir = mk_ext_based_dir(filename)
                abs_src_path = os.path.join(curr_path, filename)
                file_mover(abs_src_path, target_dir)
        if curr_path == abs_working_dir:
            logging.info(f'BREAKING LOOP of traversing through: {abs_working_dir}')
            break
        else:        
            remove_empty_dirs(curr_path)

def remove_empty_dirs(path):
    '''function attempts to delete arg. path'''
    try:
        os.removedirs(path)
        logging.info(f'Path has been DELETED:\n{path}')
    except:
        logging.info(f'Uanable to delete dir: {path}')

def file_mover(abs_src_path, abs_target_path):
    '''Tries to move file abs_src_path (abs path to file) to target path (second arg)'''
    f_basename = os.path.basename(abs_src_path)
    if os.path.exists(abs_target_path):
        try:
            shutil.move(abs_src_path, abs_target_path)
            logging.info(f'\nfile {f_basename} moved to: {abs_target_path}')
        except:
            logging.info(f'For some reason file\n{f_basename}\nwas not moved')

def handle_duplicates(src_file, trg_file):
    '''removes src_file is it's identical to trg_file. Returns abs path to renamed src_file
    if files only have the same filename.
    src_file, trg_file: abs. paths to files of interest'''
    # check if proviced arguments have the same filename and require handling in the first place
    if os.path.basename(src_file) != os.path.basename(trg_file):
        return
    else:
        if filecmp.cmp(src_file, trg_file, shallow=False) == True:
            rm_f_abs_path = os.path.abspath(src_file)
            try:
                os.remove(rm_f_abs_path)
                logging.info(f'Removing file: {rm_f_abs_path}')
            except:
                logging.info(f'Unable to delete duplicate file: {os.path.basename(src_file)} in\n{rm_f_abs_path}')
        # Only filename is the same
        else:
            return make_filename_unique(src_file)

def make_filename_unique(path_to_file):
    '''Renames and returns abs path to renamed file basename added (1) at the end
    path_to_file is an absolute path to filename'''
    base, ext = os.path.splitext(path_to_file)
    new_path = base + '(1)' + ext
    os.rename(path_to_file, new_path)
    logging.info(f'Renaming file {os.path.basename(path_to_file)} found in\n{os.path.dirname(path_to_file)} to: {os.path.basename(new_path)}')
    return new_path

def mk_ext_based_dir(filename):
    '''Extracts extention from arg (filename). Checks if directory exists, if not - creates one. Returns abs. path to new folder'''
    ext = filename.upper().split('.')[-1]
    ext_dir = os.path.join(abs_working_dir, ext)
    if os.path.exists(ext_dir) == False:
        os.mkdir(ext_dir)
        logging.info(f'Folder {ext} created in {ext_dir}')
    else:
        logging.info(f'Directory {ext_dir} already exists')
    return ext_dir


if __name__=='__main__':
    # reset_sorter_dir.reset_messy_dir()
    # sort_this(abs_working_dir)
    handle_duplicates('mess inside/mess2/There are two of me.txt',
    'C:/Coding/Sorter/mess inside/messy stuff1/There are two of me.txt')
    logging.info('----------- SORTER FINISHED RUNNING -----------')