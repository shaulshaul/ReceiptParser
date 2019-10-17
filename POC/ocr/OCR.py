try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import io
from io import BytesIO
import cv2
import base64

def ocr_core_path(filename):
    """
    This function will handle the core OCR processing of images.
    """
    text = pytesseract.image_to_string(Image.open(filename))  # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
    return text

def image_from_b64string(base64_string):
    # Create imaage from base64 string
    a = {}
    start_index = base64_string.index(b'base64') + 6
    a['img'] = base64_string[start_index:]

    im = Image.open(BytesIO(base64.b64decode(a['img'])))
    return im

def ocr_core(base64_string):
    """
    This function will handle the core OCR processing of images.
    """
    # Create image from base64 string
    im = image_from_b64string(base64_string)
    # Now working with image
    image = im

    # If need to perform rotation:
    rotation = False
    if rotation:
    # Edit the image to make it more readable
        rotated_image = rotate(im)
        image = rotated_image

    text = pytesseract.image_to_string(image)  # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
    return text

# Helpers for better images
def rotate(image):
    # load the image from disk
    # image = cv2.imread(file_name)

    # convert the image to grayscale and flip the foreground
    # and background to ensure foreground is now "white" and
    # the background is "black"
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)

    # threshold the image, setting all foreground pixels to
    # 255 and all background pixels to 0
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # grab the (x, y) coordinates of all pixel values that
    # are greater than zero, then use these coordinates to
    # compute a rotated bounding box that contains all
    # coordinates
    coords = np.column_stack(np.where(thresh > 0))
    angle = cv2.minAreaRect(coords)[-1]

    # the `cv2.minAreaRect` function returns values in the
    # range [-90, 0); as the rectangle rotates clockwise the
    # returned angle trends to 0 -- in this special case we
    # need to add 90 degrees to the angle
    if angle < -45:
        angle = -(90 + angle)

    # otherwise, just take the inverse of the angle to make
    # it positive
    else:
        angle = -angle

    # rotate the image to deskew it
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h),
        flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    #cv2.imwrite(output_file_name, rotated)

    # # draw the correction angle on the image so we can validate it
    # cv2.putText(rotated, "Angle: {:.2f} degrees".format(angle),
    #     (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # # show the output image
    # print("[INFO] angle: {:.3f}".format(angle))
    # cv2.imshow("Input", image)
    # cv2.imshow("Rotated", rotated)
    # cv2.waitKey(0)
    return rotated

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# print(ocr_core(r"D:\Projects\ReceiptParser\POC\Images\2.png"))