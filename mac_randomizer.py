import random
import time
import argparse
import subprocess
import logging
import signal
import sys

class MACRandomizer:
    def __init__(self, interface, interval=3600):
        self.interface = interface
        self.interval = interval
        self.running = True
        logging.basicConfig(
            filename='/var/log/mac-randomizer/mac_randomizer.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def generate_valid_mac(self):
        oui = ['00:16:3e', '00:04:4b', '00:1d:0f']
        return f"{random.choice(oui)}:{random.randint(0x00, 0x7f):02x}:{random.randint(0x00, 0xff):02x}:{random.randint(0x00, 0xff):02x}"

    def change_mac(self):
        new_mac = self.generate_valid_mac()
        try:
            subprocess.run(['ip', 'link', 'set', 'dev', self.interface, 'down'], check=True)
            subprocess.run(['ip', 'link', 'set', 'dev', self.interface, 'address', new_mac], check=True)
            subprocess.run(['ip', 'link', 'set', 'dev', self.interface, 'up'], check=True)
            logging.info(f"Changed MAC to {new_mac} on {self.interface}")
            return True
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to change MAC: {str(e)}")
            return False

    def run(self):
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        logging.info("Service started")
        
        while self.running:
            if self.change_mac():
                time.sleep(self.interval)
            else:
                time.sleep(60)

    def signal_handler(self, signum, frame):
        logging.info("Service stopping")
        self.running = False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='MAC Address Randomizer')
    parser.add_argument('-i', '--interface', required=True, help='Network interface')
    parser.add_argument('-t', '--interval', type=int, default=3600, help='Change interval in seconds')
    args = parser.parse_args()

    try:
        mac_randomizer = MACRandomizer(args.interface, args.interval)
        mac_randomizer.run()
    except Exception as e:
        logging.critical(f"Critical error: {str(e)}")
        sys.exit(1)