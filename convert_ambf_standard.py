# import relevant classes
import sys
import os
import cv2 as cv
import glob
import argparse
from Scripts.image import ImageCustom

# ---------------------------------------------
# parse arguments
# ---------------------------------------------
argv = sys.argv
parser = argparse.ArgumentParser(description='find the location and the correct label of the to-be-processed dataset')

parser.add_argument('-f', '--folder', type=str, required=True,
                    help='the location of the to be processed images')
parser.add_argument('-r', '--rec', type=str, required=True,
                    help='the label of the recording')

args = parser.parse_args()

# ---------------------------------------------
# output path setup
# ---------------------------------------------
if not os.path.exists(os.path.join(os.getcwd(), 'output')):
    os.mkdir(os.path.join(os.getcwd(), 'output'))

folder_name = os.path.join(os.getcwd(), 'output')
sub_folder_name = os.path.join(os.getcwd(), os.path.join('output', args.rec))
if not os.path.exists(sub_folder_name):
    os.mkdir(sub_folder_name)

category = ['raw', 'ambf', 'annotation2colors', 'annotation4colors', 'annotation5colors']
for catg in category:
    category_folder_name = os.path.join(os.getcwd(),
                                        os.path.join('processed',
                                                     os.path.join(args.rec, catg)))
    if not os.path.exists(category_folder_name):
        os.mkdir(category_folder_name)

# ---------------------------------------------
# output file setup
# ---------------------------------------------
width, height = 1280, 480
frameSize = (int(width / 2), height)
fourcc = cv.VideoWriter_fourcc(*'DIVX')
out = cv.VideoWriter("ambf_endo_" + args.rec + "_seg.avi", fourcc, 30, frameSize)

filenames = glob.glob(os.getcwd() + "/*.png")
filenames.sort()
# images = [cv.imread(img) for img in filenames]

# ---------------------------------------------
# start processing raw images
# ---------------------------------------------
for img in filenames:

    cur_img = ImageCustom(img)
    for x in range(3):
        new_img = cur_img.set_annotation(x)
        cv.imwrite(cur_img.seg_str, new_img)
        out.write(new_img)
        cv.imshow('frame', new_img)

    if cv.waitKey(1) == ord('q'):
        break

out.release()
cv.destroyAllWindows()