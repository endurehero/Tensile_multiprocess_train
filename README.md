# Tensile_multiprocess_train
Description: A tool for tensile training(multicard support, currently only support dgemm case) based on python3.


Usages:
/bin/train is the top-level script. Below command line could be used for launching...

cd ～/Tenslie_multiporcess_train  #enter the root folder
scl enable devtoolset-7 bash
python ./bin/train config_path tensile_path [gpu]
- config_path  : required, specify the input yaml file.
- tensile_path : required, specify the root folder of tensile
- gpu          : optional, specify the gpu index which will be used to trian, default is use all the gpu in that environment.

example:
python train ./rocblas_dgemm_nt_inc0.yaml ~/Tensile/  -g 0 1 2 3   # use gpu 0 1 2 3 to train tensile

after training, you will find "output" folder in the workdir, and it's tree struct as below:

-output
--config (store the config yaml file which be splited from input yaml config file)
--LOG    (store the training log for every gpus)
--logic  (store the logic file for splited config yaml file and the final result)


so, you can find the result in the folder "output/logic/final/"
