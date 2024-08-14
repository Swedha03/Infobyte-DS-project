from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.http import HttpResponseRedirect

# Create your views here.
def index(request):
    return render(request,"index.html")

def about(request):
    return render(request,"about.html")

def products(request):
    return render(request,"products.html")

def register(request):
    if request.method=="POST":
        first=request.POST['fname']
        last=request.POST['lname']
        un=request.POST['uname']
        em=request.POST['email']
        p1=request.POST['pwd']
        p2=request.POST['pwd1']
        if p1==p2:
            if User.objects.filter(email=em).exists():
                messages.info(request,"Email Exists")
                return render(request,"register.html")
            elif User.objects.filter(username=un).exists():
                messages.info(request,"Username available")
                return render(request,"register.html")
            else:
                user=User.objects.create_user(first_name=first,last_name=last,username=un,email=em,password=p2)
                user.save()
                return HttpResponseRedirect('login')
        else:
            messages.info(request,"Password not matching")
            return render(request,"register.html")
    else:
        return render(request,"register.html")
    
def login(request):
    if request.method=="POST":
        un=request.POST['uname']
        ps=request.POST['pwd']
        user=auth.authenticate(username=un,password=ps)
        if user is not None:
            auth.login(request,user)
            return HttpResponseRedirect('/')
        else:
            messages.info(request,"Invalid Credentials")
    
    return render(request,"login.html")

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

def data(request):
    if request.method=="POST":
        weight=int(request.POST['Item_Weight'])
        fat=request.POST['Item_Fat_Content']
        visibility=float(request.POST['Item_Visibility'])
        itemType=request.POST['Item_Type']
        mrp=float(request.POST['Item_MRP'])
        outletSize=request.POST['Outlet_Size']

        import pandas as pd
        df=pd.read_csv(r"static/datasets/salesPrediction.csv")
        print(df.head())
        print(df.isnull().sum())
        print(df.dropna(inplace=True))
        from sklearn.preprocessing import LabelEncoder
        l=LabelEncoder()

        fat1=l.fit_transform([fat])
        Fat_Content=l.fit_transform(df["Item_Fat_Content"])
        df["Fat_Content"]=Fat_Content

        itemType1=l.fit_transform([itemType])
        item_type=l.fit_transform(df["Item_Type"])
        df["item_type"]=item_type

        outletSize1=l.fit_transform([outletSize])
        outlet_size=l.fit_transform(df["Outlet_Size"])
        df["outlet_size"]=outlet_size

        X=df.drop(["Item_Identifier","Item_Fat_Content","Item_Type","Outlet_Identifier","Outlet_Establishment_Year","Outlet_Size","Outlet_Location_Type","Outlet_Type","Item_Outlet_Sales"],axis=1)
        #X=df["Item_Weight","Fat_Content","Item_Visibility","item_type","Item_MRP","outlet_size"]
        y=df["Item_Outlet_Sales"]
        from sklearn.linear_model import LinearRegression
        #from sklearn.linear_model import LogisticRegression
        model = LinearRegression()
        model.fit(X, y)
        #log=LogisticRegression()
        #log.fit(X,y)
        import numpy as np
        pred_input=np.array([[weight,fat1,visibility,itemType1,mrp,outletSize1]],dtype=object)
        pred_outcome = model.predict(pred_input)
        #pred_outcome=log.predict(pred_input)
        print(pred_outcome)
        return render(request,"predict.html",{"Item_Weight":weight,"Item_Fat_Content":fat,
        "Item_Visibility":visibility,"Item_Type":itemType,"Item_MRP":mrp,"Outlet_Size":outletSize,"prediction":pred_outcome})
    return render(request,"data.html")

def predict(request):
    return render(request,"predict.html")