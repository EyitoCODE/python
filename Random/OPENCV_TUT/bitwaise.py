import cv2 as cv
import numpy as np

blank = np.zeros((400,400), dtype='uint8')

rectangle =cv.rectangle(blank.copy(), (30,30), (370, 370), 255, -1)
circle = cv.circle(blank.copy(), (200, 200), 200, 255, -1)

cv.imshow('Rect', rectangle)
cv.imshow('Circle', circle)

#bitwise AND --- INTERSECTING REGION
bitwise_and = cv.bitwise_and(rectangle, circle)
cv.imshow('Bitwise and',bitwise_and)

#BITWISE OR --- non-INTERSECTING REGION and INTERSECTING REGION
bitwise_or = cv.bitwise_or(rectangle, circle)
cv.imshow('Bitwise OR',bitwise_or)

#BITWISE XOR --- non-INTERSECTING REGION
bitwise_xor = cv.bitwise_xor(rectangle, circle)
cv.imshow('Bitwise xor',bitwise_xor)

#BITWISE NOT
bitwise_not = cv.bitwise_not(rectangle)
cv.imshow('rect not',bitwise_not)
bitwise_not = cv.bitwise_not(circle)
cv.imshow('circle not',bitwise_not)

cv.waitKey(0)