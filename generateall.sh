set -e

#conda activate CV2


TARGET="test"
TARGET="SuppVideo1"
TARGET="SuppVideo2"
TARGET="SuppVideo3"
TARGET="Promo"

TARGET="cVideo2"
TARGET="c302Full"
TARGET="c302FW"
TARGET="c302Sibernetic"
TARGET="NWBE"
TARGET="NP8"
TARGET="Human"


BACKUP_DIR="backup/$TARGET-`date +%H_%M_%S-%y_%m_%d`"

mkdir $BACKUP_DIR
cp $TARGET/*.avi $TARGET/*.mov $BACKUP_DIR 2>/dev/null || :
rm -f $TARGET/frames/*.png

#python makeVideo.py -dir Introduction
#python makeVideo.py -dir ExploringModelsOnOSB
#python makeVideo.py -dir NeuronsAndNetworksOnOSB

#python makeVideo.py -dir Video1
python makeVideo.py -dir $TARGET


#cp $TARGET.avi $BACKUP_DIR

cp $TARGET/*.mov ../Dropbox/work/OSB_Videos/src/$TARGET 2>/dev/null || :
cp $TARGET*.mov ../Dropbox/work/OSB_Videos/ 2>/dev/null || :
cp $TARGET*.mp4 ../Dropbox/work/OSB_Videos/ 2>/dev/null || :

echo "Backed up to: "$BACKUP_DIR
