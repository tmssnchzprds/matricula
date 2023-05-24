import cv2
import pytesseract
import re

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
placa = []
coches = ['img/coche1.jpg', 'img/coche2.jpg', 'img/coche3.jpg', 'img/coche4.jpg', 'img/coche5.jpg', 'img/coche6.jpg', 'img/coche7.jpg', 'img/coche8.jpg', 'img/coche9.jpeg', 'img/coche10.jpeg', 'img/coche11.jpeg', 'img/coche12.jpeg']
for coche in coches:
    image = cv2.imread(coche)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.blur(gray, (3, 3))
    canny = cv2.Canny(gray, 100, 150)
    canny = cv2.dilate(canny, None, iterations=1)
    #cv2.imshow('canny', canny)
    # _,cnts,_ = cv2.findContours(canny,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    cnts, _ = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(image,cnts,-1,(0,255,0),2)

    for c in cnts:
        area = cv2.contourArea(c)

        x, y, w, h = cv2.boundingRect(c)
        epsilon = 0.08 * cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, epsilon, True)

        if 2 < len(approx) and 2000 < area:
            aspect_ratio = float(w) / h
            if 1.8 < aspect_ratio:
                placa = gray[y:y + h, x:x + w]
                text = pytesseract.image_to_string(placa, config='--psm 8')
                txt = text.split(' ')
                for t in txt:
                    if (len(t) == 4) and t.isdigit():
                        s = t
                    elif (len(t) == 5) and t.isdigit():
                        s = t[1:]
                    elif len(t) == 3:
                        s = s +' '+ t
                    elif 3 < len(t) < 6:
                        s = s +' '+ t[:3]
                if 's' != '' and re.match(r'(\d{4})( )([A-Z]{3})', s):
                    cv2.drawContours(image, [approx], 0, (0, 255, 0), 3)
                    print('area=', area)
                    print('PLACA DE ',coche,': ', s)
                    #cv2.imshow('PLACA', placa)
                    #cv2.moveWindow('PLACA', 780, 10)
                    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 3)
                    cv2.putText(image, s, (x - 20, y - 10), 1, 2.2, (0, 255, 0), 3)
                    s = ''
    cv2.imshow('Image', image)
    cv2.moveWindow('Image', 45, 10)
    cv2.waitKey(0)
