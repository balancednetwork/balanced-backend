# Prices 

Notes on how to get prices for pools / tokens 

## Steps 

#### Build index of pools 

1. Get list of tokens 
  - This is sourced from git repo 
    - balancednetwork/balanced-network-interface/store/lists/<list.json>
    - [balanced](https://github.com/balancednetwork/balanced-network-interface/blob/master/src/store/lists/tokenlist.json) 
    - [community](https://github.com/balancednetwork/balanced-network-interface/blob/master/src/store/lists/communitylist.json)
  - Put all the tokens in the DB with their symbols 
2. Pull all the pool names / ids 
  - Hit the `getNamedPools` method on the dex contract 
  - Iterate through the pools, match the token symbol to get token address
  - Hit the `getPoolId` method on dex to get pool ID 
  - Insert the pool names / ID into the pools table 

#### Update pool and token prices 

- Calculate decimals 
  - 1e18 + quote decimals - base decimals 


- getNonce
- getPoolStats 


For pool id #5 

```json
{
  "base": "0x1e9bfbb03d",
  "base_decimals": "0x6",
  "base_token": "cxae3034235540b924dfcc1b45836c293dcc82bfb7",
  "min_quote": "0x8ac7230489e80000",
  "name": "IUSDC/bnUSD",
  "price": "0xc98e7d8993f993e7e6c6dc1f7",
  "quote": "0x1bc8f579e61141dda951",
  "quote_decimals": "0x12",
  "quote_token": "cx88fd7df7ddff82f7cc735c871dc519838cb235bb",
  "total_supply": "0x18a56a2f5f850b5"
}
```

Base: IUSDC
Quote: bnUSD 

```python
# quote liquidity / total supply 
int('0x1bc8f579e61141dda951', 16) / 1e18
# 131210.9322741956

# base liquidity / total supply 
int('0x1e9bfbb03d', 16) / 1e6
# 131465.982013

# Price 
int('0xc98e7d8993f993e7e6c6dc1f7', 16) / 1e30 
# 0.9980599563864423

```