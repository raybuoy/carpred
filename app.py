from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    Fuel_Type_Diesel=0
    if request.method == 'POST':
        Year = int(request.form['Year'])
        
        
        Kms_Driven=int(request.form['Kms_Driven'])
        
        Kms_Driven2=np.log(Kms_Driven)
        
        Owner=int(request.form['Owner'])
        
        if(Owner==2):
            owner_Second_Owner=1
            owner_Fourth_Above_Owner=0
            owner_Third_Owner=0
            owner_Test_Drive_Car=0
            
        elif(Owner==3):
            owner_Second_Owner=0
            owner_Fourth_Above_Owner=0
            owner_Third_Owner=1
            owner_Test_Drive_Car=0
            
        elif(Owner>=4):
            owner_Second_Owner=0
            owner_Fourth_Above_Owner=1
            owner_Third_Owner=0
            owner_Test_Drive_Car=0
        
        else:
            owner_Second_Owner=0
            owner_Fourth_Above_Owner=1
            owner_Third_Owner=0
            owner_Test_Drive_Car=0
        
        Fuel_Type_Petrol=request.form['Fuel_Type_Petrol']
        
        mileage=int(request.form['mileage'])
        
        if(Fuel_Type_Petrol=='Petrol'):
            Fuel_Type_Petrol=1
            Fuel_Type_Diesel=0
            Fuel_Type_LPG=0
        elif(Fuel_Type_Petrol=='Diesel'):
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=1
            Fuel_Type_LPG=0
        elif(Fuel_Type_Petrol=='LPG'):
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=0
            Fuel_Type_LPG=1
        else:
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=0
            Fuel_Type_LPG=0
            
        Year=2020-Year
        
        Seller_Type_Individual=request.form['Seller_Type_Individual']
        if(Seller_Type_Individual=='Individual'):
            Seller_Type_Individual=1
            Seller_Type_Trustmark_Dealer=0
        else:
            Seller_Type_Individual=0
            Seller_Type_Trustmark_Dealer=1
            
        Transmission_Mannual=request.form['Transmission_Manual']
        if(Transmission_Mannual=='Manual'):
            Transmission_Mannual=1
        else:
            Transmission_Mannual=0
            
        engine=int(request.form['engine'])
        max_power=int(request.form['max_power']) 
        seats=int(request.form['seats'])       
        prediction=model.predict([[Year,Kms_Driven2,mileage,engine, max_power, seats,Fuel_Type_Diesel,Fuel_Type_LPG,Fuel_Type_Petrol,Seller_Type_Individual,Seller_Type_Trustmark_Dealer,Transmission_Mannual,owner_Fourth_Above_Owner,owner_Second_Owner,owner_Test_Drive_Car, owner_Third_Owner]])
        output=round(prediction[0],2)
        if output<0:
            return render_template('index.html',prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('index.html',prediction_text="You Can Sell The Car at {}".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)