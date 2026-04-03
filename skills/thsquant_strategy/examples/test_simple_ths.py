# Minimal test strategy
from mindgo_api import *


def initialize(context):
    log.info("INITIALIZE CALLED")
    set_benchmark("000300.SH")
    run_daily(daily_run, time_rule="after_open", hours=0, minutes=0)


def daily_run(context):
    log.info("DAILY_RUN CALLED at " + context.current_dt.strftime("%Y-%m-%d %H:%M"))
