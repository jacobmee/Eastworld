#!/bin/bash
# script to backup Pi SD card
# 2015-11-28
#DSK='disk4'
# Find disk with LInux partition (works for Raspbian)
export DSK=`diskutil list | grep "Linux" | cut -c 69-73 | head -1`
if [ $DSK ]; then
    echo $DSK
else
    echo "Disk not found"
    exit
fi
diskutil unmountDisk /dev/$DSK
echo please wait - This takes some time
echo Ctl+T to show progress!
time sudo dd if=/dev/r$DSK bs=4m | gzip -9 > ~/Piback.img.gz
#rename to current date
echo compressing completed - now renaming
mv -n ~/Piback.img.gz ~/Piback`date +%Y%m%d`.img.gz

#sudo gzip -dc /XXXimage.gz | dd bs=4m of=/dev/XXX