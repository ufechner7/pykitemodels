from math import degrees
from src.model_client import *

setdict = {
  "sample_freq": 20, # sampling frequency [Hz]
  "sim_time": 30.0,  # simulation time    [s]
  "log_level": 2,
  "solver": "DFBDF",
  "abs_tol": 0.0006,
  "rel_tol": 0.00001
}

def test_stabilization():
    set_data_path("data")
    clear_errors()
    set = settings()
    dt = 1/set["sample_freq"]
    sim_time = setdict["sim_time"]

    sys_state_ = init_model()

    # preprocessing and time setting
    sys_states = []
    sys_states += [sys_state_]

    # simulation
    final_time = int(sim_time/dt)
    for i in range(final_time):
        res = step(depower=0.25)
        if res is None:
            print("Error in step()")
            break
        sys_state_ = sys_state()
        time.sleep(0.048)
        print("Time, elevation:", "{:.2f}".format(sys_state_["time"]), "{:.2f}".format(degrees(sys_state_["elevation"])))
        sys_states += [sys_state_]


def init_model():
    # update the settings using the variable setdict
    set_set(setdict)

    # initialization
    init()
    sys_state_=sys_state()
    return sys_state_

if __name__ == '__main__':
    test_stabilization()
    print("Errors: ", get_errors())