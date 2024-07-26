from math import degrees
from src.model_client import *

""" 
Test the error handling. 
Expected output:

Time, elevation: 67.50 0.75
Time, elevation: 67.55 0.40
AssertionError("height > 0")
Error in step()
Errors:  1
"""

setdict = {
  "sample_freq": 20, # sampling frequency [Hz]
  "sim_time": 70.0,
  "log_level": 2,
  "solver": "DFBDF",
  "abs_tol": 0.0006,
  "rel_tol": 0.00001
}

SIM_TIME = setdict["sim_time"]

def test_stabilisation():
    set_data_path("data")
    clear_errors()
    set = settings()
    dt = 1/set["sample_freq"]

    sys_state_ = init_model()

    # preprocessing and time setting
    sys_states = []
    sys_states += [sys_state_]

    # simulation
    final_time = int(SIM_TIME/dt)
    for i in range(final_time):
        res = step(depower=0.25)
        if res is None:
            print("Error calling step(): " + get_last_error())
            break
        sys_state_ = sys_state()
        print("Time, elevation:", "{:.2f}".format(sys_state_["time"]), "{:.2f}".format(degrees(sys_state_["elevation"])))
        sys_states += [sys_state_]

def init_model():
    # update the settings using the variable setdict
    set_set(setdict)

    # initialization
    init()
    return sys_state()

if __name__ == '__main__':
    test_stabilisation()
    print("Errors: ", get_errors())