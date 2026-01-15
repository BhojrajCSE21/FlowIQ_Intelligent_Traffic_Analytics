"""
Data Preprocessor Module
Handles data cleaning, transformation, and feature engineering
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple, List, Optional


class DataPreprocessor:
    """Clean and transform traffic datasets for analysis"""
    
    def __init__(self):
        self.processed_datasets: Dict[str, pd.DataFrame] = {}
    
    def clean_accidents_by_time(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and transform accidents by time dataset
        - Extracts time slot columns
        - Creates long format for analysis
        """
        df = df.copy()
        
        # Drop serial number column if exists
        if 'Sl. No.' in df.columns:
            df = df.drop(columns=['Sl. No.'])
        
        # Identify state column
        state_col = [c for c in df.columns if 'State' in c or 'UT' in c][0]
        df = df.rename(columns={state_col: 'State'})
        
        # Extract road accident time columns (focus on road accidents)
        time_cols = [c for c in df.columns if 'Road Accidents -' in c and 'hrs' in c]
        
        # Create mapping for time slots
        time_mapping = {
            '0000 hrs': '00:00-03:00',
            '0300 hrs to 0600 hrs': '03:00-06:00',
            '0600 hrs to 0900 hrs': '06:00-09:00',
            '0900 hrs to 1200 hrs': '09:00-12:00',
            '1200 hrs to 1500 hrs': '12:00-15:00',
            '1500 hrs to 1800 hrs': '15:00-18:00',
            '1800 hrs to 2100': '18:00-21:00',
            '2100 hrs. to 2400': '21:00-24:00'
        }
        
        # Create long format
        records = []
        for _, row in df.iterrows():
            state = row['State']
            for col in time_cols:
                if 'Total' not in col:
                    # Extract time slot from column name
                    for key, time_slot in time_mapping.items():
                        if key in col:
                            records.append({
                                'State': state,
                                'TimeSlot': time_slot,
                                'Accidents': row[col]
                            })
                            break
        
        result = pd.DataFrame(records)
        result['Accidents'] = pd.to_numeric(result['Accidents'], errors='coerce').fillna(0).astype(int)
        
        self.processed_datasets['accidents_time'] = result
        return result
    
    def clean_accidents_by_month(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and transform accidents by month dataset
        - Creates long format with State, Month, Accidents
        """
        df = df.copy()
        
        # Drop serial number column if exists
        if 'Sl. No.' in df.columns:
            df = df.drop(columns=['Sl. No.'])
        
        # Identify state column
        state_col = [c for c in df.columns if 'State' in c or 'UT' in c or 'City' in c][0]
        df = df.rename(columns={state_col: 'State'})
        
        # Extract road accident month columns
        months = ['January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December']
        
        month_cols = [c for c in df.columns if any(m in c for m in months) and 'Road Accidents' in c]
        
        # Create long format
        records = []
        for _, row in df.iterrows():
            state = row['State']
            for month in months:
                col = f'Road Accidents - {month}'
                if col in df.columns:
                    records.append({
                        'State': state,
                        'Month': month,
                        'MonthNum': months.index(month) + 1,
                        'Accidents': row[col]
                    })
        
        result = pd.DataFrame(records)
        result['Accidents'] = pd.to_numeric(result['Accidents'], errors='coerce').fillna(0).astype(int)
        
        self.processed_datasets['accidents_month'] = result
        return result
    
    def clean_accidents_severity(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean accidents severity dataset
        - Extracts cases, injured, died statistics
        """
        df = df.copy()
        
        # Drop serial number column if exists
        if 'Sl. No.' in df.columns:
            df = df.drop(columns=['Sl. No.'])
        
        # Identify state column
        state_col = [c for c in df.columns if 'State' in c or 'Ut' in c][0]
        df = df.rename(columns={state_col: 'State'})
        
        # Select relevant columns for total traffic accidents
        result = df[['State']].copy()
        
        # Add total traffic accident columns
        for col in df.columns:
            if 'Total Traffic Accidents' in col:
                new_col = col.replace('Total Traffic Accidents - ', '')
                result[new_col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
        
        # Calculate fatality rate
        if 'Cases' in result.columns and 'Died' in result.columns:
            result['FatalityRate'] = (result['Died'] / result['Cases'] * 100).round(2)
        
        # Calculate injury rate
        if 'Cases' in result.columns and 'Injured' in result.columns:
            result['InjuryRate'] = (result['Injured'] / result['Cases'] * 100).round(2)
        
        self.processed_datasets['accidents_severity'] = result
        return result
    
    def clean_vehicle_registrations(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean vehicle registrations dataset
        - Handles comma-formatted numbers
        - Calculates vehicle density metrics
        """
        df = df.copy()
        
        # Identify city column
        city_col = [c for c in df.columns if 'Cit' in c or 'cit' in c][0]
        df = df.rename(columns={city_col: 'City'})
        
        # Clean numeric columns (remove commas, handle special chars)
        numeric_cols = [c for c in df.columns if c != 'City']
        for col in numeric_cols:
            df[col] = df[col].astype(str).str.replace(',', '').str.replace('^', '0').str.replace('-', '0')
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
        
        # Calculate total two wheelers
        two_wheeler_cols = [c for c in numeric_cols if 'Two Wheeler' in c or 'Scooter' in c or 
                           'Moped' in c or 'Motor Cycle' in c]
        if two_wheeler_cols:
            df['TotalTwoWheelers'] = df[two_wheeler_cols].sum(axis=1)
        
        # Calculate four wheelers (cars + jeeps)
        if 'Cars' in df.columns and 'Jeeps' in df.columns:
            df['TotalFourWheelers'] = df['Cars'] + df['Jeeps']
        
        self.processed_datasets['vehicle_registrations'] = df
        return df
    
    def process_all(self, datasets: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
        """Process all datasets"""
        print("Processing datasets...")
        
        if 'accidents_time' in datasets:
            self.clean_accidents_by_time(datasets['accidents_time'])
            print("  ✓ Accidents by Time")
        
        if 'accidents_month' in datasets:
            self.clean_accidents_by_month(datasets['accidents_month'])
            print("  ✓ Accidents by Month")
        
        if 'accidents_severity' in datasets:
            self.clean_accidents_severity(datasets['accidents_severity'])
            print("  ✓ Accidents Severity")
        
        if 'vehicle_registrations' in datasets:
            self.clean_vehicle_registrations(datasets['vehicle_registrations'])
            print("  ✓ Vehicle Registrations")
        
        print(f"\nProcessed {len(self.processed_datasets)} datasets")
        return self.processed_datasets
    
    def save_processed_data(self, output_dir: str = "data/processed") -> None:
        """Save processed datasets to CSV"""
        from pathlib import Path
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        for name, df in self.processed_datasets.items():
            file_path = output_path / f"{name}_processed.csv"
            df.to_csv(file_path, index=False)
            print(f"Saved: {file_path}")
    
    def get_summary_statistics(self) -> pd.DataFrame:
        """Generate summary statistics for processed data"""
        stats = []
        for name, df in self.processed_datasets.items():
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                stats.append({
                    'Dataset': name,
                    'Column': col,
                    'Min': df[col].min(),
                    'Max': df[col].max(),
                    'Mean': df[col].mean(),
                    'Median': df[col].median(),
                    'Std': df[col].std()
                })
        return pd.DataFrame(stats)


# Quick test when run directly
if __name__ == "__main__":
    from loader import DataLoader
    
    loader = DataLoader()
    datasets = loader.load_all_datasets()
    
    preprocessor = DataPreprocessor()
    processed = preprocessor.process_all(datasets)
    
    print("\n" + "="*50)
    print("Summary Statistics:")
    print(preprocessor.get_summary_statistics())
    
    # Save processed data
    preprocessor.save_processed_data()
