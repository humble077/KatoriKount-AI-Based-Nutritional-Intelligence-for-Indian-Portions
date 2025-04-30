import pandas as pd
from typing import List, Dict, Any

class NutritionData:
    def __init__(self, data: List[List[Any]]):
        self.data = data
        self.df = self._create_dataframe()
        
    def _create_dataframe(self) -> pd.DataFrame:
        """Convert raw data to pandas DataFrame."""
        if not self.data:
            return pd.DataFrame()
            
        headers = self.data[0]
        rows = self.data[1:]
        return pd.DataFrame(rows, columns=headers)
        
    def get_summary(self) -> Dict[str, float]:
        """Get nutritional summary statistics."""
        if self.df.empty:
            return {}
            
        numeric_columns = self.df.select_dtypes(include=['float64', 'int64']).columns
        return self.df[numeric_columns].mean().to_dict()
        
    def filter_by_date(self, start_date: str, end_date: str) -> pd.DataFrame:
        """Filter data by date range."""
        if self.df.empty:
            return pd.DataFrame()
            
        if 'Date' in self.df.columns:
            self.df['Date'] = pd.to_datetime(self.df['Date'])
            mask = (self.df['Date'] >= start_date) & (self.df['Date'] <= end_date)
            return self.df.loc[mask]
        return self.df
        
    def get_unique_categories(self) -> List[str]:
        """Get unique categories from the data."""
        if self.df.empty:
            return []
            
        if 'Category' in self.df.columns:
            return self.df['Category'].unique().tolist()
        return [] 