from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.shortcuts import render
import pickle
from django.views.decorators.csrf import csrf_exempt
import json
import os
import cv2
import shutil
import skimage
from skimage.transform import resize
from sklearn.utils import shuffle
from skimage.color import rgb2gray
import numpy as np
from keras.models import model_from_json
json_file = open('./Forestmodel.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
#load weights into new model
loaded_model.load_weights("./Forestmodel30.h5")
print("Loaded model from disk")
def videoToImage(file):
    cap=cv2.VideoCapture(file)
    dir = './temp/'
    try:
        shutil.rmtree(dir)
    except:
        pass
    i = 0       #starting index for the loop
    while(cap.isOpened()):  #creating while loop
        flag, frame = cap.read()  #declaring flag and frame variable
        if flag == False:         #creating condition after limit exceed break
            break
        if not os.path.exists(os.path.dirname(dir)):
            os.makedirs(os.path.dirname(dir))

        path = dir+ str(i) +'.jpg' #specifying path and name
        cv2.imwrite(path,frame)
        i+=1
    cap.release()
    cv2.destroyAllWindows()

def pred_outcome(img,loaded_model):
    z=[]
    print(img.shape)
    img = skimage.transform.resize(img,(224,224,3), anti_aliasing=True)
    print(img.shape)
    img = np.asarray(img)
    z.append(img)
    z = np.asarray(z)
    classes_names=['no_fire', 'fire', 'start_fire']
    nbr_classes=3
    predictions=loaded_model.predict(z)[0]
    result = [(classes_names[i], float(predictions[i]) * 100.0) for i in range(nbr_classes)]
    result.sort(reverse=True, key=lambda x: x[1])
    print(result[0][0])
    return result[0][0]

@csrf_exempt
def FireClassifier(request):
    try:
        print("######",request)
        if request.FILES:
            print("yesss")
            files = request.FILES.getlist('file')
            dir = './videoFol/'
            if not os.path.exists(os.path.dirname(dir)):
                os.makedirs(os.path.dirname(dir))
            for f in files:
                with open(dir + str(f), 'wb') as dest:
                    for chunk in f.chunks():
                        dest.write(chunk)
            videoToImage('./videoFol/'+ str(f))
            flag=0
            img_dir = './temp/'
            for elem in os.listdir(img_dir):
                imgage_file=cv2.imread(os.path.join(img_dir,elem))
                result=pred_outcome(imgage_file,loaded_model)
                if result=='fire':
                    flag=1
                    break
                elif result=='start_fire':
                    flag=2
                    break
                else:
                    continue
            if flag==1:
                return JsonResponse({"Msg":'Fire'},status=201 )
            elif flag==2:
                return JsonResponse({"Msg":'Start Fire'},status=201 )
            else:
                return JsonResponse({"Msg":'No Fire'},status=201 )
    except Exception as e:
        print(e)
        return JsonResponse({"Msg":'Unexpected Error'+str(e)},status=500)

@csrf_exempt
def index(request):
    return render(request,'index.html')
