import cv2
import numpy as np
from pyzbar.pyzbar import decode


def decoder(image):
    gray_img = cv2.cvtColor(image, 0)
    barcode = decode(gray_img)

    if len(barcode) == 1:
        obj = barcode[0]
        points = obj.polygon
        (x, y, w, h) = obj.rect
        pts = np.array(points, np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(image, [pts], True, (0, 255, 0), 3)
        barcodeData = obj.data.decode("utf-8")
        barcodeType = obj.type
        string = "Data " + str(barcodeData) + " | Type " + str(barcodeType)
        cv2.putText(frame, string, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
        print("Barcode: " + barcodeData + " | Type: " + barcodeType)
        return obj
    else:
        pass


def verify(x, y):
    print('verfied')




cap = cv2.VideoCapture(0)
id_store = ''
while True:
    ret, frame = cap.read()
    current = decoder(frame)
    try:
        if current.type == 'QRCODE' and len(id_store) == 0:
            id_store = current.data.decode("utf-8")
            print('yeah')
        elif current.type == 'CODE128' and len(id_store) != 0:
            verify(id_store, current.data.decode("utf-8"))
    except:
        pass
    cv2.imshow('Image', frame)
    code = cv2.waitKey(10)
    if code == ord('q'):
        break