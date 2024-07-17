import numpy as np
import pandas as pd

from feature_engineering import Features

class LabelGenerator:
    """
    # Label Generation
    
    Implementation: 
    Get current rows timestamp. For each timestamp we want to find to approx., 
    calculate x seconds away from current timestamp, use the price of the first 
    of the two rows that span this timestamp.
    """
    hot_cache = {}
    
    @classmethod
    def generateLabel(cls, current_midprice: int, future_price: int) -> int:
        return future_price - current_midprice
        # if(future_price > current_midprice):
        #     return 1
        # elif(future_price < current_midprice):
        #     return -1
        # else:
        #     return 0
    
    @staticmethod
    def create_timestamp_label(df: pd.DataFrame, offset_seconds: int, average_rows_per_second:int):
        values = np.zeros(len(df))

        current_midprice = 0

        current_index = 0
        midpoint_index = 0
        future_guess_index = 0

        timestamps = df['timestamp'].astype(np.int64).values

        for row_index in range(df.shape[0]):
            row = df.iloc[row_index]        
            current_midprice = row["midprice"]
            current_timestamp = row['timestamp'].astype(np.int64)
            goal_timestamp = current_timestamp + offset_seconds
            
            if goal_timestamp in LabelGenerator.hot_cache:
                values[row_index] = LabelGenerator.generateLabel(current_midprice, LabelGenerator.hot_cache[goal_timestamp])
                continue
            
            current_index = row_index
            future_guess_index = row_index + average_rows_per_second
            
            while future_guess_index < len(timestamps) - 1 and timestamps[future_guess_index] < goal_timestamp:
                current_index += average_rows_per_second
                future_guess_index += average_rows_per_second
            
            current_index = min(current_index, len(df) - average_rows_per_second)
            future_guess_index = min(future_guess_index, len(df) - 1)
            
            midpoint_index = (current_index + future_guess_index) // 2
            
            # binary search algorithm between the current index and the maximum index found in step prior
            while timestamps[midpoint_index] != goal_timestamp:
                
                if(future_guess_index - current_index <= 1):
                    break
                
                if timestamps[midpoint_index] < goal_timestamp:
                    current_index = midpoint_index
                else:
                    future_guess_index = midpoint_index
                
                midpoint_index = (current_index + future_guess_index) // 2
            
            values[row_index] = LabelGenerator.generateLabel(current_midprice, df.iloc[midpoint_index]['midprice'])
            LabelGenerator.hot_cache[goal_timestamp] = df.iloc[midpoint_index]['midprice']
            
            row_index += 1

        return values

    @staticmethod
    def createLabels(data : pd.DataFrame, average_rows_per_second: int=250):
        for window in Features.sec_window:
            print(f"LabelGenerator | Creating labels for {window}s")
            data[f'{window}s_change'] = LabelGenerator.create_timestamp_label(data, window, int(average_rows_per_second))        
        return data