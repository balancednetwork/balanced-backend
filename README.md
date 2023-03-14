# balanced-backend
[![loopchain](https://img.shields.io/badge/ICON-API-blue?logoColor=white&logo=icon&labelColor=31B8BB)](https://shields.io) [![GitHub Release](https://img.shields.io/github/release/balancednetwork/balanced-backend.svg?style=flat)]() ![](https://github.com/balancednetwork/balanced-backend/workflows/push-main/badge.svg?branch=main) ![](https://img.shields.io/github/license/balancednetwork/balanced-backend)

Backend service for Balanced Network. 

[API Docs](https://balanced.icon.community/api/v1/docs) + [Live Stats Page](https://stats.balanced.network/)

### Development

For local development, you will want to run the `docker-compose.db.yml` as you develop. To run the tests,

```bash
make test
```

### Deployment 

To bring up the whole stack, run:

```bash
docker-compose -f docker-compose.db.yml -f docker-compose.yml up -d
```

If you are running in prod, be sure to change the DB password with an `.env` file. You'd be also wise to run a local ICON node. Note that sync time might be slow and is not tested outside of proximity to the ICON tracker. 

### License 

Apache 2.0
