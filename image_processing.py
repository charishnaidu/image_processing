# Import necessary packages
# https://auth0.com/blog/image-processing-in-python-with-pillow/#Resizing-Images
import argparse
import glob
import re
import cv2
import os
from PIL import Image
import shutil

numbers = re.compile(r'(\d+)')


def numerical_sort(value):
    # function that splits text part and numerical part in the string
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts


def modify_frames(frames, video_name):
    if os.path.exists('./{}'.format(video_name)):
        shutil.rmtree('./{}'.format(video_name))
        os.makedirs('./{}'.format(video_name))
    else:
        os.makedirs('./{}'.format(video_name))

    full_path = os.path.join(frames, '*.png')
    all_images = glob.glob(full_path)
    all_images = sorted(all_images, key=numerical_sort)

    all_heights = []
    for filename in all_images:
        background_img = Image.open('./white.png')
        img = Image.open(filename)
        img.thumbnail((240, 400))
        actual_size = img.size
        # print(actual_size[0])
        # position = ((0,0))
        position = (int((240-actual_size[0])/2), int((400-actual_size[1])/2))
        background_img.paste(img, position)
        background_img.save('./{}/{}'.format(video_name, filename[-14:]))


def create_white_image():
    img = Image.new('RGB', (240, 400), color='white')
    img.save('white.png')


def merge_images(folder_1, folder_2):
    # 1st folder with images
    list_1 = os.listdir(folder_1)
    list_1 = sorted(list_1, key=numerical_sort)

    # 2nd folder with images
    list_2 = os.listdir(folder_2)
    list_2 = sorted(list_2, key=numerical_sort)

    # 3rd and so on can added if needed

    # Creating an empty folder with the name of folder_1 for saving the merged frames
    out_path = os.path.join('./merged_frames', os.path.basename(folder_1))
    os.makedirs(out_path, exist_ok=True)

    # Check whether both the folder contains equal number of frames or not
    if len(list_1) != len(list_2):
        raise ValueError('Frames in both folders are not equal')
    else:
        total_frames = len(list_1)
        for i in range(0, total_frames):
            im1 = os.path.join(folder_1, list_1[i])
            im2 = os.path.join(folder_2, list_2[i])
            # im3 and son on can be added here if needed

            list_ims = [im1, im2]
            images = [Image.open(i) for i in list_ims]
            widths, heights = zip(*(i.size for i in images))

            total_width = sum(widths)
            max_height = max(heights)

            new_im = Image.new('RGB', (total_width, max_height))

            x_offset = 0
            for im in images:
                new_im.paste(im, (x_offset, 0))
                x_offset += im.size[0]

            new_im.save(out_path + '/frame_%04d.png' % i)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Data pre processing')
    parser.add_argument('--frames', type=str, default='', help='path and folder name of frames')
    parser.add_argument('--vname', type=str, default='', help='name of the video')
    parser.add_argument('--folder1', type=str, default='', help='Folder containing frames')
    parser.add_argument('--folder2', type=str, default='', help='Folder containing frames')
    args = parser.parse_args()
    # create_white_image()
    # modify_frames(args.frames, args.vname)

    merge_images(args.folder1, args.folder2)
    '''
    To run the file for merging frames use the following command
    python image_processing.py --folder1 Path_of_the_folder --folder2 Path_of_the_folder
    '''

