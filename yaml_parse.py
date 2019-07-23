import re
import os
import copy
from enum import Enum
from abc import ABC, abstractmethod
from .common import WORK_DIR, CONFIG_DIR, LOGIC_DIR, printWarning, printExit

try:
  import yaml
except ImportError:
  printExit("You must install PyYAML to use Tensile (to parse config files). See http://pyyaml.org/wiki/PyYAML for installation instructions.")


class YAML_BUILD_STYLE(Enum):
    BUTT          = 0
    SINGLE_CONFIG = 1
    MULTI_CONFIG  = 2

class YamlParseBase(ABC):
    def __init__(self, config_file, deviceList):
        pass

    @abstractmethod
    def getSplitConfigList(self):
        pass


class YamlParseSingleConfig(YamlParseBase):
    def __init__(self, config_file, deviceList):
        self.pre_start = -1
        self.pre_end = -1
        self.post_start = -1
        self.post_end = -1
        self.data_start_list = []
        self.data_end_list = []
        self.split_config_path_list = []
        self.config_content = []

        try:
            self.scan(config_file, deviceList)
        except IOError:
            raise IOError


    def getSplitConfigList(self):
        return self.split_config_path_list

    
    def scan(self, config_file, deviceList):
        try:
            with open(config_file, 'r') as f:
                content = f.read()
                f.close()
        except IOError:
            print("%s open failed!" % config_file)
            raise IOError
        else:
            print("%s open successed!" % config_file)
            self.config_content = content.splitlines()

        
        data_start = -1
        data_end  = -1
        
        line = 0
        for str in self.config_content:
            if -1 != str.find("- Exact:") or -1 != str.find("- Range:"):
                if -1 == data_start:
                    data_start = line
                data_end = line

            if -1 != str.find("GlobalParameters:"):
                self.pre_start = line
            if -1 != str.find("- ProblemSizes:"):
                self.pre_end = line
            if -1 != str.find("LibraryLogic:"):
                self.post_start = line
            
            line += 1
        self.post_end = line - 1
        
        total_data_num = data_end - data_start + 1
        if 0 == total_data_num:
            return
        
        device_num = len(deviceList)
        split_num =  device_num if device_num <= total_data_num else total_data_num
        
        single_part_lines = int(total_data_num / split_num)

        cur_start = data_start
        cur_line = data_start + single_part_lines - 1
        
        while split_num > 1:
            self.data_start_list.append(cur_start)
            self.data_end_list.append(cur_line)
            
            cur_start = cur_line + 1
            cur_line = cur_start + single_part_lines - 1
            
            split_num -= 1

        self.data_start_list.append(cur_start)
        self.data_end_list.append(data_end)
        
        if False == self.configCheck() or len(self.data_start_list) > len(deviceList):
            print("Invalid config file!")
            raise ValueError

        for idx in range(len(self.data_start_list)):
            config_file_name = "%s.yaml" % idx
            cur_file = CONFIG_DIR + "/" + config_file_name
            self.split_config_path_list.append(cur_file)
            
            try:
                f = open(cur_file, 'w')
            except IOError:
                print("%s open failed!".format(cur_file))
                raise IOError
            else:

                # write pre_fix
                for i in range(self.pre_start, self.pre_end + 1):
                    f.write(self.config_content[i])
                    f.write("\n")
                # write data
                for i in range(self.data_start_list[idx], self.data_end_list[idx] + 1):
                    f.write(self.config_content[i])
                    f.write("\n")
                
                # write post_fix
                for i in range(self.post_start, self.post_end + 1):
                    f.write(self.config_content[i])
                    f.write("\n")

                f.close()

    def configCheck(self):
        if -1 == self.pre_start or \
           -1 == self.pre_end   or \
           -1 == self.post_end  or \
           -1 == self.post_start:
            return False
        else:
            return True



class YamlParseMultiConfig(YamlParseBase):
    def __init__(self, config_file, deviceList):
        self._config = self.readConfig(config_file)
        self._device_list = deviceList
        self._split_config_path_list = []
        
        
        self.generateSplitConfigFile()

        
    def getSplitConfigList(self):
        return self._split_config_path_list

    def readConfig(self, config_file):
        try:
            stream = open(config_file, "r")
        except IOError:
            printExit("[YamlParseMultiConfig::readConfig] Cannot open file: {}".format(self._config_file))
            
        config = yaml.load(stream, yaml.SafeLoader)
        stream.close()
        return config


    def generateSplitConfigFile(self):
        print("generate split config file.")
        for idx in range(len(self._device_list)):
            config_file_name = "{}.yaml".format(str(self._device_list[idx]))
            cur_file = CONFIG_DIR + "/" + config_file_name

            if self.yamlWrite(idx, cur_file):
                self._split_config_path_list.append(cur_file)


    def yamlWrite(self, idx, save_file):
        valid = False
        cur_config = copy.deepcopy(self._config)
        
        if "BenchmarkProblems" in cur_config:
            for sections in  cur_config["BenchmarkProblems"]:
                for section in sections:
                    if "BenchmarkFinalParameters" in section:
                        isSaved = False
                        for problemsize in section["BenchmarkFinalParameters"]:
                            if "ProblemSizes" in problemsize:
                                start, end = self.calcRange(idx, len(problemsize["ProblemSizes"]))
                                if start != -1 and end != -1:
                                    valid = True
                                    cur_problemsize = problemsize["ProblemSizes"][start : end]
                                    problemsize["ProblemSizes"] = cur_problemsize
                                    isSaved = True
                        if False == isSaved:
                            section.clear()
                    
                    
        if True == valid:
            try:
                f = open(save_file, 'w')
            except IOError:
                printExit("[YamlParseMultiConfig :: yamlWrite]{} open failed!".format(save_file))
            else:
                f.write(yaml.dump(cur_config))
                f.close()

                print("Produce config file for {} gpu".format(idx))
        else:
            print("No need to produce config file for {} gpu.".format(idx))

        return valid
    
    def calcRange(self, idx, total):

        print("[calcRange] cur_idx = {}, cur_total = {}".format(idx, total))
        split_num = len(self._device_list)
        start = -1
        end = -1
        if total == 0 or split_num == 0:
            return start, end
        
        if total < split_num:
            if idx == 0:
                start = 0
                end = total
        else:
            part_num = total / split_num
            start = part_num * idx
            end = start + part_num
            if idx == split_num - 1:
                end = total

        start = int(start)
        end = int(end)
        
        print("[calcRange] start = {}, end = {}".format(start, end))
        return start, end
                    
    


class YamlParseContext:
    def __init__(self, style, config_file, device_list):
        if YAML_BUILD_STYLE.SINGLE_CONFIG == style:
            self._strategy = YamlParseSingleConfig(config_file, device_list)
        elif YAML_BUILD_STYLE.MULTI_CONFIG == style:
            self._strategy = YamlParseMultiConfig(config_file, device_list)

    def run(self):
        return self._strategy.getSplitConfigList()
        
        
class YamlParse:
    def __init__(self, config_file, device_list):
        self._context = YamlParseContext(YAML_BUILD_STYLE.MULTI_CONFIG, config_file, device_list)

    def run(self):
        return self._context.run()
        
