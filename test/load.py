
import numpy as np
import cv2

video='bez-2018-01-25_10.38.27.avi'
cap = cv2.VideoCapture(video)
        
print("Successfully opened %s?: %s"%(video,cap.isOpened()))

local_frames = 0
ret = True
while(ret):
    print('Reading frame: %s'%local_frames)
    # Capture frame-by-frame
    success, imgv = cap.read()
    print('Read...')
    if not success:
        print("End of de video - successful read: %s, open still: %s, local_frames=%s"%(success,cap.isOpened(),local_frames))
        break

    # Our operations on the frame come here
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    #cv2.imshow('frame',frame)
    #if cv2.waitKey(1) & 0xFF == ord('q'):
    #    break
        
    local_frames+=1

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()