# balanced-backend

Backend service for Balanced Network. 

[API Docs](https://balanced.icon.community/api/v1/docs)

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
