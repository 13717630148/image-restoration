import cv2
import numpy as np 

#读入图片
img = cv2.imread('./2.bmp' , 0)
f = np.fft.fft2(img)
fshift = np.fft.fftshift(f)
s1 = np.log(np.abs(fshift))
s1 *= 5

#填充矩阵H
H = np.ones(s1.shape , np.complex64)
center = (s1.shape[0]/2 , s1.shape[1]/2 )
c = 0.1
b = 0.1
T = 1
k = 1
for i in range(s1.shape[0]):
	for j in range(s1.shape[1]):
		temple = np.pi * ( (i - center[0]) * c + (j - center[1]) * b)
		if temple != 0:
			H[ i , j ] = T / (temple) * np.sin(temple) * np.exp(-temple * 1j ) * (((temple) * np.sin(temple)) ** 2 + k) / (((temple) * np.sin(temple)) ** 2)
		else:
			H[ i , j ] = T * np.exp(-temple * 1j )

#输出图片
img_new_fshift = fshift / H
img_new_fft = np.fft.ifftshift(img_new_fshift)
img_new = np.fft.ifft2(img_new_fft)
img_new = np.abs(img_new)
cv2.imwrite('result2.png' , img_new)
