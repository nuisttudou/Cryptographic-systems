from LSBSteg import LSBSteg
import cv2
import matplotlib.pyplot as plt

#encoding
steg = LSBSteg(cv2.imread("carrier.png"))
new_im = steg.encode_image(cv2.imread("lena.png"))
cv2.imwrite("new_image.png", new_im)

#decoding
steg = LSBSteg(cv2.imread("new_image.png"))
orig_im = steg.decode_image()
cv2.imwrite("recovered.png", orig_im)