import glob
import os
import shutil

# FFMPEG command
# ffmpeg -r 12 -pattern_type glob -i '*.jpg' -start_number 0060 -i %04d.jpg -s hd1080 -vcodec libx264 timelapse.mp4

fdir = '/Users/alexsavattone/Downloads/images/'
fdir2 = '/Users/alexsavattone/Downloads/images/seq/'

file_list = glob.glob('{}*.jpg'.format(fdir))
file_list.sort(key=os.path.getmtime)

list2 = []
for i in file_list:
    list2.append(os.path.basename(i))

# print(list2)
i = 1
for f in list2:
    shutil.copy('{}{}'.format(fdir, f), '{}{:04d}.jpg'.format(fdir2, i))
    i += 1
