import os
import re

drmprefix = '/sys/class/drm'
valuePaths = {
    'vendor' : {'prefix' : drmprefix, 'filepath' : 'vendor', 'needsparse' : False}
}


class HardwareDetector:
    def __init__(self):
        self.gpu_num = 0
        self.gpu = []
        
        self.gpu_num = self.listDevices()
        if self.gpu_num == 0:
            return

        self.gpu = list(range(0,self.gpu_num))
    
    def listDevices(self):
        """ Return a list of GPU devices.

        Parameters:
        showall -- [True|False] Show all devices, not just AMD devices
        """

        devicelist = [device for device in os.listdir(drmprefix) if re.match(r'^card\d+$', device) and (self.isAmdDevice(device))]
        #devicelist.sort()
        return len(devicelist)

    

    def isAmdDevice(self, device):
        """ Return whether the specified device is an AMD device or not

        Parameters:
        device -- DRM device identifier
        """
        vid = self.getSysfsValue(device, 'vendor')
        if vid == '0x1002':
            return True
        return False

    
    def getSysfsValue(self, device, key):
        """ Return the desired SysFS value for a specified device

        Parameters:
        device -- DRM device identifier
        key -- [$valuePaths.keys()] Key referencing desired SysFS file
        """
        filePath = self.getFilePath(device, key)
        pathDict = valuePaths[key]

        if not filePath:
            return None
        # Use try since some sysfs files like power1_average will throw -EINVAL
        # instead of giving something useful.
        try:
            with open(filePath, 'r') as fileContents:
                fileValue = fileContents.read().rstrip('\n')
        except:
            return None

        # Some sysfs files aren't a single line of text
        if pathDict['needsparse']:
            fileValue = self.parseSysfsValue(key, fileValue)


        return fileValue

    def parseSysfsValue(self, key, value):
        """ Parse the sysfs value string

        Parameters:
        key -- [$valuePaths.keys()] Key referencing desired SysFS file
        value -- SysFS value to parse

        Some SysFS files aren't a single line/string, so we need to parse it
        to get the desired value
        """
        if key == 'id':
            # Strip the 0x prefix
            return value[2:]
        if re.match(r'temp[0-9]+', key):
            # Convert from millidegrees
            return int(value) / 1000
        if key == 'power':
            # power1_average returns the value in microwatts. However, if power is not
            # available, it will return "Invalid Argument"
            if value.isdigit():
                return float(value) / 1000 / 1000
        # ras_reatures has "feature mask: 0x%x" as the first line, so get the bitfield out
        if key == 'ras_features':
            return int((value.split('\n')[0]).split(' ')[-1], 16)
        # The smc_fw_version sysfs file stores the version as a hex value like 0x12345678
        # but is parsed as int(0x12).int(0x34).int(0x56).int(0x78)
        if key == 'smc_fw_version':
            return (str('%02d' % int((value[2:4]), 16)) + '.' + str('%02d' % int((value[4:6]), 16)) + '.' +
                    str('%02d' % int((value[6:8]), 16)) + '.' + str('%02d' % int((value[8:10]), 16)))

        return ''

    def getFilePath(self, device, key):
        """ Return the filepath for a specific device and key

        Parameters:
        device -- Device whose filepath will be returned
        key -- [$valuePaths.keys()] The sysfs path to return
        """
        if key not in valuePaths.keys():
            print('Cannot get file path for key %s' % key)
            return None

        pathDict = valuePaths[key]
        fileValue = ''

        if pathDict['prefix'] == drmprefix:
            filePath = os.path.join(pathDict['prefix'], device, 'device', pathDict['filepath'])

        if not os.path.isfile(filePath):
            return None
        return filePath





