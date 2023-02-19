# Streaming Design 

- Manifold to send Txs down their associated processors 
- Each processor
  - Takes in the Tx 
  - Pulls out the method and calls another processing function per method 
  - Breaks up the Tx and populates a model 
  - Returns the model which is then merged into the DB 