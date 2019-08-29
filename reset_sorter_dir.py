import os
import sys
import shutil
import stat
import logging

#GLOBAL VARIABLES
src = os.path.join(os.getcwd(), 'easy mess backup', 'mess inside')
dst = os.path.join(os.getcwd(), 'mess inside')

#LOGGING SETTINGS:
logging.basicConfig(level=logging.INFO)

def on_rm_error(func, path, exc_info):
    '''handle read-only files while performing rmtree function'''
    os.chmod(path, stat.S_IWRITE)
    os.remove(path)
    
def reset_messy_dir():
    '''deletes working folder and recreates it from backup folder'''
    if os.path.exists(dst) == True:
        logging.info(f'path {dst} exists and is being removed')
        shutil.rmtree(dst, ignore_errors=False, onerror=on_rm_error)
    shutil.copytree(src, dst)
    logging.info(f'Directory copied from: {src}\nto: {dst}')
    logging.info('Finished')

if __name__ == '__main__':
    reset_messy_dir()