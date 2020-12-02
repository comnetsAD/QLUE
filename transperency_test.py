import cv2
import numpy as np
import coreFunctions


"""
### This acts as a base layer
base = cv2.imread("one.png")


### This is the component to be cropped
### In actual implementation this could be looped over
baseCropped = base[180:570,480:1200,:]

layer1 = np.zeros((base.shape[0], base.shape[1], base.shape[2]))

### These are the x1,y1 for component in the actual image
### Don't forget to add a check for when this returns -1 for match not found
topX, topY =  coreFunctions.find_image(base,baseCropped)

### make an empty mask with 4th space on the 3rd dimention
### shape[2] is (R,G,B,Alpha) where alpha is transparence [0-255]
baseMasked = np.zeros((base.shape[0],base.shape[1],4))

### set the alpha = 255 for the entire mask to make it opaque
baseMasked[:,:,3] = np.full((base.shape[0],base.shape[1]),255)

### add the (R,G,B) values of the original base image in the mask
baseMasked[:,:,0:3] = base

print(baseCropped.shape)

### set the alpha for the component as zero
baseMasked[topX:topX+baseCropped.shape[0],topY:topY+baseCropped.shape[1],3] = np.zeros((baseCropped.shape[0], baseCropped.shape[1]))
"""

base = cv2.imread("one.png")
baseCropped = base[180:570,480:1200,:]
topX, topY =  coreFunctions.find_image(base,baseCropped)

topX -=1
topY -=1

base[topX:topX+baseCropped.shape[0],topY:topY+baseCropped.shape[1],:] -= baseCropped



# x = base[topX:topX+baseCropped.shape[0],topY:topY+baseCropped.shape[1],:]
# print(np.unique(x.flatten()))

cv2.imwrite("comp.png", baseCropped)
cv2.imwrite("out.png", base)
