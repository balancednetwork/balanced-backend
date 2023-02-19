# Migration 

This document overviews all the steps needed to sunset the [balanced-geometry-backend](https://github.com/balancednetwork/balanced-geometry-backend) repo. 

[Existing OpenAPI](https://balanced.sudoblock.io/api/v1/docs)

## In Use Endpoints 

### `dex/stats/<pool-id>`

This is just the `getPoolStats` method -> no need to do anything 

```text
{
  "base": "0x1f7330d21611908f4e4d0",
  "base_decimals": "0x12",
  "base_token": "cxf61cd5a45dc9f91c15aa65831a30a90d59a09619",
  "min_quote": "0x77b1d62b8b840f15",
  "name": "BALN/sICX",
  "price": "0x81f6f1664765b58",
  "quote": "0x12686e6a4e1f5942fc0db",
  "quote_decimals": "0x12",
  "quote_token": "cx2609b924e33ef00b648a409245c7ea394c467824",
  "total_supply": "0x170700cf0f0eb0852dc89"
}
```

- Replaced by `/pools`

### `stats/token-stats`

```json
{
  "tokens": {
    "CFT": {
      "symbol": "CFT",
      "holders": -1,
      "total_supply": "0x6f13b3626d4f8a79600000",
      "price": "0x10ebc254057e04",
      "name": "Craft",
      "price_change": -19.104967698704748
    },
    ... Including community pools 
  },
  "timestamp": 1674651094
}
```

- Replaced by `/tokens`

**New format**

```json
[
  {
    "symbol": "CFT",
    "holders": -1, - from tracker 
    "total_supply": "0x6f13b3626d4f8a79600000", - from RPC 
    "price": "0x10ebc254057e04",  - From token pool prices 
    "name": "Craft",  - same 
    "price_change": -19.104967698704748  - same 
  },
  {"... Including community pools ":  ""},  
]
```

Q: Is price change 24 hour?


### `stats/dex-pool-stats-24h` + `stats/dex-pool-stats-30d`

```json
{
  "0x2": {
    "volume": {
      "cx88fd7df7ddff82f7cc735c871dc519838cb235bb": "0x10d8b3bd2715b3ac74b0",
      "cx2609b924e33ef00b648a409245c7ea394c467824": "0x65deb789ad3fe0a7d5e8"
    },
    "fees": {
      "cx88fd7df7ddff82f7cc735c871dc519838cb235bb": {
        "lp_fees": "0x67813de237d11cb4d",
        "baln_fees": "0x67813de237d11cb4d"
      },
      "cx2609b924e33ef00b648a409245c7ea394c467824": {
        "lp_fees": "0x271e3a30c5998d901f",
        "baln_fees": "0x271e3a30c5998d901f"
      }
    }
  },
  ....
}
```

**New format**

```json
[
  {
    "pool_id": 2,
    "base_address": "cx...",
    "quote_address": "cx...",
    "base_lp_fees": "",
    "quote_lp_fees": "",
    "base_baln_fees": "",
    "quote_baln_fees": "",
    "base_volume": "",
    "quote_volume": ""
  }
]
```

Q: Why are the baln fees different for the base and quote?


#### API Solution 

**Volume**

- Loop through pools in cron  
- Run appropriate summary on each pool 
  - Get all token transfers between a period
```sql
select sum(metric) where pool_id = 2 and timestam > x and timestam > y
```

#### Stream Processor Solution 

- Create table with all the Txs to the dex 
  - Methods to filter on 
    - add
    - remove 
- Fields 
  - Base token 
  - Base value 
    - Hex + float 
  - Quote token 
  - Quote value
    - Hex + float 
  - Pool ID 
    - This will need to be brought into memory and then when a pair is not known, refresh list 

#### DB Solution

- This is non-ideal as then we can't run this independently and will need to tunnel to test 

### `stats/dividends-fees`

```json
{
  "cx88fd7df7ddff82f7cc735c871dc519838cb235bb": {
    "total": "0x24911dcf10b7c0e8de595",
    "hx0000000000000000000000000000000000000000": "0x10cb472c1d4121c95e80f",
    "cxa0af3165c08318e988cb30993b3048335b94af6c": "0x63515c843cb4c7edd302",
    "cx13f08df7106ae462c8358066e6d47bb68d995b6d": "0x6ccf9031189c0b729575",
    "cx5faae53c4dbd1fbe4a2eb4aab6565030f10da5c6": "0x6c3c7d79e2191e97950f"
  },
  "cx2609b924e33ef00b648a409245c7ea394c467824": {
    "total": "0x1287d49d0af14553aa836",
    "cxa0af3165c08318e988cb30993b3048335b94af6c": "0x89b4f51a466d25ce82b2",
    "cx13f08df7106ae462c8358066e6d47bb68d995b6d": "0xfb927670272b8d4b3a8",
    "cx5faae53c4dbd1fbe4a2eb4aab6565030f10da5c6": "0x8f0f2d4f6634769771dc"
  },
  "cxf61cd5a45dc9f91c15aa65831a30a90d59a09619": {
    "total": "0x3f40c185e782f03b40ad",
    "cxa0af3165c08318e988cb30993b3048335b94af6c": "0xa9cd49734da3c5917fa",
    "cx13f08df7106ae462c8358066e6d47bb68d995b6d": "0x56d9e72004135014fa",
    "cx5faae53c4dbd1fbe4a2eb4aab6565030f10da5c6": "0x15439df85e239d7813bf",
    "cx21e94c08c03daee80c25d8ee3ea22a20786ec231": "0x1f09750f34810319fffa"
  },
  "cxae3034235540b924dfcc1b45836c293dcc82bfb7": {
    "total": "0x11b0c9e395",
    "cxa0af3165c08318e988cb30993b3048335b94af6c": "0x11b0c9e395"
  },
  "cx1a29259a59f463a67bb2ef84398b30ca56b5830a": {
    "total": "0x16555a386c974f49c176",
    "cxa0af3165c08318e988cb30993b3048335b94af6c": "0x16555a386c974f49c176"
  },
  "cxbb2871f468a3008f80b08fdde5b8b951583acf06": {
    "total": "0x7da703feface679cb73",
    "cxa0af3165c08318e988cb30993b3048335b94af6c": "0x7da703feface679cb73"
  },
  "cx2e6d0fc0eca04965d06038c8406093337f085fcf": {
    "total": "0x6369c4487aa8ba89fcf",
    "cxa0af3165c08318e988cb30993b3048335b94af6c": "0x6369c4487aa8ba89fcf"
  },
  "cx369a5f4ce4f4648dfc96ba0c8229be0693b4eca2": {
    "total": "0x2b7eed1db8b9549eeb94",
    "cxa0af3165c08318e988cb30993b3048335b94af6c": "0x2b7eed1db8b9549eeb94"
  },
  "cx3a36ea1f6b9aa3d2dd9cb68e8987bcc3aabaaa88": {
    "total": "0x2bc6b771",
    "cxa0af3165c08318e988cb30993b3048335b94af6c": "0x2bc6b771"
  }
}
```

- Token as key 
- Value contracts 
  - dex 
  - ? -> https://tracker.icon.community/contract/cx13f08df7106ae462c8358066e6d47bb68d995b6d#transactions
    - 6 txs 
  - Balanced fee handler -> https://tracker.icon.community/contract/cx5faae53c4dbd1fbe4a2eb4aab6565030f10da5c6#transactions
    - Low activity 
  - Balanced router -> cx21e94c08c03daee80c25d8ee3ea22a20786ec231
    - Used 


### `dex/swap-chart/16/1h/1619398800000000/1674959035576000`

**New API path**

`dex/swap-chart/16/1h/1619398800/1674959035` -> Does not need to change but we are storing timestamps without the 1e6 - Could keep the same 

**Intervals**
- 5m / 15m / 1h / 4h / 1d / 1w

- Format is 
  - pool_id 
  - interval (1h, 1d)
  - timestamp start 
  - timestamp end 

Current implementation is using each event on the chain and summarizing them to build the time series. This is not scalable as the chain grows since ever record needs to be fetched between a time period. 

Plan is to replace this with a cron job that creates a table per period thus reducing the load on the DB (don't need to fetch every record) and also reducing load on API (don't need to then summarize all of these with a grouping). Alternative would be to do the grouping in DB with a `group by` + table with periods but this could be expensive. Also could do grouping on API but again, this is a little expensive. 

Cron job would do the following:

- Load a config telling it when to start the TS 
- Check when the last updated time is on the DB
- Run until the TS is at head 
- To run
  - v1 -> No
    - Get list of pools at BH 
      - This would simplify the TS as then we don't need to create empty entries for non-existant pools but this is also a difficult thing to determine
      - Thus it is simply easier to check the pool nonce at the beginning and just build TS from there inserting empty rows for each TS 
    - Iterate through those pools hitting `getPoolStats`
      - Why? We already have that 
    - Build a pool object and run it through the pool price algo 
      - No need -> swaps list has lows and highs 
    - Get `TokenPool` object and persist in DB 
      - No

  - v2 
    - Get all the swaps and store in table 
      - Includes all the data we need 
    - Get nonce of dex pools for iterating over when creating TS 
    - Initialize TS by checking if the tables are empty 
      - If they are empty, create an empty pool iterand 
      - If not, check max in TS for pool ID initialize max pool id 
    - From start of dex swaps index with the following logic 
      - Init with last period in smallest interval 
        - Also get distinct all the pool ids and put them in memory 
        - If there are no swaps, then start with the first block time 
      - Build the series for the smallest interval 
      - For swaps in interval get swaps  
        - for pools in swap interval create TS entry

      - Logic pros / con  
        - Could be more efficient if storing in memory the lowest period's data and then using that to calculate the larger periods
        - This could be extra logic 
        - Number of periods in 1 yr -> time per sql -> ~.1s 
          - 1 min - ~500k -> 13 hours -> 60 pools -> 30M rows 
          - 5 min - ~100k -> 2.5 hours -> 60 -> 6M 
          - 15 min (current lowest) - 33k -> 2M rows 
          - 1 hr - ~10k 
          - 1 day - .... 

Examples:

1. https://balanced.sudoblock.io/api/v1/dex/swap-chart/8/1h/1676034916015000/1676639716015000
2. https://balanced.sudoblock.io/api/v1/dex/swap-chart/2/1h/1619995920000000/1619999520000000

