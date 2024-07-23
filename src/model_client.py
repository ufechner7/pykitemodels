import http.client
import json
import time

connection = http.client.HTTPConnection('127.0.0.1:8080')
errors = 0
last_error = ""

setdict = {
  "sample_freq": 20, # sampling frequency [Hz]
  "log_level": 2,
  "solver": "DFBDF",
  "abs_tol": 0.0006,
  "rel_tol": 0.00001
}

def get_last_error():
    return last_error

def set_data_path(path):
    global errors
    json_data = json.dumps(path)
    connection.request('POST', '/set_data_path', json_data)
    response = connection.getresponse()
    if response.status == 200:
        obj = json.loads(response.read())
        return obj
    errors += 1
    return None    

def set_set(setdict):
    global errors
    json_data = json.dumps(setdict)
    connection.request('POST', '/set_set', json_data)
    response = connection.getresponse()
    if response.status == 200:
        obj = json.loads(response.read())
        return obj
    errors += 1
    return None

def init():
    global errors
    connection.request('GET', '/init')
    time.sleep(0.5)
    response = connection.getresponse()
    if response.status == 200:
        obj = json.loads(response.read())
        return obj
    response.read()
    errors += 1
    return None

def step(v_ro = None, set_torque=None, v_wind_gnd=6.0, wind_dir=0.0, depower=0.25, steering=0.0):
    global errors, last_error
    json_data = json.dumps(locals())
    connection.request('POST', '/step', json_data)
    response = connection.getresponse()
    if response.status == 200:
        obj = json.loads(response.read())
        if obj is None:
            errors += 1
        if obj != "OK":
            errors += 1
            last_error = obj
            return None
        return obj
    response.read()
    errors += 1
    return None

def sys_state():
    global errors
    connection.request('GET', '/sys_state')
    response = connection.getresponse()
    if response.status == 200:
        obj = json.loads(response.read())
        return obj
    response.read()
    errors += 1
    return None

def settings():
    global errors
    connection.request('GET', '/settings')
    response = connection.getresponse()
    if response.status == 200:
        obj = json.loads(response.read())
        return obj
    response.read()
    errors += 1
    return None

def get_errors():
    return errors

def clear_errors():
    global errors, last_error
    errors = 0
    last_error = ""

if __name__ == '__main__':
    set_data_path("data")
    set_set(setdict)
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