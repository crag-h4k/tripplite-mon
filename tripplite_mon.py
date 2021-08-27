#!/usr/bin/python3

from time import sleep
from sys import argv
from datetime import datetime

from libs.GudLogger import Logger

from tripplite import Battery
from pprint import pformat


def log_battery_status(log_file='/var/log/tripplite.log', loop=True, check_period=300) -> None:
    logger = Logger(outfile=log_file)
    fail_check_period=10
    while loop:
        """Read battery and reopen in error. Use for long polling."""
        try:
            battery = Battery()
            battery.open()
            battery_status = battery.get()
            battery_status['ts'] = str(datetime.now())
            pretty_status = pformat(battery_status)
            #logger.info(f"{battery_status}")
            logger.info(f"{pretty_status}")
            sleep(check_period)
            battery.close()
            del battery
        except (IOError, OSError, ValueError) as e:
            logger.error(f"could not read battery: {e}")
            sleep(fail_check_period)
            pass

        except KeyboardInterrupt:
            return;


if __name__ == '__main__':
    ups_log = str(argv[1])
    poll_interval = int(argv[2])
    log_battery_status(log_file = ups_log, check_period = poll_interval)

 
