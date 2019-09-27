#!/usr/bin/env python
# coding: utf-8

"""
usage: fmplapla.py --station fmrara768 --time 1800 | mplayer.exe - -dumpstream -dumpfile out.ogg

"""

import sys
import time
import argparse
#!pip install websocket-client
import websocket

class fmplapla:
    def __init__(self, station_id, duration=0):
        self.station_id = station_id
        self.duration = duration
        self.start_time = time.time()
        self.count = 0
        #websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp('wss://fmplapla.com/socket', on_open=self._on_open, on_message=self._on_message)
        try:
            self.ws.run_forever()
        except (Exception, KeyboardInterrupt, SystemExit) as e:
            self.ws.close()
    
    def _on_message(self, data):
        if data:
            sys.stdout.buffer.write(data)
        if self.duration > 0:
            if self.duration < (time.time() - self.start_time):
                raise KeyboardInterrupt
        self.ws.send('{{"method":"continue","count":{count}}}'.format(count=self.count))
        self.count += 1
    
    def _on_open(self):
        self.ws.send('{{"method":"start","station":"{station}","burst":5}}'.format(station=self.station_id))

def main():
    parser = argparse.ArgumentParser(description='example: python fmplapla.py -s fmrara768 -t 1800 | mplayer -')
    parser.add_argument('-s', '--station', required=True, help='station id. example: fmrara768')
    parser.add_argument('-t', '--time', type=int, default=0, help='stop writing the output after its seconds reaches duration. it defaults to 0, meaning that loop forever.')
    args = parser.parse_args()
    radio = fmplapla(args.station, args.time)

if __name__ == '__main__':
    main()
