"""
CICIDS2017 Dataset Preprocessing Module

This module handles loading, cleaning, and preprocessing of the CICIDS2017 dataset
for cybersecurity threat detection.
"""

import pandas as pd
import numpy as np
import os
import pickle
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest, mutual_info_classif
import warnings
warnings.filterwarnings('ignore')

class CICIDS2017Preprocessor:
    """Preprocessor for CICIDS2017 dataset"""
    
    def __init__(self, data_path='data/', output_path='data/processed/'):
        self.data_path = data_path
        self.output_path = output_path
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.feature_selector = None
        self.selected_features = None
        
        # Create output directory if it doesn't exist
        os.makedirs(output_path, exist_ok=True)
        
        # CICIDS2017 attack types mapping
        self.attack_types = {
            'BENIGN': 0,
            'DDoS': 1,
            'PortScan': 2,
            'Bot': 3,
            'Infiltration': 4,
            'Web Attack - Brute Force': 5,
            'Web Attack - XSS': 6,
            'Web Attack - Sql Injection': 7,
            'FTP-Patator': 8,
            'SSH-Patator': 9,
            'DoS Hulk': 10,
            'DoS GoldenEye': 11,
            'DoS slowloris': 12,
            'DoS Slowhttptest': 13,
            'Heartbleed': 14
        }
    
    def load_dataset(self, filename='CICIDS2017.csv'):
        """Load the CICIDS2017 dataset"""
        print(f"Loading dataset from {self.data_path}{filename}")
        
        try:
            # Load the dataset
            df = pd.read_csv(f"{self.data_path}{filename}", low_memory=False, encoding='latin1')
            print(f"Dataset loaded successfully. Shape: {df.shape}")
            return df
        except FileNotFoundError:
            print(f"Dataset file not found at {self.data_path}{filename}")
            print("Please run merge_CICIDS2017.py first.")
            return None
    
    def clean_data(self, df):
        """Clean the dataset by handling missing values and outliers"""
        print("Cleaning dataset...")
        
        # Strip whitespace from column names
        df.columns = df.columns.str.strip()
        
        # Remove duplicate rows
        initial_shape = df.shape
        df = df.drop_duplicates()
        print(f"Removed {initial_shape[0] - df.shape[0]} duplicate rows")
        
        # Handle missing values
        df = df.replace([np.inf, -np.inf], np.nan)
        print(f"Found {df.isnull().sum().sum()} missing or infinite values.")
        
        # Drop rows with NaN values (common strategy for this dataset)
        df = df.dropna()
        
        print(f"Dataset cleaned. Final shape: {df.shape}")
        return df
    
    def encode_categorical_features(self, df):
        """Encode categorical features"""
        print("Encoding categorical features...")
        
        # Identify categorical columns (non-numeric)
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        # The 'Label' column is our target
        if 'Label' in categorical_cols:
            categorical_cols.remove('Label')
        
        # Encode other categorical features (if any)
        for col in categorical_cols:
            if col in df.columns:
                le = LabelEncoder()
                df[col] = le.fit_transform(df[col].astype(str))
        
        # Encode target variable
        if 'Label' in df.columns:
            unique_labels = df['Label'].unique()
            print(f"Found {len(unique_labels)} unique labels.")
            
            # Create a mapping for labels
            label_mapping = {}
            for label in unique_labels:
                # Find a matching key in our attack_types
                mapped_label = self.attack_types.get(label.strip(), 0) # Default to 0 (BENIGN)
                label_mapping[label] = mapped_label
            
            df['Label'] = df['Label'].map(label_mapping)
        else:
            raise ValueError("Target column 'Label' not found.")
        
        print("Categorical features encoded successfully")
        return df
    
    def feature_selection(self, X, y, k=50):
        """Perform feature selection"""
        print(f"Performing feature selection using mutual_info_classif...")
        
        # Ensure k is not larger than the number of features
        k = min(k, X.shape[1])
        
        self.feature_selector = SelectKBest(score_func=mutual_info_classif, k=k)
        
        X_selected = self.feature_selector.fit_transform(X, y)
        self.selected_features = self.feature_selector.get_support(indices=True)
        
        print(f"Selected {len(self.selected_features)} features out of {X.shape[1]}")
        return X_selected
    
    def normalize_features(self, X, fit_scaler=True):
        """Normalize features using StandardScaler"""
        print("Normalizing features...")
        
        if fit_scaler:
            X_scaled = self.scaler.fit_transform(X)
        else:
            X_scaled = self.scaler.transform(X)
        
        print("Features normalized successfully")
        return X_scaled
    
    def preprocess_pipeline(self, filename='CICIDS2017.csv', feature_selection_k=50):
        """Complete preprocessing pipeline"""
        print("Starting CICIDS2017 preprocessing pipeline...")
        
        df = self.load_dataset(filename)
        if df is None:
            return None
        
        df = self.clean_data(df)
        df = self.encode_categorical_features(df)
        
        X = df.drop('Label', axis=1)
        y = df['Label']
        
        # Ensure all X data is numeric before selection
        X = X.apply(pd.to_numeric, errors='coerce').fillna(0)
        
        X_selected = self.feature_selection(X, y, k=feature_selection_k)
        
        X_scaled = self.normalize_features(X_selected, fit_scaler=True)
        
        X_train, X_test, y_train, y_test = self.split_data(
            X_scaled, y, test_size=0.2
        )
        
        processed_data = {
            'X_train': X_train,
            'X_test': X_test,
            'y_train': y_train,
            'y_test': y_test,
            'feature_names': X.columns[self.selected_features].tolist(),
            'attack_types': self.attack_types,
            'scaler': self.scaler,
            'feature_selector': self.feature_selector
        }
        
        with open(f"{self.output_path}processed_data.pkl", 'wb') as f:
            pickle.dump(processed_data, f)
        
        print(f"Preprocessing completed. Data saved to {self.output_path}")
        return processed_data

    def split_data(self, X, y, test_size=0.2, random_state=42):
        """Split data into train and test sets"""
        print("Splitting data into train and test sets...")
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        print(f"Data split completed:")
        print(f"  Training set: {X_train.shape[0]} samples")
        print(f"  Test set: {X_test.shape[0]} samples")
        
        return X_train, X_test, y_train, y_test

    # --- THIS IS THE MISSING FUNCTION ---
    def load_processed_data(self):
        """Load previously processed data"""
        try:
            with open(f"{self.output_path}processed_data.pkl", 'rb') as f:
                processed_data = pickle.load(f)
            print("Processed data loaded successfully")
            return processed_data
        except FileNotFoundError:
            print("Processed data not found. Please run preprocessing first.")
            return None

def main():
    """Main function to run preprocessing"""
    preprocessor = CICIDS2017Preprocessor()
    
    # We will force it to re-run to avoid any errors.
    # Delete the old file if it exists.
    processed_file_path = "data/processed/processed_data.pkl"
    if os.path.exists(processed_file_path):
        print("Found old processed data. Deleting it to create a new one...")
        os.remove(processed_file_path)
    
    print("Running preprocessing pipeline...")
    processed_data = preprocessor.preprocess_pipeline()
    
    if processed_data:
        print("\nPreprocessing Summary:")
        print(f"Training samples: {processed_data['X_train'].shape[0]}")
        print(f"Test samples: {processed_data['X_test'].shape[0]}")
        print(f"Number of features: {processed_data['X_train'].shape[1]}")
        print(f"Number of attack types: {len(processed_data['attack_types'])}")

if __name__ == "__main__":
    main()