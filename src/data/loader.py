"""
Data Loader Module
Handles loading and reading various traffic datasets
"""

import os
import pandas as pd
from pathlib import Path
from typing import Dict, Optional, List


class DataLoader:
    """Load and manage traffic analysis datasets"""
    
    def __init__(self, data_dir: str = "data/raw"):
        self.data_dir = Path(data_dir)
        self.datasets: Dict[str, pd.DataFrame] = {}
    
    def load_accidents_by_time(self) -> pd.DataFrame:
        """
        Load traffic accidents by time of occurrence
        Columns: State/UT, accidents by 3-hour time slots (0-3, 3-6, 6-9, etc.)
        """
        file_path = self.data_dir / "Traffic_Accidents_Time" / "NCRB_ADSI_2023_Table_1A.6.csv"
        df = pd.read_csv(file_path)
        self.datasets['accidents_time'] = df
        return df
    
    def load_accidents_by_month(self) -> pd.DataFrame:
        """
        Load traffic accidents by month of occurrence
        Columns: State/UT/City, accidents by month (Jan-Dec)
        """
        file_path = self.data_dir / "Traffic_Accidents_Month" / "NCRB_ADSI_2023_Table_1A.5.csv"
        df = pd.read_csv(file_path)
        self.datasets['accidents_month'] = df
        return df
    
    def load_accidents_severity(self) -> pd.DataFrame:
        """
        Load accidents with injury/death statistics
        Columns: State/UT, Cases, Injured, Died (for Road, Railway, Total)
        """
        file_path = self.data_dir / "Accidents_Injureds_Deaths" / "NCRB_ADSI_2023_Table_1A.2.csv"
        df = pd.read_csv(file_path)
        self.datasets['accidents_severity'] = df
        return df
    
    def load_vehicle_registrations(self) -> pd.DataFrame:
        """
        Load vehicle registrations by city
        Columns: City, vehicle categories (Two Wheelers, Cars, etc.)
        """
        folder = self.data_dir / "Vehicles Registrations"
        dfs = []
        for file in folder.glob("*.csv"):
            # Try multiple encodings
            for encoding in ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']:
                try:
                    df = pd.read_csv(file, encoding=encoding)
                    dfs.append(df)
                    break
                except UnicodeDecodeError:
                    continue
        
        if dfs:
            combined = pd.concat(dfs, ignore_index=True)
            self.datasets['vehicle_registrations'] = combined
            return combined
        return pd.DataFrame()
    
    def load_road_statistics(self) -> pd.DataFrame:
        """
        Load road length statistics
        Columns: Road category, type, length by year
        """
        folder = self.data_dir / "Road Length Statistics"
        dfs = []
        for file in folder.glob("*.csv"):
            # Try multiple encodings
            for encoding in ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']:
                try:
                    df = pd.read_csv(file, encoding=encoding)
                    dfs.append(df)
                    break
                except UnicodeDecodeError:
                    continue
        
        if dfs:
            combined = pd.concat(dfs, ignore_index=True)
            self.datasets['road_statistics'] = combined
            return combined
        return pd.DataFrame()
    
    def load_all_datasets(self) -> Dict[str, pd.DataFrame]:
        """Load all available datasets"""
        print("Loading all datasets...")
        
        try:
            self.load_accidents_by_time()
            print("  ✓ Accidents by Time")
        except Exception as e:
            print(f"  ✗ Accidents by Time: {e}")
        
        try:
            self.load_accidents_by_month()
            print("  ✓ Accidents by Month")
        except Exception as e:
            print(f"  ✗ Accidents by Month: {e}")
        
        try:
            self.load_accidents_severity()
            print("  ✓ Accidents Severity")
        except Exception as e:
            print(f"  ✗ Accidents Severity: {e}")
        
        try:
            self.load_vehicle_registrations()
            print("  ✓ Vehicle Registrations")
        except Exception as e:
            print(f"  ✗ Vehicle Registrations: {e}")
        
        try:
            self.load_road_statistics()
            print("  ✓ Road Statistics")
        except Exception as e:
            print(f"  ✗ Road Statistics: {e}")
        
        print(f"\nLoaded {len(self.datasets)} datasets")
        return self.datasets
    
    def get_dataset(self, name: str) -> Optional[pd.DataFrame]:
        """Get a loaded dataset by name"""
        return self.datasets.get(name)
    
    def get_dataset_info(self) -> pd.DataFrame:
        """Get summary info for all loaded datasets"""
        info = []
        for name, df in self.datasets.items():
            info.append({
                'Dataset': name,
                'Rows': len(df),
                'Columns': len(df.columns),
                'Memory (KB)': df.memory_usage(deep=True).sum() / 1024
            })
        return pd.DataFrame(info)


# Quick test when run directly
if __name__ == "__main__":
    loader = DataLoader()
    datasets = loader.load_all_datasets()
    print("\n" + "="*50)
    print(loader.get_dataset_info())
