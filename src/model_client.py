""" MIT License

Copyright (c) 2024 Uwe Fechner

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE. """

import http.client
import json
import time

connection = http.client.HTTPConnection('127.0.0.1:8080')
ERRORS = 0
LAST_ERROR = ""

SETTINGS = {
  "sample_freq": 20, # sampling frequency [Hz]
  "log_level": 2,
  "solver": "DFBDF",
  "abs_tol": 0.0006,
  "rel_tol": 0.00001
}

def get_last_error():
    return LAST_ERROR

def set_data_path(path):
    global ERRORS
    json_data = json.dumps(path)
    connection.request('POST', '/set_data_path', json_data)
    response = connection.getresponse()
    if response.status == 200:
        obj = json.loads(response.read())
        return obj
    ERRORS += 1
    return None

def set_set(set_dict):
    global ERRORS
    json_data = json.dumps(set_dict)
    connection.request('POST', '/set_set', json_data)
    response = connection.getresponse()
    if response.status == 200:
        obj = json.loads(response.read())
        return obj
    ERRORS += 1
    return None

def init():
    global ERRORS
    connection.request('GET', '/init')
    time.sleep(0.5)
    response = connection.getresponse()
    if response.status == 200:
        obj = json.loads(response.read())
        return obj
    response.read()
    ERRORS += 1
    return None

# pylint: disable=unused-argument
def step(set_speed = None, set_torque=None, v_wind_gnd=6.0, \
         wind_dir=0.0, depower=0.25, steering=0.0):
    global ERRORS, LAST_ERROR
    json_data = json.dumps(locals())
    connection.request('POST', '/step', json_data)
    response = connection.getresponse()
    if response.status == 200:
        obj = json.loads(response.read())
        if obj is None:
            ERRORS += 1
        if obj != "OK":
            ERRORS += 1
            LAST_ERROR = obj
            return None
        return obj
    response.read()
    ERRORS += 1
    return None

def sys_state():
    global ERRORS
    connection.request('GET', '/sys_state')
    response = connection.getresponse()
    if response.status == 200:
        obj = json.loads(response.read())
        return obj
    response.read()
    ERRORS += 1
    return None

def settings():
    global ERRORS
    connection.request('GET', '/settings')
    response = connection.getresponse()
    if response.status == 200:
        obj = json.loads(response.read())
        return obj
    response.read()
    ERRORS += 1
    return None

def get_errors():
    return ERRORS

def clear_errors():
    global ERRORS, LAST_ERROR
    ERRORS = 0
    LAST_ERROR = ""

if __name__ == '__main__':
    set_data_path("data")
    set_set(SETTINGS)
    init()
    state = sys_state()
    print(state)
    state = step(depower=0.25)
    state = sys_state()
    print(state)

# To benchmark:
# ipython
# %timeit sys_state()
# result: 63.3 µs ± 3.12 µs per loop on Ryzen 7850X
#         75.2 µs ± 5.05 µs per loop on Laptop in performance mode
