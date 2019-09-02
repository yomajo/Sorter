import os, shutil, stat
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
                target_path = os.path.join(target_dir, filename)
                # Duplicate filename prevention        
                abs_src_path = handle_duplicates(abs_src_path, target_path)
                #duplicate file might be handled (removed), therefore try.
                try:
                    file_mover(abs_src_path, target_dir)
                except:
                    logging.info(f'\nFailed to remove file: {abs_src_path} File was removed by handler (check logs) or permission issue')
                continue
        if curr_path == abs_working_dir:
            logging.info(f'BREAKING LOOP of traversing through: {abs_working_dir}')
            break
        else:        
            remove_empty_dirs(curr_path)

def remove_empty_dirs(path):
    '''function attempts to delete arg. path'''
    try:
        os.removedirs(path)
        logging.info(f'Path has been DELETED: {path}')
    except:
        logging.info(f'Unable to delete dir: {path}')

def file_mover(abs_src_path, abs_target_path):
    '''Tries to move file abs_src_path (abs path to file) to target path (second arg)'''
    f_basename = os.path.basename(abs_src_path)
    if os.path.exists(abs_target_path):
        try:
            shutil.move(abs_src_path, abs_target_path)
            logging.info(f'file {f_basename} moved to: {abs_target_path}')
        except:
            logging.info(f'\nFor some reason file {f_basename} was not moved')
            try:
                logging.info(f'Changing file {f_basename} permissions')
                os.chmod(abs_src_path, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO)
                shutil.move(abs_src_path, abs_target_path)
            except:
                logging.info(f'\nGave up on clean shutil.move({abs_src_path}, {abs_target_path})')

def handle_duplicates(src_file, trg_file):
    '''removes src_file is it's identical to trg_file. Returns abs path to renamed src_file
    if files only have the same filename.
    src_file, trg_file: abs. paths to files of interest'''
    # Two conditions to check if args require handling in the first place
    # 1.check if proviced arguments exist
    if os.path.exists(src_file) and os.path.exists(trg_file):
        # 2.check if proviced arguments have the same filename
        if os.path.basename(src_file) != os.path.basename(trg_file):
            return src_file
        else:
            if filecmp.cmp(src_file, trg_file, shallow=False) == True:
                rm_f_abs_path = os.path.abspath(src_file)
                try:
                    os.remove(rm_f_abs_path)
                    logging.info(f'Removing file: {rm_f_abs_path}')
                except:
                    logging.info(f'Unable to delete duplicate file: {os.path.basename(src_file)} in\n{rm_f_abs_path}')
                    logging.info(f'Setting max permissions on file {os.path.basename(src_file)}')
                    os.chmod(rm_f_abs_path, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO)
                    try: 
                        os.remove(rm_f_abs_path)
                        logging.info(f'Ultimately file {os.path.basename(src_file)} was deleted successfully')
                    except:
                        logging.info(f'Gave up on removing file {os.path.basename(src_file)}')
            # Only filename is the same
            else:
                return make_filename_unique(src_file)
    else:
        return src_file

def make_filename_unique(path_to_file):
    '''Renames and returns abs path to renamed file basename added (1) at the end
    path_to_file is an absolute path to filename'''
    base, ext = os.path.splitext(path_to_file)
    new_path = base + '(1)' + ext
    os.rename(path_to_file, new_path)
    logging.info(f'Renaming file: {os.path.basename(path_to_file)} found in {os.path.dirname(path_to_file)} to: {os.path.basename(new_path)}')
    return new_path

def mk_ext_based_dir(filename):
    '''Extracts extention from arg (filename). Checks if directory exists, if not - creates one. Returns abs. path to new folder'''
    ext = filename.upper().split('.')[-1]
    ext_dir = os.path.join(abs_working_dir, ext)
    if os.path.exists(ext_dir) == False:
        os.mkdir(ext_dir)
        logging.info(f'Folder {ext} created in {ext_dir}')
    return ext_dir


if __name__=='__main__':
    sort_this(abs_working_dir)
    logging.info('----------- SORTER FINISHED RUNNING -----------')