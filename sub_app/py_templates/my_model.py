from PIL import Image
import numpy as np
import onnxruntime
import os
import cv2
from statistics import mode


image_path=os.path.dirname(os.path.dirname(__file__))
ort_session1 = onnxruntime.InferenceSession('sub_app/py_templates/efficientnet_lite0.onnx')
ort_session2 = onnxruntime.InferenceSession('sub_app/py_templates/mobilenetv3_rw.onnx')
ort_session3 = onnxruntime.InferenceSession('sub_app/py_templates/mobilenetv2_100.onnx')

def getimg(test_path):
    img = Image.open(image_path+test_path).convert('L')
    img=img.resize((224,224))
    img=np.array(img)
    blur = cv2.GaussianBlur(img,(5,5),0)
    ret3,img = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    img=img/255
    img=np.expand_dims(img,0)
    img=np.expand_dims(img,0)
    img=img.astype(np.float32)#ort require float instead of double
    return img

from decimal import Decimal
def p_root(value, root):
     
    root_value = 1 / float(root)
    return round (Decimal(value) **
             Decimal(root_value), 3)
def minkowski_distance(x, y, p_value=2):
    return (p_root(sum(pow(abs(a-b), p_value)
            for a, b in zip(x, y)), p_value))


def getembs(img1,img2,ort_session):
    inp1 = {ort_session.get_inputs()[0].name: img1}
    emb1= ort_session.run(None, inp1)[0]
    inp2 = {ort_session.get_inputs()[0].name: img2}
    emb2= ort_session.run(None, inp2)[0]
    
    return emb1.ravel(),emb2.ravel()

def getdist(p1,p2,ort_session):
    img1=getimg(p1)
    img2=getimg(p2)
    emb1o,emb2o=getembs(img1,img2,ort_session)
    r=minkowski_distance(emb1o,emb2o)
    return r

def get_ensemble_results(p1,p2,thresh=0.6):
    r1=getdist(p1,p2,ort_session1)
    r2=getdist(p1,p2,ort_session2)
    r3=getdist(p1,p2,ort_session3)
    print(r1,r2,r3)
    r1='Forged' if r1 > thresh else 'Genuine'
    r2='Forged' if r2 > thresh else 'Genuine'
    r3='Forged' if r3 > thresh else 'Genuine'
    print(r1,r2,r3)
    r=mode([r1,r2,r3])
    return r
