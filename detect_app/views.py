from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
import joblib
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import sqlite3
import pandas as pd
def home(request):
    return render(request, 'home.html')

def predict(request):
    if request.method == 'POST' and request.FILES:
        # Get the selected model from the POST request
        model_choice = request.POST.get('model')
        uploaded_file = request.FILES['file']
        print(uploaded_file)
        csv_file = pd.read_csv(uploaded_file)
        print(csv_file)

        # Load the corresponding model based on user's choice
        if model_choice == 'knn':
            scaler=joblib.load( r'C:\Users\Mrudul\Documents\PDD\detect_app\model\scaler_model.joblib')
            model_path = r'detect_app\model\KNN_parkinsons_model.joblib'
            model = joblib.load(model_path)
           # aa=pd.read_csv(uploaded_file)
            prediction_data = csv_file.drop(columns=['name', 'status'])
            ans=np.array([prediction_data])
            print(ans[0][0])
            new_data_point_scaled = scaler.transform(ans[0][0].reshape(1, -1))
            model_path2 = r'detect_app\model\pca_model.joblib'
            pca2=joblib.load(model_path2)
            new_data_point_pca = pca2.transform(new_data_point_scaled)
            prediction = model.predict(new_data_point_pca)
            if prediction[0] == 1:
                prediction2 = model.predict_proba(new_data_point_pca)[0,1]
                prediction2=prediction2*100
                prediction_text = "You have Parkinson's Disease."
            else:
                prediction2 = model.predict_proba(new_data_point_pca)[0,0]
                prediction2=prediction2*100
                prediction_text = "You are healthy."
        elif model_choice == 'svm':
            model_path = r'detect_app\model\svm_parkinsons_model2.joblib'
            scaler=joblib.load( r'C:\Users\Mrudul\Documents\PDD\detect_app\model\scaler_model.joblib')
            model = joblib.load(model_path)
            prediction_data = csv_file.drop(columns=['name', 'status'])
            ans=np.array([prediction_data])
            print(ans[0][0])
            new_data_point_scaled = scaler.transform(ans[0][0].reshape(1, -1))
            prediction = model.predict(new_data_point_scaled)
            if prediction[0] == 1:
                prediction2 = model.predict_proba(new_data_point_scaled)[0,1]
                prediction2=prediction2*100
                prediction_text = "You have Parkinson's Disease."
            else:
                prediction2 = model.predict_proba(new_data_point_scaled)[0,0]
                prediction2=prediction2*100
                prediction_text = "You are healthy."
            
          
        elif model_choice == 'random_forest':
            model_path = r'detect_app\model\random_forest_model.joblib'
            model = joblib.load(model_path)
            #uploaded_file = request.FILES['file']

            # Assume 'name' and 'status' are columns you don't need for prediction
            prediction_data = csv_file.drop(columns=['name', 'status'])
            print(prediction_data)
            print(type(prediction_data))
            prediction = model.predict(prediction_data)

            # Depending on your model output, adjust the following condition accordingly
            if prediction[0] == 1:  # Assuming the model returns a list of predictions
                prediction2 = model.predict_proba(prediction_data)[0,1]
                prediction2=prediction2*100
                prediction_text = "You have Parkinson's Disease."
            else:
                prediction2 = model.predict_proba(prediction_data)[0,0]
                prediction2=prediction2*100
                prediction_text = "You are healthy."

        else:
            # Default to a model or return an error
            model_path = r'detect_app\model\random_forest_model.joblib'

  
        return render(request, 'result.html', {'prediction': prediction_text,"prediction2":prediction2})
    if request.method == 'POST' and request.POST.get('idd'):
        model_choice = request.POST.get('model')
        idd=request.POST.get('idd')
        conn = sqlite3.connect(r'C:\Users\Mrudul\Documents\PDD\detect_app\static\images\test11.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM test_data WHERE name=?", (idd,))
        row = cursor.fetchone()
        print("Data for name '{}' found:".format(idd))
        columns = ['name', 'MDVP:Fo(Hz)', 'MDVP:Fhi(Hz)', 'MDVP:Flo(Hz)', 'MDVP:Jitter(%)', 'MDVP:Jitter(Abs)', 'MDVP:RAP', 'MDVP:PPQ', 'Jitter:DDP', 'MDVP:Shimmer', 'MDVP:Shimmer(dB)', 'Shimmer:APQ3', 'Shimmer:APQ5', 'MDVP:APQ', 'Shimmer:DDA', 'NHR', 'HNR', 'RPDE', 'DFA', 'spread1', 'spread2', 'D2', 'PPE']
        df = pd.DataFrame([row], columns=columns)  # Wrap the result in a list
        #print(df)
        df=df.drop(columns=['name'])
        print(df)
        conn.close()
        if model_choice == 'knn':
            scaler=joblib.load( r'C:\Users\Mrudul\Documents\PDD\detect_app\model\scaler_model.joblib')
            model_path = r'detect_app\model\KNN_parkinsons_model.joblib'
            model = joblib.load(model_path)
           # aa=pd.read_csv(uploaded_file)
            #prediction_data = csv_file.drop(columns=['name', 'status'])
            ans=np.array([df])
            print(ans[0][0])
            new_data_point_scaled = scaler.transform(ans[0][0].reshape(1, -1))
            model_path2 = r'detect_app\model\pca_model.joblib'
            pca2=joblib.load(model_path2)
            new_data_point_pca = pca2.transform(new_data_point_scaled)
            prediction = model.predict(new_data_point_pca)
            if prediction[0] == 1:
                prediction2 = model.predict_proba(new_data_point_pca)[0,1]
                prediction2=prediction2*100
                prediction_text = "You have Parkinson's Disease."
            else:
                prediction2 = model.predict_proba(new_data_point_pca)[0,0]
                prediction2=prediction2*100
                prediction_text = "You are healthy."
        elif model_choice == 'svm':
            model_path = r'detect_app\model\svm_parkinsons_model2.joblib'
            scaler=joblib.load( r'C:\Users\Mrudul\Documents\PDD\detect_app\model\scaler_model.joblib')
            model = joblib.load(model_path)
           # prediction_data = csv_file.drop(columns=['name', 'status'])
            ans=np.array([df])
            print(ans[0][0])
            new_data_point_scaled = scaler.transform(ans[0][0].reshape(1, -1))
            prediction = model.predict(new_data_point_scaled)
            if prediction[0] == 1:
                prediction2 = model.predict_proba(new_data_point_scaled)[0,1]
                prediction2=prediction2*100
                prediction_text = "You have Parkinson's Disease."
            else:
                prediction2 = model.predict_proba(new_data_point_scaled)[0,0]
                prediction2=prediction2*100
                prediction_text = "You are healthy."
            
          
        elif model_choice == 'random_forest':
            model_path = r'detect_app\model\random_forest_model.joblib'
            model = joblib.load(model_path)
            #uploaded_file = request.FILES['file']

            # Assume 'name' and 'status' are columns you don't need for prediction
            #prediction_data = csv_file.drop(columns=['name', 'status'])
           # print(prediction_data)
            #print(type(prediction_data))
            prediction = model.predict(df)

            # Depending on your model output, adjust the following condition accordingly
            if prediction[0] == 1:  # Assuming the model returns a list of predictions
                prediction2 = model.predict_proba(df)[0,1]
                prediction2=prediction2*100
                prediction_text = "You have Parkinson's Disease."
            else:
                prediction2 = model.predict_proba(df)[0,0]
                prediction2=prediction2*100
                prediction_text = "You are healthy."

        else:
            # Default to a model or return an error
            model_path = r'detect_app\model\random_forest_model.joblib'

  
        return  JsonResponse({'prediction': prediction_text,"prediction2":prediction2})
     
    # If not a POST request, or some other issue occurs, you might redirect or show an error
    return render(request, 'home.html', {'prediction': "Invalid request or no file uploaded."})


