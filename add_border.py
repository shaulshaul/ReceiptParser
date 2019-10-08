# -*- coding: utf-8 -*-
import cv2

def main():
    image = cv2.imread('noisy1.png')
    new_image = add_border(image)
    cv2.imwrite('noisy1_border.png', new_image)


def add_border(image):
    border_size = 10
    border_color = [255,255,255] # white
    output_image = cv2.copyMakeBorder(image, top= border_size, bottom= border_size, left= border_size, right= border_size, borderType=cv2.BORDER_CONSTANT, value=border_color)
    return output_image



if __name__ == '__main__':
    main()