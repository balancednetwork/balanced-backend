from prometheus_client import Counter, Gauge


class Metrics:
    def __init__(self):

        self.crons_ran = Counter(
            "crons_ran",
            "Cron jobs ran.",
        )

        self.crons_last_timestamp = Gauge(
            "crons_last_timestamp",
            "Last timestamp running a cron.",
        )


prom_metrics = Metrics()
