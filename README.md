# Tensile_multiprocess_train  
Description: A tool for tensile training(multicard support) based on python3.  


Usages:  
/bin/train is the top-level script. Below command line could be used for launching...  

cd ～/Tenslie_multiporcess_train  #enter the root folder  
scl enable devtoolset-7 bash  
python ./bin/train config_path output_path tensile_path [gpu]    
~ config_path  : required, specify the input yaml file.  
~ output_path  : required, sepcify the output folder.  
~ tensile_path : required, specify the root folder of tensile.    
~ gpu          : optional, specify the gpu index which will be used to trian, default is use all the gpu in that environment.  

example:  
python train ./rocblas_dgemm_nt_inc0.yaml ./output ~/Tensile/  -g 0 1 2 3   # use gpu 0 1 2 3 to train tensile  

after training, you will find "output" folder in the workdir, and it's tree struct as below:  

~ output  
    0_SplitConfigYaml      #Split config file for every gpu  
    1_BenchmarkProblems    #as folder name  
    2_BenchmarkData        #as folder name  
    3_LibraryLogic         #as folder name  
    4_LibraryClient        #as folder name  
    5_SplitTrainingLog     #Tensile log for every gpu  

