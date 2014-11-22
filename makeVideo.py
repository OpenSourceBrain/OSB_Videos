import cv2
import cv
'''

            STILL IN DEVELOPMENT

            NOT YET A GENERAL PURPOSE SCRIPT!!!
            
            NEEDS MORE WORK...

'''

import argparse
import sys

width = 1280
height = 720
scale_font = 1

font = cv2.FONT_ITALIC
font_colour = (0,0,0)
font_colour_2 = (0,0,100)

fps = 24

HEADING_1 = "### "
HEADING_2 = "## "
HEADING_3 = "# "
VIDEO = "Video: "
TEXT = "TEXT"


section_screen = "Opening.png"


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

def parse_line(line):
    
    print(">>> Processing line {%s}"%line)
    duration = 2 
    
    if line.startswith(HEADING_1):
        l0 = line[len(HEADING_1):]
        type = HEADING_1
    elif line.startswith(HEADING_2):
        l0 = line[len(HEADING_2):]
        type = HEADING_2
    elif line.startswith(HEADING_3):
        l0 = line[len(HEADING_3):]
        type = HEADING_3
    elif line.startswith(VIDEO):
        l0 = line[len(VIDEO):]
        type = VIDEO
    elif len(line.strip())==0:
        return None, -1, -1
    else:
        type = TEXT
        l0 = line
    
    if '(' in l0:
        s = l0.index('(')
        e = l0.index(' sec', s)
        duration = float(l0[s+1:e])
        
        l0 = l0[:s]
         
    return l0, type, duration
        
    
def process_line(text, type, frames, frame_count, args):
    
    print("Adding %i frames, type %s with text: %s"%(frames, type, text))

    for i in range(frames):
        frame_count +=1
        background = None
        scale = 1
        fc = font_colour
        
        if type == HEADING_1:
            background = section_screen
            scale = 3
        if type == HEADING_2:
            background = section_screen
            scale = 1
        if type == TEXT:
            background = section_screen
            scale = 1
            fc = font_colour_2
            
        img = cv2.imread(background)

        show = False
        if show:
            cv2.imshow('Image: '+img_file,img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()


        cv2.putText(img,
                    'Frame: %i'%frame_count,(width-250,60), 
                    font, 
                    scale_font,
                    font_colour)

        cv2.putText(img, 
                    text,
                    (45,150), 
                    font, 
                    scale_font,
                    fc, 
                    scale_font)

        new_file = args.dir+'/frames/'+args.dir+"_%i.png"%frame_count
        cv2.imwrite(new_file,img)
        print("Written frame %i to %s"%(frame_count, new_file))

    return frame_count

    
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
        
        script = open(args.dir+"/Script.md", "r")
        
        frame_count = 0
        
        for line in script:
            l0, type, duration = parse_line(line)
 
            frame_count = process_line(l0, type, int(duration*fps), frame_count, args)

    

    if gen_movie:

        for i in range(frame_count):
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

        #format = 'avi'
        #format = 'mpg'
        format = 'divx'

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


