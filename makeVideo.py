import cv2
import cv
import colorsys
'''

            STILL IN DEVELOPMENT

            NOT YET A GENERAL PURPOSE SCRIPT!!!
            
            NEEDS MORE WORK...

'''

import argparse
import sys

width = 800
height = 600
scale_font = 1

font = cv2.FONT_HERSHEY_COMPLEX_SMALL
font_colour = (10,10,10)


def process_args():
    """ 
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(description='A file for generating videos for OSB from simple Markdown based "scripts"')


                        
    parser.add_argument('-title', 
                        type=str, 
                        metavar='<title>', 
                        default='Introduction to the Open Source Brain repository',
                        help='Title for movie')
                        
                        
    parser.add_argument('-frames', 
                        type=int,
                        metavar='<frames>',
                        default=50,
                        help='Number of frames')

                        
    parser.add_argument('-dir', 
                        type=str, 
                        metavar='<directory of script>', 
                        help='Directory of the script file, e.g. Introduction')
                        
    return parser.parse_args()

        

    
def main (argv):
    
    args = process_args()
    
    print("Making an OSB movie....")
    
    img_files_pre = []
    img_files_post = []

    gen_images = True
    gen_movie = False
    
    #gen_images = False
    gen_movie = True
    

    if gen_images:

        for i in range(args.frames+1):
            index = str(i)
            while len(index)<3: index="0"+index
            img_files_pre.append("Opening.png")
            

        for i in range(len(img_files_pre)):
            img_file = img_files_pre[i]
            img = cv2.imread(img_file)
            print("Read in file: %s"%img_file)
            show = False
            if show:
                cv2.imshow('Image: '+img_file,img)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

            t = 0 + i*float(200)/args.frames
            
            cv2.putText(img,'Time: %.3fms'%t,(width-220,50), font, 1,font_colour,scale_font)

            cv2.putText(img,args.title,(45,150), font, 1,font_colour,scale_font*2)

            new_file = args.dir+'/frames/'+args.dir+"_%i.png"%i
            cv2.imwrite(new_file,img)
            print("Written %s"%new_file)



    if gen_movie:

        for i in range(args.frames+1):
            #index = str(i)
            #while len(index)<3: index="0"+index

            new_file = args.dir+'/frames/'+args.dir+"_%i.png"%i
            img_files_post.append(new_file)

        imgs = []

        for i in range(len(img_files_post)):
            img_file = img_files_post[i]
            img = cv2.imread(img_file)
            print("Read in %s"%img_file)
            imgs.append(img)

        format = 'avi'
        #format = 'mpg'
        #format = 'divx'

        fps = 24
        if format is 'avi':
            fourcc = cv.CV_FOURCC('X','V','I','D')
            mov_file = args.dir+'.avi'
            out = cv2.VideoWriter(mov_file,fourcc, fps, (width,height))
        if format is 'divx':
            fourcc = cv.CV_FOURCC('D','I','V','X')
            mov_file = args.dir+'.avi'
            out = cv2.VideoWriter(mov_file,fourcc, fps, (width,height))
        if format is 'mpg':
            fourcc = cv.CV_FOURCC('M','J','P','G')
            mov_file = args.dir+'.mpg'
            out = cv2.VideoWriter(mov_file,fourcc, fps, (width,height))

        f = 0
        for img in imgs:
            print("Writing frame %i"%f)
            f+=1
            out.write(img)

        out.release()
        print("Saved movie file %s"%mov_file)


    print "Done!"



if __name__ == '__main__':
    main(sys.argv)


