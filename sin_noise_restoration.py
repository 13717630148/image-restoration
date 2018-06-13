#对正弦噪声污染后的图像进行复原
#王道烩   无52   2015011006   13020023780@163.com
#2018.6.11

import cv2
import numpy as np  

#读入图片
img = cv2.imread('./1.bmp' , 0)

#对图片进行二维傅丽叶变换
f = np.fft.fft2(img)

#由于变换完之后，x，y分别为从0-2pi ,这样会使得低频分量对应图像的四个角落。
#使用fftshift函数是将图像重新平移，使得图像的x，y取值为从-pi~pi这样对应正中心为低频分量，外围为高频分量。
fshift = np.fft.fftshift(f)

#将变换后的系数区绝对值并取对数，取对数是为了让图像看起来更好。
s1 = np.log(np.abs(f))
s2 = np.log(np.abs(fshift))

#经测试，直接画图整体比较黑，所以将每个值都扩大5倍，效果较好。
s1 *= 5
s2 *= 5

#mask为滤波器，观察可知正弦噪声的中心频点在(182 ,  74) , (74 , 182)位置处，同时设置滤波器的半径，观察对比现象。
mask = np.ones(s1.shape , np.uint8)
r =   20;

#填充mask
row  , colum = s1.shape
for i in range(row):
	for j in range(colum):
		if (i - 182) ** 2 + (j - 74 ) ** 2 <= r ** 2 or (i - 74) ** 2 + (j - 182 ) ** 2 <= r ** 2 :
			mask[i , j ] = 0

cv2.circle(s2 , (182 , 74) , r , (255 , 255 , 255) , 1)
cv2.circle(s2 , (74 , 182) , r , (255 , 255 , 255) , 1)
cv2.imwrite('fft_masked.png' , s2)

#滤波
fshift_masked = fshift * mask

#重新恢复到0-2pi
fshift_masked_ishift = np.fft.ifftshift(fshift_masked)

#逆变换得到处理后的图像
img_new = np.fft.ifft2(fshift_masked_ishift)
img_new = np.abs(img_new)
cv2.imwrite('new.png' , img_new)

#打印新图片的频谱
s2  = s2 * mask
cv2.imwrite('fft_newimg.png' , s2)