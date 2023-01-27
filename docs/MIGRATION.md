# Migration 

This document overviews all the steps needed to sunset the [balanced-geometry-backend](https://github.com/balancednetwork/balanced-geometry-backend) repo. 

## In Use Endpoints 

### `dex/stats/<pool-id>`

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

#### Issues 

- Need to determine how to get the `min_quote`

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

### `stats/dex-pool-stats-24h`

### `stats/dex-pool-stats-30d`

### `stats/dividends-fees`

