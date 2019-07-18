import os
import re
import shutil
from abc import ABC, abstractmethod
from enum import Enum
from .common import WORK_DIR, CONFIG_DIR, LOGIC_DIR, LOG_DIR, OUTPUT_DIR

GPU_FOLDER_PATTERN = r'[0-9]+'

class BUILD_STYLE(Enum):
    BUTT = 0
    TENSILE_STYLE = 1

class DirBuildStrategyBase(ABC):
    
    def __init__(self):
        pass
    
    @abstractmethod
    def build(self):
        pass

class InvalidStyle(DirBuildStrategyBase):
    def __init__(self):
        pass
    def build(self):
        print("Invalid build style, do nothing")
        

class DirBuildTensileStyle(DirBuildStrategyBase):
    '''
    0_SplitConfigYaml
    1_BenchmarkProblems
    2_BenchmarkData
    3_LibraryLogic
    4_LibraryClient
    5_SplitTrainingLog
    '''
    def __init__(self):
        self._0_folder = "0_SplitConfigYaml"
        self._1_folder = "1_BenchmarkProblems"
        self._2_folder = "2_BenchmarkData"
        self._3_folder = "3_LibraryLogic"
        self._4_folder = "4_LibraryClient"
        self._5_folder = "5_SplitTrainingLog"
        
    
    def build(self):
        self.build_0_SplitConfigYaml()
        self.build_1_BenchmarkProblems()
        self.build_2_BenchmarkData()
        self.build_3_LibraryLogic()
        self.build_4_LibraryClient()
        self.build_5_SplitTrainingLog()

    def build_0_SplitConfigYaml(self):
        print("*******************************************")
        print("Start build 0_SplitConfigYaml...")

        if not os.path.exists(CONFIG_DIR):
            print("[DirBuildTensileStyle::build_0_SplitConfigYaml] Invalid src dir")
            return
        
        folder = os.path.join(OUTPUT_DIR, self._0_folder)
        os.mkdir(folder)
            
        for root, dirs, files in os.walk(CONFIG_DIR, topdown=False):
            for file in files:
                filename = os.path.splitext(file)[0]
                post = os.path.splitext(file)[1]
                if post == ".yaml":
                    dst_dir = os.path.join(folder, filename)
                    os.mkdir(dst_dir)
                    dst_path = os.path.join(dst_dir, file)
                    shutil.copyfile(os.path.join(root, file), dst_path)
        
        print("0_SplitConfigYaml build completed.")
        print("*******************************************")
    
    def build_1_BenchmarkProblems(self):
        print("*******************************************")
        print("Start build 1_BenchmarkProblems...")

        if not os.path.exists(LOGIC_DIR):
            print("[DirBuildTensileStyle::build_1_BenchmarkProblems] Invalid src dir")
            return
        
        folder = os.path.join(OUTPUT_DIR, self._1_folder)
        os.mkdir(folder)

        for root,dirs,files in os.walk(LOGIC_DIR):
            if root == LOGIC_DIR:
                for dir in dirs:
                    if re.match(GPU_FOLDER_PATTERN, dir):
                        dst_folder = os.path.join(folder, dir)
                        os.mkdir(dst_folder)
                        src_folder = os.path.join(root, dir, self._1_folder)
                        command = "cp -r {}/. {}".format(src_folder, dst_folder)
                        print(command)
                        os.system(command)
                        
                
        print("1_BenchmarkProblems build completed.")
        print("*******************************************")
    
    def build_2_BenchmarkData(self):
        print("*******************************************")
        print("Start build 2_BenchmarkData...")

        if not os.path.exists(LOGIC_DIR):
            print("[DirBuildTensileStyle::build_2_BenchmarkData] Invalid src dir")
            return
        
        folder = os.path.join(OUTPUT_DIR, self._2_folder)
        os.mkdir(folder)

        for root,dirs,files in os.walk(LOGIC_DIR):
            if root == LOGIC_DIR:
                for dir in dirs:
                    if re.match(GPU_FOLDER_PATTERN, dir):
                        dst_folder = os.path.join(folder, dir)
                        os.mkdir(dst_folder)
                        src_folder = os.path.join(root, dir, self._2_folder)
                        command = "cp -r {}/. {}".format(src_folder, dst_folder)
                        print(command)
                        os.system(command)

        print("2_BenchmarkData build completed.")
        print("*******************************************")
    
    def build_3_LibraryLogic(self):
        print("*******************************************")
        print("Start build 3_LibraryLogic...")

        if not os.path.exists(LOGIC_DIR):
            print("[DirBuildTensileStyle::build_3_LibraryLogic] Invalid src dir")
            return
        
        folder = os.path.join(OUTPUT_DIR, self._3_folder)
        os.mkdir(folder)

        for root,dirs,files in os.walk(LOGIC_DIR):
            if root == LOGIC_DIR:
                for dir in dirs:
                    dst_folder = os.path.join(folder, dir)
                    os.mkdir(dst_folder)
                    src_folder = os.path.join(root, dir)
                    if re.match(GPU_FOLDER_PATTERN, dir):
                        src_folder = os.path.join(root, dir, self._3_folder)
                    
                    command = "cp -r {}/. {}".format(src_folder, dst_folder)
                    print(command)
                    os.system(command)

        print("3_LibraryLogic build completed.")
        print("*******************************************")
    
    def build_4_LibraryClient(self):
        print("*******************************************")
        print("Start build 4_LibraryClient...")

        if not os.path.exists(LOGIC_DIR):
            print("[DirBuildTensileStyle::build_4_LibraryClient] Invalid src dir")
            return
        
        folder = os.path.join(OUTPUT_DIR, self._4_folder)
        os.mkdir(folder)

        for root,dirs,files in os.walk(LOGIC_DIR):
            if root == LOGIC_DIR:
                for dir in dirs:
                    if re.match(GPU_FOLDER_PATTERN, dir):
                        dst_folder = os.path.join(folder, dir)
                        os.mkdir(dst_folder)
                        src_folder = os.path.join(root, dir, self._4_folder)
                        command = "cp -r {}/. {}".format(src_folder, dst_folder)
                        print(command)
                        os.system(command)
        

        print("4_LibraryClient build completed.")
        print("*******************************************")

    def build_5_SplitTrainingLog(self):
        print("*******************************************")
        print("Start build 5_SplitTrainingLog...")

        if not os.path.exists(LOG_DIR):
            print("[DirBuildTensileStyle::build_5_SplitTrainingLog] Invalid src dir")
            return
  
        folder = os.path.join(OUTPUT_DIR, self._5_folder)
        os.mkdir(folder)
            
        for root, dirs, files in os.walk(LOG_DIR, topdown=False):
            for file in files:
                filename = os.path.splitext(file)[0]
                post = os.path.splitext(file)[1]
                if post == ".log":
                    dst_dir = os.path.join(folder, filename)
                    os.mkdir(dst_dir)
                    dst_path = os.path.join(dst_dir, file)
                    shutil.copyfile(os.path.join(root, file), dst_path)
                    
        print("5_SplitTrainingLog build completed.")
        print("*******************************************")

class Context:
    def __init__(self, build_style):
        if  BUILD_STYLE.TENSILE_STYLE == build_style:
            self._strategy = DirBuildTensileStyle()
        else:
            self._strategy = InvalidStyle()
    
    def build(self):
        self._strategy.build()

class DirStructBuilder:
    def __init__(self):

        if not os.path.exists(WORK_DIR):
            print("[DirStructGenerator::init] {} folder not exised".format(WORK_DIR))
            return
        
        if os.path.exists(OUTPUT_DIR):
            shutil.rmtree(OUTPUT_DIR)
        
        os.mkdir(OUTPUT_DIR)
        
        print("[DirStructGenerator::init] src folder is {}".format(WORK_DIR))
        print("[DirStructGenerator::init] dst folder is {}".format(OUTPUT_DIR))
        context = Context(BUILD_STYLE.TENSILE_STYLE)
        context.build()
        shutil.rmtree(WORK_DIR)

    

    

        