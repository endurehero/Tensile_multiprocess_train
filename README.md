# Tensile_multiprocess_train
Description: A tool for tensile training(multicard support, currently only support dgemm case).


Usages:

/bin/train is the top-level script. Below command line could be used for launching...

cd .../bin/
python train config_path tensile_path [gpu]

example:
python train ./rocblas_dgemm_nt_inc0.yaml ~/Tensile/  -g 0 1 2 3   # use gpu 0 1 2 3 to train tensile


the result will be found in folder "output/logic/final/"