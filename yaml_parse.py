import re
import os

WORK_DIR = os.getcwd() + "/tmp"
CONFIG_DIR = WORK_DIR + "/config"
LOGIC_DIR  = WORK_DIR + "/logic"

class YamlParse:
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
        
        
        
        
        
