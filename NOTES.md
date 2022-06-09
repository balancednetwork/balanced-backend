

## RPC Value Series 

- There are many situations where we want to see the result of an RPC call over time 
  - bnusd -> totalSupply
  - loans -> getTotalCollateral
  - contract X -> method y 

- Instead of creating a bespoke implementation of each RPC call, would be better if we could simply give the:
  1. time to start the time series (ie contract initialization date)
  2. method
  3. address 
  - And the rest of the chart is filled in

- We can now do that for each contract and produce the time series 
  - Build a list of dicts that we iterate over to produce the table
  
- Differences between v1 backend 
  - Much more performant queries -> Old backend returned ~330k records before building charts 
    - Can run this on tiny instance vs old version 
    - Only deliver results -> API doesn't crunch any numbers, just delivers pre-fetched values 
    - 90% less code 
    - Update contracts / targets by simply populating a dict 
    - Run on testnets easily 
      - Only need to swap out contract addresses 
    - Usable by community as reference implementation 

TTD: 
- Make a single table and API to expose the data 
  - Index on the identifier for the method / contract 
  - [ ] Get approval of plan then implment 

- Endpoints
  - /historical?contract_name=bnusd&method=totalSupply 
    - Defaults to entire time series 
  - /historical?contract_name=bnusd&method=totalSupply&days_ago=1 
    - Gets yesterday's method value 
    - Replace ?
      - https://balanced.sudoblock.io/api/v1/stats/dex-pool-stats-24h
      - https://balanced.sudoblock.io/api/v1/stats/dividends-fees
      - https://balanced.sudoblock.io/api/v1/stats/collateral-chart?start_timestamp=1619398800000000&end_timestamp=1654770458627000&time_interval=86400000000
      - These seem like they need stream processing 
      - https://balanced.sudoblock.io/api/v1/stats/token-stats
  - /historical?contract_name=bnusd&method=totalSupply&start_timestamp=16xxxxxxxxxx&end_time=165xxx
    - Get time series between start and end timestamps

- Stats page 
  - Change out solidwallet for api.icon.community
  - Change API from .foundation to .community
    - https://tracker.icon.foundation/v3/token/holders?contractAddr=cx88fd7df7ddff82f7cc735c871dc519838cb235bb
    - https://tracker.v2.mainnet.sng.vultr.icon.community/api/v1/transactions/token-holders/token-contract/cx88fd7df7ddff82f7cc735c871dc519838cb235bb
  - Token stats endpoints?
    - https://balanced.sudoblock.io/api/v1/stats/token-stats
  - Stats 
    - https://balanced.sudoblock.io/api/v1/dex/stats/10
