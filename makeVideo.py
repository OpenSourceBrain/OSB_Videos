
'''

            STILL IN DEVELOPMENT

            NOT YET A GENERAL PURPOSE SCRIPT!!!
            
            NEEDS MORE WORK...

'''

from __future__ import print_function
import argparse
import sys
import cv2
import os
import numpy as np
from PIL import ImageFont, ImageDraw, Image  
    
#import svgwrite
#import cairosvg

#
hd = False
hdhalf = True
hd = True

if hd:
    width = 1578
    height = 794
    width = 1280
    height = 720
    width = 1600
    height = 900
    suffix='_HD'
elif hdhalf:
    width = 960
    height = 540
    suffix='_HDh'
else:
    width = 640
    height = 360
    suffix=''

scale_font = 1

font = cv2.FONT_ITALIC
font_colour = (0,0,0)
font_colour_2 = (0,0,100)

fps = 30
fps_in = 30

TRANSITION1 = 1 # e.g. first intro slide
TRANSITION2 = 2.2 # internal intro slide
INFO1 = 1.5 # internal intro slide
INFO2 = 2.5 # internal intro slide
INFO3 = 3.5 # internal intro slide
INFO4 = 4.5 # internal intro slide


HEADING_1 = "# "
HEADING_2 = "## "
HEADING_3 = "### "
COMMENT = "//"
VIDEO = "Video: "
FRAME = "Frame: "
TEXT = "TEXT"
BLANK = "BLANK"

interpolation = cv2.INTER_AREA

section_screen = "Opening.png"
section_screen = "Opening2.png"


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

def parse_seconds(sec_num):
    
    if sec_num=='TRANSITION1':
        sec_num = TRANSITION1
    elif sec_num=='TRANSITION2':
        sec_num = TRANSITION2
    elif sec_num=='INFO1':
        sec_num = INFO1
    elif sec_num=='INFO2':
        sec_num = INFO2
    elif sec_num=='INFO3':
        sec_num = INFO3
    elif sec_num=='INFO4':
        sec_num = INFO4
    duration = float(sec_num)
    
    return duration
    

def parse_line(line):
    
    print(">>> Processing line {%s}"%line.strip())
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
        l0 = line[len(VIDEO):].strip()
        type = VIDEO
    elif line.startswith(FRAME):
        l0 = line[len(FRAME):].strip()
        type = FRAME
    elif line.startswith(COMMENT):
        return None, BLANK, -1
    elif len(line.strip())==0:
        return None, BLANK, -1
    else:
        type = TEXT
        l0 = line
    
    if type != FRAME:
        if '(' in l0:
            s = len(l0) - 1 - l0[::-1].index('(')
            e = l0.index(' sec', s)
            sec_num = l0[s+1:e]
            duration = parse_seconds(sec_num)

            l0 = l0[:s]

    return l0, type, duration

def add_overlay(img, frame_count):

        cv2.putText(img,
                    'Frame: %i'%frame_count,(width-250,60), 
                    font, 
                    scale_font,
                    font_colour_2)
                    
def add_text(img, text, location, scale, font_colour):
    
    
    '''
    temp_file =  text.replace(' ','_')+'.png'
    dwg = svgwrite.Drawing(temp_file, (200, 200), debug=True)
    paragraph = dwg.add(dwg.g(font_size=14))
    paragraph.add(dwg.text(text, (10,20)))
    dwg.save(temp_file)
    print("Loading: %s"%temp_file)
    s_img = cv2.imread(temp_file)
    print s_img
    y_offset = location[0]
    x_offset = location[1]
    print y_offset
    print x_offset
    img[y_offset:y_offset+s_img.shape[0], x_offset:x_offset+s_img.shape[1]] = s_img'''
    
    '''
    cv2.putText(img, 
                text,
                location, 
                font, 
                scale_font,
                font_colour, 
                scale_font*scale)'''
                
    lines = text.split('\\n')
    
    for i in range(len(lines)):
               
        
        #Based on http://www.codesofinterest.com/2017/07/more-fonts-on-opencv.html
        # Convert the image to RGB (OpenCV uses BGR)  
        cv2_im_rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)  

        # Pass the image to PIL  
        pil_im = Image.fromarray(cv2_im_rgb)  

        draw = ImageDraw.Draw(pil_im)  
        # use a truetype font  
        #font = ImageFont.truetype("arial.ttf", int(24*scale))
        font = ImageFont.truetype("Arial Unicode.ttf", int(24*scale))

        y_offset = location[0]+i*30*scale
        x_offset = location[1]
        # Draw the text  
        draw.text((x_offset, y_offset), lines[i], font=font, fill=(font_colour[2],font_colour[1],font_colour[0],255))  

        # Get back the image to OpenCV  
        img = cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGB2BGR)  
    
    return img
 
def add_box(img, top, bottom, outline_colour, fill_colour):
    
    #Based on http://www.codesofinterest.com/2017/07/more-fonts-on-opencv.html
    # Convert the image to RGB (OpenCV uses BGR)  
    cv2_im_rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)  

    # Pass the image to PIL  
    pil_im = Image.fromarray(cv2_im_rgb)  

    draw = ImageDraw.Draw(pil_im)  

    draw.rectangle([(top[0], top[1]), (bottom[0], bottom[1])], \
              outline=(outline_colour[2],outline_colour[1],outline_colour[0],255), \
              fill=(fill_colour[2],fill_colour[1],fill_colour[0],255))  

    # Get back the image to OpenCV  
    img = cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGB2BGR)  
    
    return img
   
    
def process_line(text, type, frames, frame_count, args):
    
    if type == BLANK:
        return frame_count
    
    
    if type == FRAME:
        
        caption = text.split(';')[1].strip()
        
        w = text.split(';')[0].split()
        video = args.dir+'/'+w[0]
        
        frame_timepoint = float(w[1])
        frame_duration = parse_seconds(w[2])
        extra_frames = int(frame_duration * fps)
        print("Adding frame at %s sec from: [%s] & displaying for %s sec (%s frames), with caption: %s..."%(frame_timepoint, video, frame_duration, extra_frames, caption[:25]))
               
        v = cv2.VideoCapture(video)
        
        local_frames = 0
        added = False
        while True:
            success, imgv = v.read()

            if not success:
                print("End of the video")
                break

            w = np.size(imgv, 1)
            h = np.size(imgv, 0)
            #print("Frame is %i x %i"%(w,h))

            local_frames +=1
            local_t = float(local_frames)/fps_in
            
            if local_t>=frame_timepoint and not added:
                added = True
                frame_count +=1

                global_t = float(frame_count)/fps
                #img = cv2.imread(section_screen)

                
                scale = 1
                fc = font_colour
                
                img = add_box(imgv, (180,500), (1100,650), (0,0,100), (250,250,250))
                
                img = add_text(img, caption, (520,250), scale, font_colour_2)
                
                #img[:(min(h,height)), :(min(w,width))] = imgv[:(min(h,height)), :(min(w,width))]
                img = cv2.resize(img,(width, height), interpolation = interpolation)

                #add_overlay(img, frame_count)
                frame_dir = args.dir+'/frames/'
                if not os.path.isdir(frame_dir):
                    print("Making dir: "+frame_dir)
                    os.path.mkdir(frame_dir)
                
                for i in range(extra_frames):
                    new_file = frame_dir+args.dir+"_%i.png"%frame_count
                    cv2.imwrite(new_file,img)
                    print("Written frame %i to %s (frame %i of %s; local t=%s sec; global t=%s sec)"%(frame_count, new_file, local_frames, video,local_t, global_t))
                    
                    local_frames +=1
                    frame_count +=1
                    global_t = float(frame_count)/fps
            else:
                pass
                #print("Skipping frame %i at time %s sec; "%(local_frames, local_t),end="")
          
        ##v.release()
    
    elif type == VIDEO:
        
        w = text.split()
        video = args.dir+'/'+w[0]
        
        print("Adding a video from: [%s] with opencv %s"%(video, cv2.__version__))
        if not os.path.isfile(video):
            print('Video file %s not found!!'%video)
            exit()
        start_times = [0]
        end_times = [1e12]
        if len(w)>1:
            start_times = []
            end_times = []
            for b in w[1].split('&'):
                start_times.append(float(b.split('-')[0]))
                end_times.append(1e12 if b.split('-')[1]=='end' else float(b.split('-')[1]))
        
        v = cv2.VideoCapture(video)
        ##v.open(video)
        
        print("Successfully opened %s?: %s"%(video,v.isOpened()))
        print("Starts: %s, ends: %s"%(start_times, end_times))
        
        local_frames = 0
        while True:
            success, imgv = v.read()
            print('Read...')
            if not success:
                print("End of de video - successful read: %s, open still: %s, local_frames=%s"%(success,v.isOpened(),local_frames))
                break

            w = np.size(imgv, 1)
            h = np.size(imgv, 0)
            
            print("Frame %s is %i x %i"%(local_frames,w,h))
            
            local_frames +=1
            local_t = float(local_frames)/fps_in
            
            for i in range(len(start_times)):
                start_time = start_times[i]
                end_time = end_times[i]
                
                if local_t>start_time and local_t<end_time:

                    frame_count +=1

                    global_t = float(frame_count)/fps
                    img = cv2.imread(section_screen)

                    #img[:(min(h,height)), :(min(w,width))] = imgv[:(min(h,height)), :(min(w,width))]
                    img = cv2.resize(imgv,(width, height), interpolation = interpolation)

                    #add_overlay(img, frame_count)
                    frame_dir = args.dir+'/frames/'
                    if not os.path.isdir(frame_dir):
                        print("Making dir: "+frame_dir)
                        os.path.mkdir(frame_dir)
                    new_file = frame_dir+args.dir+"_%i.png"%frame_count
                    cv2.imwrite(new_file,img)
                    print("Written frame %i to %s (frame %i of %s; local t=%s sec; global t=%s sec)"%(frame_count, new_file, local_frames, video,local_t, global_t))
                else:
                    pass
                    #print("Skipping frame %i at time %s sec; "%(local_frames, local_t),end="")
                    
        ##v.release()
                
    else:

        print("Adding %i frames, type %s with text: {%s}"%(frames, type, text))

        sub = None
        if '-' in text:
            w = text.split('-')
            text = w[0].strip()
            sub = w[1].strip()
            print("  subheading: %s"%sub)

        for i in range(frames):
            frame_count +=1
            
            global_t = float(frame_count)/fps
            background = None
            scale = 1
            fc = font_colour
            
            scale_big = 2.5
            scale_mid = 1.7

            if type == HEADING_1:
                background = section_screen
                scale = scale_big
            if type == HEADING_2:
                background = section_screen
                scale = scale_mid
            if type == HEADING_3:
                background = section_screen
                scale = scale_mid
            if type == TEXT:
                background = section_screen
                scale = scale_mid
                #fc = font_colour_2

            img = cv2.imread(background)

            show = False
            if show:
                cv2.imshow('Image: '+img_file,img)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            
            img = add_text(img, text, (45,150), scale, fc)
            if sub:
                img = add_text(img, sub, (145,220), scale_mid, font_colour_2)
                
            #img[:(min(h,height)), :(min(w,width))] = imgv[:(min(h,height)), :(min(w,width))]
            img = cv2.resize(img,(width, height), interpolation = interpolation)

            frame_dir = args.dir+'/frames/'
            if not os.path.isdir(frame_dir):
                print("Making dir: "+frame_dir)
                os.mkdir(frame_dir)
            new_file = frame_dir+args.dir+"_%i.png"%frame_count
            cv2.imwrite(new_file,img)
            print("Written the frame %i to %s, t=%s sec"%(frame_count, new_file, global_t))

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


        #format = 'mpg'
        #format = 'divx'
        format = 'mov'
        format = 'mpg'
        format = 'mp4h'
        #format = 'avi'

        if format == 'avi':
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            mov_file = args.dir+suffix+'.avi'
            out = cv2.VideoWriter(mov_file,fourcc, fps, (width,height))
        if format == 'divx':
            #fourcc = cv.CV_FOURCC('D','I','V','X')
            fourcc = cv2.VideoWriter_fourcc(*'DIVX')
            mov_file = args.dir+suffix+'.avi'
            out = cv2.VideoWriter(mov_file,fourcc, fps, (width,height))
        if format == 'mov':
            #fourcc = cv.CV_FOURCC('D','I','V','X')
            fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
            mov_file = args.dir+suffix+'.mov'
            out = cv2.VideoWriter(mov_file,fourcc, fps, (width,height))
        if format == 'mpg':
            #fourcc = cv.CV_FOURCC('M','J','P','G')
            #fourcc = cv2.VideoWriter_fourcc(*'MJPG')
            fourcc = cv2.VideoWriter_fourcc('m', 'j', 'p', 'g') # note the lower case
            mov_file = args.dir+suffix+'.mpg'
            out = cv2.VideoWriter(mov_file,fourcc, fps, (width,height))
            
        if format == 'mp4h':
            #fourcc = cv.CV_FOURCC('M','J','P','G')
            #fourcc = cv2.VideoWriter_fourcc(*'MJPG')
            
            fourcc = cv2.VideoWriter_fourcc(*'H264')
            #fourcc = cv2.VideoWriter_fourcc('m', 'j', 'p', 'g') # note the lower case
            mov_file = args.dir+suffix+'.mp4'
            out = cv2.VideoWriter(mov_file,fourcc, fps, (width,height))
            print('vvvvvvv')
            print(fourcc)
            
        if format == 'mp4':
            #fourcc = cv.CV_FOURCC('M','J','P','G')
            #fourcc = cv2.VideoWriter_fourcc(*'MJPG')
            
            fourcc = cv2.VideoWriter_fourcc(*'MP4V')
            #fourcc = cv2.VideoWriter_fourcc('m', 'j', 'p', 'g') # note the lower case
            mov_file = args.dir+suffix+'.mp4'
            out = cv2.VideoWriter(mov_file,fourcc, fps, (width,height))

        f = 0
        for i in range(len(img_files_post)):
            img_file = img_files_post[i]
            img = cv2.imread(img_file)
            print("Read in %s"%img_file)
            f+=1
            print("Writing frame %i/%i"%(f,len(img_files_post)))
            out.write(img)

        out.release()
        global_t = float(frame_count)/fps

        print("*************************************************\n    Saved movie file %s, total length: %s seconds\n*************************************************"%(mov_file,global_t))

    print("Done with %s!"%sys.version)



if __name__ == '__main__':
    main(sys.argv)


