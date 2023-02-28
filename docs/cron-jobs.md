# Cron Jobs 

Some brief notes on how the cron jobs work. 

- Cron jobs need to be run in order initially but then later can be run out of order 
- Pools 
  - Initially we need to pull the pools and store them in a table - [pool_lists](pool_lists.py)
  - Then we want to calculate the prices currently, after 24h, 7d, 30d. 
    - Additionally volumes are filled in at this cron but this requires other data from swaps to be fully filled for this calc to take place. [pool_prices](pool_prices.py)
  - Last we calculate a time series of all the pool prices over time in [pool_series](pool_series.py). This again requires swap data [](contracts/dex_swaps.py)
- Tokens
  - Then we need to get all the tokens in [token_lists](token_lists.py). We do this by pulling data from the lists stored in github and also filling in any pools that we get from the `getPoolStats` dex method
    - TODO: When tons of pools are added, we'll need to put in a stop gap that will prevent too many pools being indexed here. 
  - Token price summaries are then calculated (24h, 7d, 30d) which again requires [pool_prices](pool_prices.py) to be run. [token_price](token_price.py)
  - We then calculate a time series of the prices for tokens which requires [pool_series](pool_series.py) to have some data otherwise it will only sync up to the last point. 

### Token Prices 

Current Algo 
- Algo needs to be generic so that it can calculate the price for both Token table and time series tables. 
- Starting with one known price (ICX) as the root address, find the weighted shortest path to the target token. We also need to feed it a known price which is generally ICX and is seeded off the band contract. 
  - Pool history started off without pool 1 (sICX/ICX) so in this case we use the algo with a different `root_address` which is from pool 2, sICX/bnUSD using sICX and it's associated price based on bnUSD which is assumed to be 1 dollar
- Iterate through that path to find the price of the next token till you get to the end 

TODO: 
- Find several paths instead of just one 
- Algo would need to output each path along with its distance 
