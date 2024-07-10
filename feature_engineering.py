import datetime
import pandas as pd

from data_types import OrderType

class Features:
    timestamp = None
    max_lag = 5
    window = [5, 10, 20]
    sec_window = [1, 3, 5]
    rolling_sum_cols = []
    rolling_mean_cols = []
    rolling_max_cols = []
    rolling_min_cols = []
    rolling_std_cols = []
    
    @staticmethod
    def bid_ask_spread(data: pd.DataFrame):
        """Generates datapoints using the best bid and ask prices.
        Spread - Calculates the spread between the best bid and ask prices.
        Midprice - Calculates the midprice between the best bid and ask prices."""
        data['spread'] = data['ask_1_price'] - data['bid_1_price']
        data['midprice'] = (data['ask_1_price'] + data['bid_1_price']) / 2
        
    @staticmethod
    def bid_ask_qty(data: pd.DataFrame):
        """Generates datapoints using the best bid and ask quantities.
        bid_ask_qty_diff - Calculates the difference between the best bid and ask quantities.
        bid_ask_qty_comb - Calculates the sum of the best bid and ask quantities.
        imbalance - Calculates the imbalance between the best bid and ask quantities."""
        data['bid_ask_qty_diff'] = data['ask_1_size'] - data['bid_1_size']
        data['bid_ask_qty_comd'] = data['ask_1_size'] + data['bid_1_size']
        data['imbalance'] = (data['bid_1_size']) / (data['ask_1_size'] + data['bid_1_size'])

    @staticmethod
    def diff_feature(data: pd.DataFrame):
        """
        Generated the differences between rows for each column in the data.
        """
        for col in set(data.columns) - {'timestamp'}:
            data[f'{col}_diff'] = data[col]

    @staticmethod
    def sum_feature(data: pd.DataFrame):
        """
        Calculates the volume traded within the last n seconds.
        """
        for window in Features.sec_window:
            data[f'sum_within_{window}s'] = data['size'].where(data['type'] == OrderType.EXECUTION_VISIBLE.value).rolling(window=pd.Timedelta(seconds=window)).sum().fillna(0)

    @staticmethod
    def calc_advance_times(data: pd.DataFrame):
        """
        Calculates the time between bid and ask price advances.
        """
        bid_price_advances = data['bid_1_price'].diff().fillna(0) > 0
        ask_price_advances = data['ask_1_price'].diff().fillna(0) < 0
        
        data['bid_advance_timetamp'] = data[bid_price_advances]['timestamp']
        data['ask_advance_timetamp'] = data[ask_price_advances]['timestamp']
        
        data['previous_bid_advance_timestamp'] = data['bid_advance_timetamp'].ffill()
        data['previous_ask_advance_timestamp'] = data['ask_advance_timetamp'].ffill()

        data['bid_advance_time'] = ((data['timestamp'] - data['previous_bid_advance_timestamp']) / datetime.timedelta(milliseconds=1)).fillna(0)
        data['ask_advance_time'] = ((data['timestamp'] - data['previous_ask_advance_timestamp']) / datetime.timedelta(milliseconds=1)).fillna(0)

        # remove bid_advance_timetamp and previous_bid_advance_timestamp
        data = data.drop(columns=['bid_advance_timetamp', 'ask_advance_timetamp', 'previous_bid_advance_timestamp', 'previous_ask_advance_timestamp'])
    
    @staticmethod
    def rolling_feature(data: pd.DataFrame, col, window: int, feature):
        """
        Windows: 
        """
        try:
            new_col = f'{col}_rolling_{feature}_{window}'
            
            rolling = data[col].rolling(window=window)

            match feature:
                case 'sum':
                    data[new_col] = rolling.sum()
                case 'mean':
                    data[new_col] = rolling.mean()
                case 'max':
                    data[new_col] = rolling.max()
                case 'min':
                    data[new_col] = rolling.min()
                case 'std':
                    data[new_col] = rolling.std()
                case _:
                    raise ValueError(f'Invalid feature {feature}')
        except ValueError as e:
            print(e)
            print(window)
        except Exception as e:
            print(e)
            print(window)
        finally:
            return
    
    @classmethod
    def lag_rolling_features(cls, data):
        """Add lag and rolling features to the data"""
        data = data.copy()
        
        cols_to_ignore = {'timestamp', 'type', 'orderId', 'direction'}
        rolling_cols = set(data.columns) - cols_to_ignore
        
        cls.rolling_sum_cols = [i for i in rolling_cols if 'diff' in i]
        cls.rolling_mean_cols = rolling_cols
        
        cls.rolling_min_cols = [i for i in rolling_cols if '_size' in i]
        cls.rolling_max_cols = [i for i in rolling_cols if '_size' in i]
        
        cls.rolling_std_cols = rolling_cols

        for col in rolling_cols: 
            for window in cls.window:
                # window = '{}m'.format(window)
                window *= 60
                
                if col in cls.rolling_sum_cols:
                    cls.rolling_feature(data, col, window, 'sum')
                if col in cls.rolling_mean_cols:
                    cls.rolling_feature(data, col, window, 'mean')
                if col in cls.rolling_max_cols:
                    cls.rolling_feature(data, col, window, 'max')
                if col in cls.rolling_min_cols:
                    cls.rolling_feature(data, col, window, 'min')
                if col in cls.rolling_std_cols:
                    cls.rolling_feature(data, col, window, 'std')
        
        data['timestamp'] = pd.to_datetime(data['timestamp'])
        data = data.set_index('timestamp')
        # data.index = cls.timestamp
        for col in rolling_cols:
            for sec_window in cls.sec_window:
                sec_window = '{}s'.format(sec_window)
                
                if col in cls.rolling_sum_cols:
                    cls.rolling_feature(data, col, sec_window, 'sum')
                if col in cls.rolling_mean_cols:
                    cls.rolling_feature(data, col, sec_window, 'mean')
                if col in cls.rolling_max_cols:
                    cls.rolling_feature(data, col, sec_window, 'max')
                if col in cls.rolling_min_cols:
                    cls.rolling_feature(data, col, sec_window, 'min')
                if col in cls.rolling_std_cols:
                    cls.rolling_feature(data, col, sec_window, 'std')
                if col in ['up_down', 'trade_price_compare', 'trade_price_pos']:
                    cls.rolling_feature(data, col, sec_window, 'mode')

        return data
    
    @classmethod
    def add_features(cls, data):
        """Add's all basic features to the dataset"""
        
        ata = data.copy()
        cls.timestamp = data['timestamp']

        cls.bid_ask_spread(data)
        cls.bid_ask_qty(data)
        # cls.diff_feature(data)
        # cls.up_or_down(data)

        return data