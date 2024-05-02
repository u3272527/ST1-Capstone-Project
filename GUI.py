import pickle
import tkinter as tk
import numpy as np
#import pandas as pd
#Make sure sklearn is installed into your system
# I used 'py -m pip install -U scikit-learn' in cmd to install it
# Also pandas with 'py -m pip install pandas'

#Paste the place you stored your pickle files here (include the r in front)
filePath = r"C:\Users\admin\Documents\UC\Capstone_Project\pickled_files\MLdata_Numeric.pkl"
MLdata_Numeric = pickle.load(open(filePath, 'rb')) 

targetVar = 'Price'
predictors = ['Engine', 'Power', 'Fuel_Type_CNG', 'Fuel_Type_Diesel', 'Fuel_Type_Electric', 'Fuel_Type_LPG', 'Fuel_Type_Petrol', 'Transmission_Automatic', 'Transmission_Manual']

x = MLdata_Numeric[predictors].values
y = MLdata_Numeric[targetVar].values

# Setup for the prediction model
from sklearn.neighbors import KNeighborsRegressor

knn = KNeighborsRegressor(n_neighbors=3)
predictionModel = knn.fit(x,y)

#Exception classes
class lackFuelType(Exception):
    pass

class lackTransmissionType(Exception):
    pass

#GUI functions
def predictPrice(eng,pow,cng,dsl,elt,lpg,ptr,auto,manu):
    predictVal = predictionModel.predict(np.c_[eng, pow, cng, dsl, elt, lpg, ptr, auto, manu])
    return(predictVal)    

def numerateFuel(inp):
    #changes the input value to 1 and the others to 0
    if inp == 'CNG':
        cng = 1
        diesel = 0
        electric = 0
        lpg = 0
        petrol = 0
    elif inp == 'Diesel':
        diesel = 1
        cng = 0
        electric = 0
        lpg = 0
        petrol = 0
    elif inp == 'Electric':
        electric = 1
        cng = 0
        diesel = 0
        lpg = 0
        petrol = 0
    elif inp == 'LPG':
        lpg = 1
        cng = 0
        diesel = 0
        electric = 0
        petrol = 0
    elif inp == 'Petrol':
        petrol = 1
        cng = 0
        diesel = 0
        electric = 0
        lpg = 0
    else:
        #raises an exeption
        raise lackFuelType()
    return cng,diesel,electric,lpg,petrol
    
def numerateTransmission(inp):
    auto = 0
    manual = 0
    if inp == 'Automatic':
        auto = 1
        manual = 0
    elif inp == 'Manual':
        manual = 1
        auto = 0
    else:
        raise lackTransmissionType()
    return auto,manual
    
def Calculate_Value():
    try:
        #Gets all the inputs 
        engine = float(engineInp.get())
        power = float(powerInp.get())
        cng,diesel,electric,lpg,petrol=numerateFuel(fuelVar.get())
        auto,manual = numerateTransmission(transVar.get())
        prediction = predictPrice(engine,power,cng,diesel,electric,lpg,petrol,auto,manual)
        #Apply numpy exponent to undo log also takes out from numpy array and rounds it
        prediction = round((np.exp(prediction))[0],4)
        print(f'Prediction Price (In Lakh): {prediction}')
        outputVar.set(prediction)
    except ValueError:
        print("Non-number values were used in engine/power")
    except lackFuelType:
        print("Missing input from fuel type")
    except lackTransmissionType:
        print('Missing input from transmission type')
    

#Setup for GUI 
root = tk.Tk()
root.title('Car price predictor')
root.geometry('300x300')

#Variable for displaying values
engineVar = tk.DoubleVar()
powerVar = tk.DoubleVar()
outputVar = tk.DoubleVar()

engineLab = tk.Label(root, height=1, width=15, text='Engine Power (CC)')
engineLab.grid(padx=1,pady=1)
engineInp = tk.Entry(root, textvariable=engineVar)
engineInp.grid(padx=1,pady=1)

powerLab = tk.Label(root, height=1, width=15, text='Power (bhp)')
powerLab.grid(padx=1,pady=1)
powerInp = tk.Entry(root, textvariable=powerVar)
powerInp.grid(padx=1,pady=1)

#Option menu things
# variable for fuel type
fuelVar = tk.StringVar(root)
fuelVar.set('Select fuel type')
fuelTypes = ['CNG', 'Diesel', 'Electric', 'LPG', 'Petrol']

#variable for transmission type
transVar = tk.StringVar(root)
transVar.set('Select transmission type')
transTypes = ['Automatic', 'Manual']

#Categorical value GUI
fuelLab = tk.Label(root, height=1, width=40, text='Fuel Type (CNG, Diesel, Electric, LPG, Petrol)')
fuelLab.grid(padx=1,pady=1)
fuelInp = tk.OptionMenu(root, fuelVar, *fuelTypes)
fuelInp.grid(padx=1,pady=1)

transLab = tk.Label(root, height=1, width=30, text='Transmission Type (Automatic, Manual)')
transLab.grid(padx=1,pady=1)
transInp = tk.OptionMenu(root, transVar, *transTypes)
transInp.grid(padx=1,pady=1)

calculationLab = tk.Label(root,height=1, width=25, text='Car price prediction (In Lakh)')
calculationLab.grid(padx=1,pady=1)
calculationDisp = tk.Label(root, height = 1, width = 15,relief="sunken",justify="left",textvariable=outputVar)
calculationDisp.grid(padx=1,pady=1)

calculateBtn = tk.Button(root,text='Calculate Price', command=Calculate_Value)
calculateBtn.grid(padx=1,pady=1)

root.mainloop()