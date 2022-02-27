from django.shortcuts import render

# Create your views here.
import Preprocessing as preprocess

from django.http import JsonResponse
from django.shortcuts import render
import pickle
from django.views.decorators.csrf import csrf_exempt
import json
@csrf_exempt
def Classifier(request):
    try:
        print(request.body.decode('utf-8'))
        data = request.body.decode('utf-8')
        dict=json.loads(data)
        Rawtweet= dict['Raw_tweet']
        CleanTweet=preprocess.preprocess_tweet(Rawtweet)
        vectorizer = pickle.load(open('./Vectorizer','rb'))
        model = pickle.load(open('./LRclassifier','rb'))
        pred = model.predict(vectorizer.transform([Rawtweet]))[0]
        if pred==0:
            return JsonResponse({"Msg":'NoHate'} ,status=201)
        else:
            return JsonResponse({"Msg":'Hateful Tweet'},status=201 )
    except Exception as e:
        return JsonResponse({"Msg":'Unexpected Error'+str(e)},status=500)

@csrf_exempt
def index(request):
    return render(request,'index.html')
