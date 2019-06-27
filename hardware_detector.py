import os
import re

class HardwareDetector:
    def __init__(self):
        self.gpu_num = 0
        self.gpu = []
        
        self.gpu_num = self.listDevices()
        if self.gpu_num == 0:
            return

        self.gpu = range(0,self.gpu_num)
    
    def listDevices(self):
        """ Return a list of GPU devices."""
        devicelist = [device for device in os.listdir('/sys/class/drm') if re.match(r'^card\d+$', device)]
        return len(devicelist)
