
from scipy.spatial import distance as dist
import imutils
from imutils import contours
from datetime import datetime
from imutils import perspective
import numpy as np
import argparse
import cv2
import os
import shutil
import requests
import json



url = 'http://localhost:5000/data'  # Flask 애플리케이션의 주소

headers = {'Content-Type': 'application/json'}  # 요청 헤더에 Content-Type 추가
def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5 ) #중앙좌표 설정



folder_path = 'img'
target_path  =  'img2'
image_files = sorted([f for f in os.listdir(folder_path) if f.endswith((".jpg", ".jpeg"))])

image_path = os.path.join(folder_path, image_files[0]) 

image = cv2.imread(image_path , cv2.IMREAD_COLOR)
image =  rotated = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (7,7), 0)

edged = cv2.Canny(gray, 75, 255)
edged = cv2.dilate(edged, None, iterations=1)
edged = cv2.erode(edged, None, iterations=1)

ret, binary = cv2.threshold(gray, 70, 255, cv2.THRESH_OTSU) #데이터전처리 작업

cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_TC89_L1) #윤곽선추출
cnts = imutils.grab_contours(cnts)

(cnts, _) = contours.sort_contours(cnts)
pixelsPerMetric = 12.72 #픽셀당 매트리스 비율설정
for i in range(1): #박스형 크기 추출 반목문
    
    for c in cnts:
    
     if cv2.contourArea(c) < 10:
        continue

     orig = image.copy()
     box = cv2.minAreaRect(c)
     box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
     box = np.array(box, dtype="int")


     box = perspective.order_points(box)
     cv2.drawContours(orig, [box.astype("int")], -1, (255, 255, 0), 2)   

     for (x, y) in box:
       cv2.circle(orig, (int(x), int(y)), 3, (0, 0, 255), -1)


       (tl, tr, br, bl) = box
       (tltrX, tltrY) = midpoint(tl, tr)
       (blbrX, blbrY) = midpoint(bl, br)

       (tlblX, tlblY) = midpoint(tl, bl)
       (trbrX, trbrY) = midpoint(tr, br)

       cv2.circle(orig, (int(tltrX), int(tltrY)), 8, (255, 0, 0), -1)
       cv2.circle(orig, (int(blbrX), int(blbrY)), 8, (255, 0, 0), -1)
       cv2.circle(orig, (int(tlblX), int(tlblY)), 8, (255, 0, 0), -1)
       cv2.circle(orig, (int(trbrX), int(trbrY)), 8, (255, 0, 0), -1)

       cv2.line(orig, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)),
           (255, 0, 255), 1)
       cv2.line(orig, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)),
           (255, 0, 255), 1)

       dA = 29.70 #A4용지 세로
       dB = 21.00 #A4용지 가로
       dC = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
       dD = dist.euclidean((tlblX, tlblY), (trbrX, trbrY)) #유클리디안 거리계산함수

       if pixelsPerMetric is None:
          pixelsPerMetric = dB

       dimA = dA 
       dimB = dB 
       dimC = dC / pixelsPerMetric
       dimD = dD / pixelsPerMetric 

    
       #cv2.putText(orig, "{:.2f} cm ".format(dimA),
         # (int(tltrX - 20), int(tltrY - 15)), cv2.FONT_HERSHEY_SIMPLEX,
         # 0.5, (255, 255, 255), 1)
       #cv2.putText(orig, "{:.2f} cm".format(dimB ),
         # (int(trbrX + 10), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX,
         # 0.5, (255, 255, 255), 1)

       cv2.putText(orig, "{:.2f} cm".format(dimC),
          (int(trbrX -70), int(trbrY-225)), cv2.FONT_HERSHEY_SIMPLEX,
          0.7, (125, 255, 255), 1)
       cv2.putText(orig, "{:.2f} cm".format(dimD),
          (int(trbrX ), int(trbrY+30)), cv2.FONT_HERSHEY_SIMPLEX,
          0.7, (12, 255, 255), 1)
        
       cv2.drawContours(orig, cnts, 1, (0, 255, 0), 2)
        

       # show the output image
       #cv2.imshow("kim.jpg", orig)
       cv2.waitKey(0)
    
    for i in range(1): #지정된 자표 출력 반목문

     x = int(cnts[i][5][0][0]) 
     y = int(cnts[i][5][0][1])  

     circle1_x, circle1_y = x +120, y + 43
     circle2_x, circle2_y = x +120, y + 820 #총장

     circle3_x, circle3_y = x +400, y + 70
     circle4_x, circle4_y = x -145, y + 50

     #circle5_x, circle5_y = x +455, y + 110
     #circle6_x, circle6_y = x -250, y + 110 #어꺠넓이

     circle7_x, circle7_y = x + 410, y + 320
     circle8_x, circle8_y = x - 168, y + 320

     circle9_x, circle9_y = x - 340, y + 180
     circle10_x, circle10_y = x + 175, y + 180


     cv2.circle(orig, (circle1_x, circle1_y), 3, (255, 255, 0), 3) 
     cv2.circle(orig, (circle2_x, circle2_y), 3, (255, 255, 0), 3)  #총장

     cv2.circle(orig, (circle3_x, circle3_y), 3, (255, 0, 255), 3)  
     cv2.circle(orig, (circle4_x, circle4_y), 3, (255, 0, 255), 3)  

     #cv2.circle(orig, (circle5_x, circle5_y), 3, (0, 0, 0), 3)  
     #cv2.circle(orig, (circle6_x, circle6_y), 3, (0, 0, 0), 3)  #어꺠넓이

     cv2.circle(orig, (circle7_x, circle7_y), 3, (111, 111, 111), 3) 
     cv2.circle(orig, (circle8_x, circle8_y), 3, (111, 111, 111), 3)  #가슴넙이

     cv2.circle(orig, (circle9_x, circle9_y), 3, (50, 50, 255), 3)
    # cv2.circle(orig, (circle10_x, circle10_y), 3, (50, 50, 255), 3)   


     d1 = dist.euclidean((circle1_x, circle1_y), (circle2_x, circle2_y))
 
     d2 = dist.euclidean((circle3_x, circle3_y), (circle4_x, circle4_y))

    # d3 = dist.euclidean((circle5_x, circle5_y), (circle6_x, circle6_y))

     d4 = dist.euclidean((circle7_x, circle7_y), (circle8_x, circle8_y))

     d5 =  dist.euclidean((circle4_x, circle4_y), (circle9_x, circle9_y))

   #  d6 =  dist.euclidean((circle4_x, circle4_y), (circle6_x, circle6_y))

     damA = d1/pixelsPerMetric
     damB = d2/pixelsPerMetric
     #damC = d3/pixelsPerMetric
     damD = d4/pixelsPerMetric
     damE = d5/pixelsPerMetric
    # damF = d6/pixelsPerMetric

     cv2.line(orig, (circle1_x, circle1_y), (circle2_x, circle2_y), (255, 255, 0), 1)
     cv2.line(orig, (circle3_x, circle3_y), (circle4_x, circle4_y), (255, 0, 255), 1)
    #cv2.line(orig, (circle5_x, circle5_y), (circle6_x, circle6_y), (0, 0, 0), 1)
     cv2.line(orig, (circle7_x, circle7_y), (circle8_x, circle8_y), (111, 111, 111), 1)
 
   # cv2.line(orig, (circle6_x, circle6_y), (circle9_x, circle9_y), (111, 111, 111), 1)
     cv2.line(orig, (circle4_x, circle4_y), (circle9_x, circle9_y), (111, 111, 111), 1)


     cv2.putText(orig, "{:.2f} cm".format(damA),
     (int(x-30), int(y+440)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0 ), 1)

     cv2.putText(orig, "{:.2f} cm".format(damB),
     (int(x-30), int(y-30)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (125, 255, 255), 1)

     #cv2.putText(orig, "{:.2f} cm".format(damC),
     #(int(x-300), int(y+60)), cv2.FONT_HERSHEY_SIMPLEX,1, (0,0,0 ), 1)

     cv2.putText(orig, "{:.2f} cm".format(damD),
     (int(x-350), int(y+180)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0 ), 1)


     cv2.putText(orig, "{:.2f} cm".format(damE),
     (int(x-350), int(y+130)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0 ), 1)
     
     #cv2.putText(orig, "{:.2f} cm".format(damF),
     #(int(x-260), int(y+20)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (125, 255, 255), 1)
    
     print("{:.1f}".format(damA)) #총장
     print("{:.1f}".format(damB)) #어꺠넓이
     print("{:.1f}".format(damD)) # 가슴넓이
     print("{:.1f}".format(damE)) #소매길이


    data = {
    'damA': "{:.1f}".format(damA),
    'damB': "{:.1f}".format(damB),
    'damD': "{:.1f}".format(damD),
    'damE': "{:.1f}".format(damE)
}

response = requests.post(url, headers=headers, json=data)
print(response.content)  # 서버 응답 확인
now = datetime.now()
timestamp = now.strftime("%Y%m%d%H%M%S")
save_path = os.path.join(target_path, f"{timestamp}.jpg")
cv2.imwrite(save_path, image)


   
     #cv2.imshow("kim.jpg", orig)
cv2.waitKey(0)
