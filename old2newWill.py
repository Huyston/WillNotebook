'''Converts the old .will format to the new one. Use as follows:
Create a folder and copyy this script to that folder. Move the old .will file to that folder and other related files, if they exist,
like the Images folder and the database.bib file. Then, using the command prompt, execute the script like this:

python old2newWill.py <old.will> <Optional: new.will>

A file new.will will be created including the database.will and the images in the Images folder.'''

import tarfile
import sys
import os

try:
    old = sys.argv[1]
except IndexError:
    print('You must specify the file to be converted.')
    sys.exit()
try:
    new = sys.argv[2]
except IndexError:
    new = 'new'+old

if not 'database.bib' in os.listdir():
    with open('database.bib','w') as db:
        pass
if not 'Images' in os.listdir():
    os.mkdir('Images')

os.rename(old,old.replace('.will','.wnb'))
with tarfile.open(new,'w:xz') as will:
    will.add(old.replace('.will','.wnb'))
    will.add('database.bib')
    will.add('Images')

print('File successfuly converted to '+new)
