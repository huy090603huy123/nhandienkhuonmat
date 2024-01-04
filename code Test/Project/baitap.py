import cv2
import numpy as np 
import matplotlib.pyplot as plit


trainingData = np.random.randint(0, 100 , (25,2)).astype(np.float32);

ketqua = np.random.randint(0,2 ,(25,1)).astype(np.float32);
red = trainingData[ketqua.ravel()==1]
blue = trainingData[ketqua.ravel()==0]
newmember = np.random.randint(0 , 100,(1,2)).astype(np.float32);
print (trainingData)
print (ketqua)
print (red)
 



plit.scatter(red[:,0], red[:,1], 100 , 'r','s')
plit.scatter(blue[:,0], blue[:,1], 100 , 'b','^')
plit.scatter(newmember[:,0], newmember[:,1], 100 , 'g','o')

knn = cv2.ml.KNearest_create()
knn.train(trainingData, 0 ,ketqua)
temp,ketqua , Nguoigan ,khoangcach = knn.findNearest(newmember,3)

print("ketqua : {}\n".format(ketqua));
print("nguoi gan : {}\n".format(Nguoigan));
print("khoang cach : {}\n".format(khoangcach));
plit.show()