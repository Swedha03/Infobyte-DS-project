from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.http import HttpResponseRedirect

# Create your views here.
def index(request):
    return render(request,"index.html")

def about(request):
    return render(request,"about.html")
def data(request):
    if request.method=="POST":
        SL=float(request.POST['LSepal'])
        SW=float(request.POST['WSepal'])
        PL=float(request.POST['LPetal'])
        PW=float(request.POST['WPetal'])
        from django.conf import settings
        import os
        import pandas as pd 
        csv_path = os.path.join(settings.BASE_DIR, 'static/dataset/Iris.csv')
        
        df = pd.read_csv(csv_path)
        print(df.head)
        print(df.isnull().sum())
        print(df.dropna(inplace=True))
        from sklearn.preprocessing import LabelEncoder
        l=LabelEncoder()
        X=df.drop("Species",axis=1)
        y=df["Species"]
        from sklearn.linear_model import LogisticRegression
        log=LogisticRegression()
        log.fit(X,y)
        import numpy as np 
        pred_input=np.array([[SL,SW,PL,PW]],dtype=object)
        pred_outcome=log.predict(pred_input)
        print(pred_outcome)
        return render(request,"recommend.html",{"LSepal":SL,"WSepal":SW,"LPetal":PL,"WPetal":PW,"prediction":pred_outcome})
        
    return render(request,"data.html")
def recommend(request):
    return render(request,"recommend.html")

  

# Create your views here.
