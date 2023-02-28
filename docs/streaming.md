# Streaming 

Currently no streaming is required but the rigging is in place to enable this feature in the future. 

To do that:
- [ ] Uncomment all the code in `streaming` and `tests/streaming`
  - The tests should use fixtures for each block that an event is trying to be built around. 
- [ ] Enable the packages in CI 
  - Proto takes 15 min to install so leaving that out 
- [ ] Deploy the container in the cluster
  - Current helm chart doesn't have the 

### Design 

- Manifold to send Txs down their associated processors 
- Each processor
  - Takes in the Tx 
  - Pulls out the method and calls another processing function per method 
  - Breaks up the Tx and populates a model 
  - Returns the model which is then merged into the DB 

