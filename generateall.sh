set -e

TARGET="SuppVideo1"


BACKUP_DIR="backup/$TARGET-`date +%H_%M_%S-%y_%m_%d`"

mkdir $BACKUP_DIR
cp $TARGET/*.avi $BACKUP_DIR
rm -f $TARGET/frames/*.png

#python makeVideo.py -dir Introduction
#python makeVideo.py -dir ExploringModelsOnOSB
#python makeVideo.py -dir NeuronsAndNetworksOnOSB

#python makeVideo.py -dir Video1
python makeVideo.py -dir $TARGET


cp $TARGET.avi $BACKUP_DIR

cp $TARGET/*.avi ../Dropbox/work/OSB_Videos/src/$TARGET
cp $TARGET*.avi ../Dropbox/work/OSB_Videos/

echo "Backed up to: "$BACKUP_DIR