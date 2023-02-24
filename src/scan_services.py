# MIT License
#
# Copyright (c) 2018 Airthings AS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# https://airthings.com

import logging
from bluepy.btle import Scanner, DefaultDelegate
import pandas as pd

class DecodeErrorException(Exception):
    '''
    represents error as a string
    '''
    def __init__(self, err_value):
        self.value = err_value
    def __str__(self):
        return repr(self.value)

class ScanDelegate(DefaultDelegate):
    '''
    since this class has no extra capability, it probably isn't necessary?
    '''
    def __init__(self):
        DefaultDelegate.__init__(self)

scanner = Scanner().withDelegate(ScanDelegate())

logger = logging.getLogger('bluetooth')
logger.setLevel(logging.DEBUG)

company_ids = pd.read_csv('data/Bluetooth-Company-Identifiers.csv')
company_ids.columns = ['id','company']
company_dict = pd.Series(company_ids.company.values,index=company_ids.id).to_dict()

try:
    devices = scanner.scan(20.0)
    for dev in devices:
        ManuData = ""
        for (adtype, desc, value) in dev.getScanData():
            if desc == "Manufacturer":
                ManuData = value

            if ManuData == "":
                continue

            #Start decoding the raw Manufacturer data
            ManuDataHex = [f"{int(i+j, 16):02x}".upper() for i,j in zip(ManuData[::2], ManuData[1::2])]
            manufacturer_bt_code = '0x'+ ''.join(ManuDataHex[0:2][::-1])
            if manufacturer_bt_code == '0x0334': # Airthings, formerly Correntium AS
                print('....Airthings device:')
            print(manufacturer_bt_code, company_dict[manufacturer_bt_code])
            serial = ''.join(ManuDataHex[2:5])
            print( f"{dev.addr} ({dev.addrType}), RSSI={dev.rssi} dB, SN={serial}" )


except DecodeErrorException as e:
    print(e)
