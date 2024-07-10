import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sklearn
import datetime

from feature_engineering import Features
from labels import LabelGenerator

def x_y_split(data: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    label_cols = ['1s_change', '3s_change', '5s_change']
    feature_cols = list(set(data.columns) - set(label_cols))
    y = data[label_cols].copy()
    x = data[feature_cols].copy()

    return x, y

def main():
    prefix = "MSFT_2012-06-21_34200000_57600000"

    trades_data_file = f"./data/{prefix}_message_5.csv"
    orderbook_data_file = f"./data/{prefix}_orderbook_5.csv"

    trade_df = pd.read_csv(trades_data_file,names=(
    'timestamp',
    'type',
    'orderId',
    'size',
    'trade_price',
    'direction'
))

    orderbook_df = pd.read_csv(orderbook_data_file, names=(
        'ask_1_price',
        'ask_1_size',
        'bid_1_price',
        'bid_1_size',

        'ask_2_price',
        'ask_2_size',
        'bid_2_price',
        'bid_2_size',

        'ask_3_price',
        'ask_3_size',
        'bid_3_price',
        'bid_3_size',

        'ask_4_price',
        'ask_4_size',
        'bid_4_price',
        'bid_4_size',

        'ask_5_price',
        'ask_5_size',
        'bid_5_price',
        'bid_5_size',
    ))

    df = pd.concat([trade_df, orderbook_df], axis=1)
    # print(df.head())
    df['timestamp'] = df['timestamp'] - 34200

    print("Main | Adding Features")
    df : pd.DataFrame = Features.add_features(df)
    
    print("Main | Generating Labels")
    df = LabelGenerator.createLabels(df)
    
    x, y = x_y_split(df)
    x = Features.lag_rolling_features(x)
    
    print("Main | Saving Data")
    x.to_csv(f"./data/features_{prefix}.csv", index=False)
    y.to_csv(f"./data/labels_{prefix}.csv", index=False)
    
if __name__ == "__main__":
    main()