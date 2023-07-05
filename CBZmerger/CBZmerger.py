
""" SANTIAGO VALLE - CBZmerger """

import os
from zipfile import ZipFile
import re
import shutil

#Requesting to user necessary stuffs
print('To start please type the directory of the CBZ files to merge (IMPORTANT: Put / at the end)')
print('Example: D:\\User\\Desktop\\')
directory = input()
directory = directory.replace("\\", "/") #Replace the \ symbol to / which i use in code

print('\nType the name of the merged file (Example: One Piece - Volume 2)')
merged_name = input()

print('\nType how many files do you want to merge (Example: 18)')
numfiles = input()

print('\nType 1 if the CBZ files are named "Episode XX" or write another number in case they are named "Chapter XX"')
print('IMPORTANT: The CBZ files must be named "Episode XX" or "Chapter XX" (XX is replaced by the corresponding number)')
opt = input()

if opt==1:
    print('\nType the name of the first CBZ file (Example: Episode 32)')
    print('IMPORTANT: If we follow the example the others files must be named Episode 33, Episode 34, etc.')
else:
    print('\nType the name of the first CBZ file (Example: Chapter 32)')
    print('IMPORTANT: If we follow the example the others files must be named Chapter 33, Chapter 34, etc.')
firstfile = input()

files = []

print('\nMerging',numfiles, 'CBZ files with the following order:')

#Define function to increment chapter/episode from the data given by the user
def increment_chapter(text,option):
    if option==1:
        pattern = r'Episode (\d+)'
    else:
        pattern = r'Chapter (\d+)'

    match = re.search(pattern, text)

    if match:

        chapter_number = int(match.group(1))

        incremented_chapter = chapter_number + 1
        if option==1:
            modified_text = re.sub(pattern, f'Episode {incremented_chapter}', text)
        else:
            modified_text = re.sub(pattern, f'Chapter {incremented_chapter}', text)

        return modified_text
    else:
        return text

#Show on console the complete order of the CBZ files to merge
files.append(firstfile)
print('\t',firstfile)

file_plus = increment_chapter(firstfile,opt)
files.append(file_plus)
print('\t',file_plus)

for i in range(int(numfiles)-2):
    file_plus = increment_chapter(file_plus,opt)
    files.append(file_plus)
    print('\t',file_plus)
  
# Convert CBZ files to ZIP and Unzip CBZ files into the Temp(New folder) subdirectories
for i in range(int(numfiles)):
    cbz_file = str(directory)+str(files[i])+'.cbz'
    zip_file = str(directory)+str(files[i])+'.zip'
    os.rename(cbz_file, zip_file)
    with ZipFile(zip_file, 'r') as f:
        f.extractall(str(directory)+'Temp/'+str(i+1))

print('\nMerging in process, please don\'t delete the new directory "Temp" untill the merge finalize')

# Convert ZIP files to CBZ (Returning CBZ files to their original format)
for i in range(int(numfiles)):
    cbz_file = str(directory)+str(files[i])+'.cbz'
    zip_file = str(directory)+str(files[i])+'.zip'
    os.rename(zip_file, cbz_file)

dir_temp = str(directory)+'Temp/'
cbz_infiles = os.listdir(dir_temp+str(1))
j = len(cbz_infiles)+1

# Rename unzipped files to the correct format
for i in range(int(numfiles)):   
    if i != 0:
        k = os.listdir(dir_temp+str(i+1))
        for w in range(len(k)):
            if w<9:
                old_name = dir_temp+str(i+1)+'/'+'0'+str(w+1)+'.jpg'
            else:
                old_name = dir_temp+str(i+1)+'/'+str(w+1)+'.jpg'
            new_name = dir_temp+str(i+1)+'/'+str(j)+'.jpg'
            os.rename(old_name, new_name)
            j = j+1
 
# Zip renamed files           
with ZipFile(str(directory)+str(merged_name)+'.zip', 'w') as f:
    for folder, subfolders, files in os.walk(dir_temp):
        for file in files:
            if file.endswith('.jpg'):
                f.write(os.path.join(folder, file), file)


# Removing Temp directory
shutil.rmtree(dir_temp)

# Convert ZIP file to CBZ (Merge completed)
cbz_file = str(directory)+str(merged_name)+'.cbz'
zip_file = str(directory)+str(merged_name)+'.zip'
os.rename(zip_file, cbz_file)

print('\nDone! Now you can enjoy your merged CBZ file')