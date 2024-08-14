from django.shortcuts import render
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder

def index(request):
    return render(request, "index.html")

def about(request):
    return render(request, "about.html")



from django.shortcuts import render
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

# Path to the saved model and dataset
dataset_path = 'static\dataset\car_prices.csv'

def load_model():
    # Load and prepare the dataset
    data = pd.read_csv(dataset_path)
    data = pd.get_dummies(data)  # One-hot encoding for categorical variables
    X = data.drop('price', axis=1)
    y = data['price']

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Model training
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f'Mean Squared Error: {mse}')
    
    return model, X.columns

def data(request):
    if request.method == "POST":
        # Capture input data
        brand = request.POST.get('brand', '')
        model_name = request.POST.get('model', '')
        year = request.POST.get('year', '')
       
        fuel_type = request.POST.get('fuel_type', '')
        transmission = request.POST.get('transmission', '')

        # Check if any required field is missing
        if not (brand and model_name and year  and fuel_type and transmission):
            return render(request, "data.html", {
                "error": "Please provide all required input values."
            })

        # Convert input values to appropriate types
        try:
            year = float(year)
            
        except ValueError:
            return render(request, "data.html", {
                "error": "Please enter valid numeric values for year ."
            })

        # Load the model and prepare data for prediction
        model, X_columns = load_model()

        # Prepare example data
        example_data = pd.DataFrame({
            'brand': [brand],
            'model': [model_name],
            'year': [year],
            
            'fuel_type': [fuel_type],
            'transmission': [transmission],
            
        })

        # One-hot encoding for categorical features
        example_data = pd.get_dummies(example_data)
        example_data = example_data.reindex(columns=X_columns, fill_value=0)

        # Make prediction
        price_prediction = model.predict(example_data)[0]

        # Render result
        return render(request, "predict.html", {
            "brand": brand,
            "model": model_name,
            "year": year,
            "fuel_type": fuel_type,
            "transmission": transmission,
            "prediction": price_prediction
        })
    else:
        return render(request, "data.html")

def predict(request):
    return render(request, "predict.html")
