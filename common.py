import os
import sys

################################################################################
# Global vars
################################################################################
ROOT_DIR = os.getcwd()
WORK_DIR = ROOT_DIR + "/tmp"
CONFIG_DIR = WORK_DIR + "/config"
LOGIC_DIR  = WORK_DIR + "/logic"
LOG_DIR = WORK_DIR + "/LOG"
OUTPUT_DIR = ROOT_DIR  + "/output"

################################################################################
# Print Debug
################################################################################
def printWarning(message):
  print("Tensile::WARNING: {}".format(message))
  sys.stdout.flush()

def printExit(message):
  print("Tensile::FATAL: {}".format(message))
  sys.stdout.flush()
  sys.exit(-1)