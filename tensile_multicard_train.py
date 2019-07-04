import os
import sys
import argparse
import shutil
import multiprocessing
from multiprocessing import Pool

from .hardware_detector import HardwareDetector
from .yaml_parse import YamlParse, WORK_DIR, CONFIG_DIR, LOGIC_DIR


deviceList = []
LOG_DIR = WORK_DIR + "/LOG"
logic_dir_list = []

def run(command):
    print("[Process %s], command: %s" % (os.getpid(), command))
    os.system(command)

def multiRun(tensile_root, conf_file_list, deviceList):
    train_command = "python " + tensile_root + "/Tensile/bin/Tensile"

    pool = Pool(len(conf_file_list))
    print("fork %s subprocess to train..." % len(conf_file_list))
    for idx in range(len(conf_file_list)):
        device_idx = deviceList[idx]
        config_file = conf_file_list[idx]
        
        log_dir = LOG_DIR + "/" + str(device_idx) + ".log"
        logic_dir = LOGIC_DIR + "/" + str(device_idx) + "/"
        
        logic_dir_list.append(logic_dir + "3_LibraryLogic")
        command_line = "HIP_VISIBLE_DEVICES=" + str(device_idx) + " " + train_command + " " + config_file + " " + logic_dir + " > " + log_dir
        pool.apply_async(run, [command_line])
    
    pool.close()
    pool.join()

    print("multi process done.")
    

def mergeLogicFile(tensile_path):
    print("merge start...")
    merge_script = "python " + tensile_path + "/Tensile/Utilities/merge_rocblas_yaml_files.py"
    
    print("all the logic files as below:")
    print(logic_dir_list)

    if 0 == len(logic_dir_list):
        print("No file need to merge!")
        return

    final_dir = LOGIC_DIR + "/final"
    
    os.mkdir(final_dir)
    
    if 1 == len(logic_dir_list):
        os.system("cp %s/* %s" % (logic_dir_list[0], final_dir))
        return

    tmp_dir = LOGIC_DIR + "/tmp"
    os.mkdir(tmp_dir)
    os.system("cp %s/* %s" % (logic_dir_list[0], tmp_dir))
    
    orig_dir = tmp_dir
    for i in range(1, len(logic_dir_list)):
        new_dir = LOGIC_DIR + "/tmp%s" % i
        os.mkdir(new_dir)

        command = "%s %s %s %s" % (merge_script, orig_dir, logic_dir_list[i], new_dir)
        print(command)
        os.system(command)
        orig_dir = new_dir
    
    os.system("cp %s/* %s" % (orig_dir, final_dir))

    print("merge done.")
    
        
    
def Train(usrArgs):
    argParser = argparse.ArgumentParser()
    argParser.add_argument("config_path", help="config.yaml file path")
    argParser.add_argument("tensile_path", help="root path of tensile")
    argParser.add_argument("-g", "--gpu", type = int, dest='gpu', \
        help = "gpu idx which used, will use all the valid gpu default", \
        required = False, nargs = '*')

    args = argParser.parse_args()
    
    hardware = HardwareDetector()
    
    if args.gpu:
        deviceList = list(set(hardware.gpu).intersection(set(args.gpu)))
    else:
        deviceList = hardware.gpu

    if 0 == len(deviceList):
        print("No GPU available or you choose the invalid gpu!")
        return

    print("%s gpu will be used. devices list : %s" % (len(deviceList), deviceList))
    
    if os.path.exists(WORK_DIR):
        shutil.rmtree(WORK_DIR)
    os.mkdir(WORK_DIR)
    os.mkdir(CONFIG_DIR)
    os.mkdir(LOG_DIR)
    os.mkdir(LOGIC_DIR)
    
    try:
        parse =  YamlParse(args.config_path, deviceList)
    except (ValueError, IOError):
        return
    else:
        multiRun(args.tensile_path, parse.split_config_path_list, deviceList)
        mergeLogicFile(args.tensile_path)
        
    

def main():
    Train(sys.argv[1:])


if __name__ == "__main__":
    print("This is can no longer be run as script. Run 'tensile_multicard_train/bin/train' instead.")
    exit(1)