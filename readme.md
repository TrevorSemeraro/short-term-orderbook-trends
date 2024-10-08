# Idea

Create a neural network using random forest regression to predict directionality, and magnitude of short term orderbook movements.

# Results

Achieved an R^2 value of 0.5240, signifying strong enough predictive capabilities.

## Base Data

| Key         | Type   | Description                      |
|-------------|--------|----------------------------------|
| timestamp   | number | unix timestamp                   |
| bid_1_size  | number | Size of bid orders at depth=1    |
| ask_1_size  | number | Size of ask orders at depth=1    |
| bid_2_size  | number | Size of bid orders at depth=2    |
| ask_2_size  | number | Size of ask orders at depth=2    |
| bid_n_size  | number | Size of bid orders at depth <= n |
| ask_n_size  | number | Size of ask orders at depth <= n |
| trade_price | number | last traded price                |

## Feature Columns

| midprice        | number | midprice of asset              |
| imbalance        | number | imbalance btw. top order levels             |
| sum_trade_1s     | number | sum of quantity traded over the last second |
| sum_trade_5s     | number | sum of quantity traded over the last second |
| sum_trade_10s    | number | sum of quantity traded over the last second |
| bid_advance_time | number | seconds since bid price last increased      |
| ask_advance_time | number | seconds since ask price last decreased      |

Imbalance: Qb / (Qb + Qa)

## Labels - to be implemented

| Key       | Type  | Description                  |
|-----------|-------|------------------------------|
| 1s_change | float | Change in midprice after 1s. |
| 3s_change | float | Change in midprice after 3s. |
| 5s_change | float | Change in midprice after 5s. |

# References

https://arxiv.org/pdf/1901.10534
https://github.com/hzjken/HFT-price-prediction
https://www.ma.imperial.ac.uk/~ajacquie/Gatheral60/Slides/Gatheral60%20-%20Stoikov.pdf

# Data

https://lobsterdata.com/info/DataSamples.php