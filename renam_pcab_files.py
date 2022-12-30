# In this prigram all *.csv files rename to a format which I can call them in a loop and run functions
import os
import glob

# It is the folder path which includes pcab files saved in csv format
folder_path = r'C:\Users\hosam\Documents\Professor Bruno\OpenPLC\PCAB\pcab files'

# I change os folder to which pcab csv files are located
os.chdir(folder_path)

# In this loop, all detected csv files will rename to specific names which ends from 01 - ...
## I am in need of a counter
i = 1
## Rename procedure has don in this loop with the help of 'glob' library
for file_01 in glob.glob('*.csv'):
    if i < 10:
        name_variable = str('0' + str(i))
    else:
        name_variable = str(i)
    file_name = 'Pcab ' + str(name_variable) + ' 221222.csv'
    os.rename(file_01, file_name)
    i += 1
