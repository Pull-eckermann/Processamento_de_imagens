"""
results_CORREL = list()
results_CHISQR = list()
results_INTERSECT = list()
results_BHATTACHARYYA = list()

img1 = cv2.imread('b2.bmp')
img2 = cv2.imread('b1.bmp')

hist1 = cv2.calcHist([img1], [1], None, [256], [0,256])
hist2 = cv2.calcHist([img2], [1], None, [256], [0,256])

sc = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
print(sc)

cv2.imshow("Display window", img1)
k = cv2.waitKey(0)

plt.plot (hist1, color = 'r')
plt.xlim ([0,256])
plt.show ()
"""
