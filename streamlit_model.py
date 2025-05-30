import pandas as pd
import streamlit as st
import os
import numpy as np
import joblib
import pickle


def load_saved_models(model_dir='saved_models'):
    """Load all saved models and return them as a dictionary"""
    models = {}
    
    # Load individual models
    models['endpoint_type'] = joblib.load(os.path.join(model_dir, 'endpoint_type_model.pkl'))
    models['endpoint_val'] = joblib.load(os.path.join(model_dir, 'endpoint_val_model.pkl'))
    models['endpoint_units'] = joblib.load(os.path.join(model_dir, 'endpoint_units_model.pkl'))
    
    # Load encoders and scaler
    models['endpoint_encoder'] = joblib.load(os.path.join(model_dir, 'endpoint_encoder.pkl'))
    models['units_encoder'] = joblib.load(os.path.join(model_dir, 'units_encoder.pkl'))
    models['scaler'] = joblib.load(os.path.join(model_dir, 'scaler.pkl'))
    
    # Load metadata
    with open(os.path.join(model_dir, 'model_metadata.pkl'), 'rb') as f:
        metadata = pickle.load(f)
    
    models['metadata'] = metadata
    return models


def predict_with_loaded_models(models, input_data):
    """Make predictions using loaded models"""
    data = input_data.copy()
    
    # Step 1: Predict endpoint type
    X1 = data[models['metadata']['feature_columns']['model1']]
    endpoint_type_encoded = models['endpoint_type'].predict(X1)[0]
    endpoint_type = models['endpoint_encoder'].inverse_transform([endpoint_type_encoded])[0]
    
    # Add encoded endpoint type for subsequent models
    data['endpoint_type_encoded'] = endpoint_type_encoded
    
    # Step 2: Predict endpoint value
    X2 = data[models['metadata']['feature_columns']['model2']]
    endpoint_values = models['endpoint_val'].predict(X2)
    log_value = endpoint_values[0][0]
    direct_value = endpoint_values[0][1]
    
    # Step 3: Predict units
    X3 = data[models['metadata']['feature_columns']['model3']]
    units_encoded = models['endpoint_units'].predict(X3)[0]
    units = models['units_encoder'].inverse_transform([units_encoded])[0]
    
    return {
        'endpoint_type': endpoint_type,
        'endpoint_value_log': log_value,
        'endpoint_value_direct': direct_value,
        'endpoint_units': units,
        'endpoint_value_from_log': np.exp(log_value)
    }


# Set page config
st.set_page_config(
    page_title="Toxicity Prediction App",
    page_icon="🧪",
    layout="wide"
)

@st.cache_resource
def load_trained_models():
    """Load the trained models (cached for performance)"""
    try:
        models = load_saved_models('saved_models')
        return models, None
    except Exception as e:
        return None, str(e)

def prepare_input_data(user_inputs, feature_columns):
    """Prepare user input data to match training data format"""
    data = pd.DataFrame(index=[0])
    
    # Fill in user inputs
    for key, value in user_inputs.items():
        data[key] = value
    
    # Get all unique feature names from all models
    all_features = set()
    for model_features in feature_columns.values():
        all_features.update(model_features)
    
    # Add missing columns with default values
    for col in all_features:
        if col not in data.columns:
            data[col] = 0
    
    # Set the appropriate dummy variables to 1
    technique = user_inputs.get('Tox Exposure Technique', 'other')
    technique_col = f'technique_{technique}'
    if technique_col in data.columns:
        data[technique_col] = 1
    
    life_stage = user_inputs.get('Life Cycle Stage', 'adult')
    stage_col = f'stage_{life_stage}'
    if stage_col in data.columns:
        data[stage_col] = 1
    
    selected_class = user_inputs.get('class', '')
    class_col = f'class_{selected_class}'
    if class_col in data.columns:
        data[class_col] = 1
        
    selected_order = user_inputs.get('order', '')
    order_col = f'order_{selected_order}'
    if order_col in data.columns:
        data[order_col] = 1
    
    # Calculate derived features
    data['Lipinski_Violations'] = (
        (data['MolecularWeight'] > 500).astype(int) +
        (data['XLogP'] > 5).astype(int) +
        (data['HBondDonorCount'] > 5).astype(int) +
        (data['HBondAcceptorCount'] > 10).astype(int)
    )
    data['Total_HBonds'] = data['HBondDonorCount'] + data['HBondAcceptorCount']
    data['MW_XLogP'] = data['MolecularWeight'] * data['XLogP']
    data['TPSA_HBonds'] = data['TPSA'] * data['Total_HBonds']
    
    return data

def main():
    models, error = load_trained_models()

    #Get Chemical Data
    chem_data = pd.read_csv('Data/ChemicalData.csv')
    chemicals = chem_data['ChemicalName'].tolist()
    chem_option = st.selectbox(
        "Choose Chemical",
        chemicals,
        index=0,
        placeholder="Chemical",
    )
    chemical = chem_data[chem_data['ChemicalName'] == chem_option]
    molecular_weight = chemical['MolecularWeight'].iloc[0]
    xlogp = chemical['XLogP'].iloc[0]
    tpsa = chemical['TPSA'].iloc[0]
    hbonddonorcount = chemical['HBondDonorCount'].iloc[0]
    hbondacceptorcount = chemical['HBondAcceptorCount'].iloc[0]

    #Get Animal Data
    animal_data = pd.read_csv('Data/PhylogeneticTreeData.csv')
    animals = animal_data['species'].tolist()
    animal_option = st.selectbox(
        "Choose animal",
        animals,
        index=0,
        placeholder="Animal"
    )
    animal = animal_data[animal_data['species'] == animal_option]
    animal_class = animal['class'].iloc[0]
    animal_order = animal['order'].iloc[0]
    print(animal_class, animal_order)

    #Get Exposure Data
    exposure_duration = st.number_input(
        "Tox Exposure Duration (days)", 
        min_value=0.1, 
        value=1.0, 
        step=0.1
    )

    #Get Exposure Technique
    exposure_technique = st.selectbox(
        "Tox Exposure Technique", 
        options=['diet', 'waterborne', 'oral', 'other']
    )

    #Get Life Cycle Stage
    life_stage = st.selectbox(
        "Life Cycle Stage",
        options=['adult', 'juvenile', 'embryo', 'larval', 'other']
    )

    user_inputs = {
            'MolecularWeight': molecular_weight,
            'XLogP': xlogp,
            'TPSA': tpsa,
            'HBondDonorCount': hbonddonorcount,
            'HBondAcceptorCount': hbondacceptorcount,
            'Tox Exposure Duration': exposure_duration,
            'Tox Exposure Technique': exposure_technique,
            'Life Cycle Stage': life_stage,
            'class': animal_class,
            'order': animal_order
    }
    
    if st.button("🔮 Predict Toxicity", type="primary"):

        feature_columns = models['metadata'].get('feature_columns')
        if feature_columns is None:
            st.error("❌ Feature columns missing!")
            return
            
        # Convert user_inputs to DataFrame with all required features
        input_data = prepare_input_data(user_inputs, feature_columns)
        molecular_features = ['MolecularWeight', 'XLogP', 'TPSA', 'MW_XLogP', 'TPSA_HBonds']
        input_data[molecular_features] = models['scaler'].transform(input_data[molecular_features])
            
        # Make prediction
        predictions = predict_with_loaded_models(models, input_data)
        st.write(predictions)


if __name__ == "__main__":
    main()

