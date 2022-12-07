# Written by Caleb C. in 2022 for general device connectivity.
# Exact data structure will need to be implemented for your device!
# Leverages configuration of your device from the 'dev.toml' config.
import struct
import threading
import time
import usb.core
import toml
import logging
import sqlite3
import queue

# The TOML file should contain the following fields:
#
#   [logging]
#   level = "info"     # logging level (one of "debug", "info", "warning", "error", "critical")
#   filename = "log.txt"  # logging filename (optional)
#
#   [device]
#   vendor_id = 0x1234  # USB device vendor ID
#   product_id = 0x5678  # USB device product ID
#   endpoint = 0x01  # USB device endpoint for data transfer
#   max_packet_size = 64  # maximum packet size for data transfer
#   time_limit = 60  # time limit for reading data from USB device (in seconds)
#
#   [database]
#   path = "data.db"  # path to SQLite3 database file
#
# If the configuration file is not found or is malformed, an error message is logged
# and None is returned.
def load_config():
    try:
        config = toml.load("config.toml")
    except toml.TomlDecodeError as e:
        logging.error("Failed to load configuration: {}".format(e))
        return None
    return config

# connect_to_usb_device() finds the USB device with the specified vendor and product IDs,
# and sets its configuration.
#
# The function takes a dictionary with the following fields:
#
#   vendor_id: the vendor ID of the USB device
#   product_id: the product ID of the USB device
#
# If the USB device is not found, a ValueError is raised with an error message.
# If the configuration of the USB device fails, an error message is logged and None
# is returned. Otherwise, the USB device object is returned.
def connect_to_usb_device(config):
    dev = usb.core.find(
        idVendor=config["device"]["vendor_id"], idProduct=config["device"]["product_id"])
    if dev is None:
        raise ValueError(
            "Could not find USB device with specified vendor and product IDs")
    dev.set_configuration()  # type: ignore
    return dev

# open connection to SQLite3 database
def open_database_connection(config):
    try:
        db = sqlite3.connect(config["database"]["path"])
    except Exception as e:
        logging.error("Failed to open database connection: {}".format(e))
        return None
    return db

# Create data buffer
# thread-safe queue data structure provided by the queue module, which allows multiple threads
# to safely add and remove items from the queue without interfering with each other.
data_buffer = queue.Queue()

# start concurrent thread to decode data from buffer and publish to database
def decode_and_publish(db):
    while True:
        # check if there is data in the buffer
        if not data_buffer.empty():
            # decode data from buffer into integers using struct.unpack()
            data = struct.unpack("ii", data_buffer.get())

            # publish data to database
            db.execute("INSERT INTO data (value) VALUES (?)", data)
            db.commit()

# The function reads data from the USB device, and adds it to the buffer. If there is
# an error reading from the USB device, an error message is logged and the function
# returns. Otherwise, the function continues to read data from the USB device until
# the time limit is reached, at which point the function returns.
#   dev: the USB device object
#   config: a dictionary containing the configuration for the USB device
#   time_limit: the time limit for reading data from the USB device (in seconds)
def read_from_usb_device(dev, config, time_limit):
    start_time = time.time()
    while True:
        if time.time() - start_time >= time_limit:
            break
        try:
            data = dev.read(config["device"]["endpoint"],
                            config["device"]["max_packet_size"])
        except Exception as e:
            logging.error("Failed to read from USB device: {}".format(e))
            break
        data_buffer.put(data)

# main function
def main():
    # load configuration
    config = load_config()
    if config is None:
        return

    # configure logging
    logging.basicConfig(
        level=config["logging"]["level"], filename=config["logging"]["filename"])

    # connect to USB device
    dev = connect_to_usb_device(config)
    if dev is None:
        return

    # open database connection
    db = open_database_connection(config)
    if db is None:
        return

    # start concurrent thread to decode and publish data
    thread = threading.Thread(target=decode_and_publish, args=(db,))
    thread.start()

    # read data from USB device and add it to the buffer
    read_from_usb_device(dev, config, config["device"]["time_limit"])


if __name__ == "__main__":
    main()
