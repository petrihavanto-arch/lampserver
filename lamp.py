#!/usr/bin/env python3

import relayserver

import os



import logging
import sys
import traceback
from datetime import datetime
from pathlib import Path
import signal
import threading
from functools import wraps



import commondata
import proccmdline


log = logging.getLogger(__name__)
logfilename = "releohjain"
logging.basicConfig(level=commondata.loglevel,
                    format=commondata.FORMAT,
                    datefmt="%H:%M:%S",
                    filename=commondata.logpath+logfilename+".log")

pihavalo_socket = 11111
pihavalo_ohjain_releportti = 'B'
pihavalo_on_html = "html/Pihavalo-ohjain_on.htm"
pihavalo_off_html = "html/Pihavalo-ohjain_off.htm"


def setup_logging(script_name):
    """Configure logging to both file and console with rotation"""
    if commondata.pi :
        log_dir = Path('/home/pi/logs')
    else:
        log_dir= Path('/home/petri/logs')
    log_dir.mkdir(exist_ok=True)

    log_file = log_dir / f"{script_name}_{datetime.now().strftime('%Y%m%d')}.log"

    # Configure logging format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # File handler with rotation
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # Root logger configuration
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# Decorator for error handling
def error_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger = logging.getLogger()
            logger.error(f"Error in {func.__name__}: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise
    return wrapper

# System resource monitoring
def monitor_system_resources():
    """Monitor system resources and log if they exceed thresholds"""
    while True:
        try:
            # CPU temperature
            with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
                temp = float(f.read()) / 1000
                if temp > 80:  # Temperature threshold in Celsius
                    logging.warning(f"High CPU temperature: {temp}°C")

            # Memory usage (requires psutil)
            import psutil
            memory = psutil.virtual_memory()
            if memory.percent > 90:  # Memory threshold
                logging.warning(f"High memory usage: {memory.percent}%")

        except Exception as e:
            logging.error(f"Error in resource monitoring: {str(e)}")

        threading.Event().wait(60)  # Check every minute

# Signal handler
def signal_handler(signum, frame):
    """Handle system signals gracefully"""
    logger = logging.getLogger()
    logger.info(f"Received signal {signum}. Performing cleanup...")
    # Add your cleanup code here
    sys.exit(0)


if __name__ == '__main__':

    # Initialize logging
    logger = setup_logging("lamp")

    # Register signal handlers
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    # Start resource monitoring in background
    monitor_thread = threading.Thread(target=monitor_system_resources, daemon=True)
    monitor_thread.start()


    @error_handler
    def main():
        args = proccmdline.proccmdline()
        if vars(args)['debug']:
            loglevel_here = logging.DEBUG
        else:
            loglevel_here = logging.INFO

        logging.getLogger("relayserver").setLevel(loglevel_here)

        log.info("--------------Lampserver @ socket "+str(pihavalo_socket)+" --------------")
        mylampserver = relayserver.relayserver(lampport=pihavalo_socket,
                                             releportti=pihavalo_ohjain_releportti,
                                             on_html=pihavalo_on_html,
                                             off_html=pihavalo_off_html,
                                             time_increment=commondata.TimeIncrement)


    try:
        main()
    except Exception as e:
        logger.error(f"Script terminated due to error: {str(e)}")
        sys.exit(1)


