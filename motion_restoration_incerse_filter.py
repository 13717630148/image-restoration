import cv2
import numpy as np 

#读入图片
img = cv2.imread('./2.bmp' , 0)
f = np.fft.fft2(img)
fshift = np.fft.fftshift(f)
s1 = np.log(np.abs(fshift))
s1 *= 5

#填充H矩阵
H = np.ones(s1.shape , np.complex64)
center = (s1.shape[0]/2 , s1.shape[1]/2 )
c = 0.1
b = 0.1
T = 1
for i in range(s1.shape[0]):
	for j in range(s1.shape[1]):
		temple = np.pi * ( (i - center[0]) * c + (j - center[1]) * b)
		if temple != 0:
			H[ i , j ] = T / (temple) * np.sin(temple) * np.exp(-temple * 1j )
		else:
			H[ i , j ] = T * np.exp(-temple * 1j )

#除去H
img_new_fshift = fshift / H

#对输出图片频谱进行处理，对于过大的值使用其周围的值的平均值进行替换
for i in range(s1.shape[0]):
	for j in range(s1.shape[1]):
		if np.abs(img_new_fshift[i , j]) > 5 *  np.abs(img_new_fshift[256 , 256]):
			if i != 0 and i != 511 and j != 0 and j != 511:
				img_new_fshift[i , j] = (img_new_fshift[i-1 , j] + img_new_fshift[i+1,j] + img_new_fshift[i , j-1] + img_new_fshift[i , j+1])/4
			elif i == 0:
				img_new_fshift[i , j] = img_new_fshift[i+1 , j]
			elif i == 511:
				img_new_fshift[i , j] = img_new_fshift[i-1 , j]
			elif j == 0:
				img_new_fshift[i , j] = img_new_fshift[i , j+1]
			elif j == 511:
				img_new_fshift[i , j] = img_new_fshift[i , j-1]
		else:
			pass

#输出图片
img_new_fft = np.fft.ifftshift(img_new_fshift)
img_new = np.fft.ifft2(img_new_fft)
img_new = np.abs(img_new)
cv2.imwrite('result1.png' , img_new)
