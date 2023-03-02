# import relevant classes
import cv2 as cv
import glob


# background = [104 104 104]
# arm dark grey = [54 54 54]
# arm light grey = [89 89 89]
# arm joint = [125 125 125]
# needle = [87 87 87]
# find the instrument, thread, and needle according to BGR color
def detect(frame, x, y):
    B = frame.item(x, y, 0)
    G = frame.item(x, y, 1)
    R = frame.item(x, y, 2)

    test1 = B == 54 and G == 54 and R == 54
    test2 = B == 89 and G == 89 and R == 89
    test3 = B == 125 and G == 125 and R == 125
    test4 = B == 87 and G == 87 and R == 87
    test5 = 0 <= B <= 10 and 0 <= G <= 10 and 0 <= R <= 10
    if test1 is True or test2 is True or test3 is True or test4 is True or test5 is True:
        return True
    else:
        return False


# iterate through the image
def process(frame):
    global width, height
    new_frame = frame
    for i in range(0, height):
        for j in range(int(width / 2), width):
            if detect(frame, i, j):
                new_frame[i, j] = [255, 255, 255]
            else:
                new_frame[i, j] = [0, 0, 0]

    return new_frame[:, int(width / 2):width]


# process video
name1 = "output1"
width, height = 1280, 480
frameSize = (int(width / 2), height)
fourcc = cv.VideoWriter_fourcc(*'DIVX')
out = cv.VideoWriter("ambf_endo_"+name1+"_seg.avi", fourcc, 26, frameSize)

filenames = glob.glob(name1+"/*.png")
filenames.sort()
images = [cv.imread(img) for img in filenames]

for img in images:
    processed_img = process(img)
    out.write(processed_img)
    cv.imshow('frame', processed_img)
    if cv.waitKey(1) == ord('q'):
        break

out.release()
cv.destroyAllWindows()
