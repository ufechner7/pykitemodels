# pykitemodels
A package that provides the kite power system models as described in [KiteModels.jl](https://ufechner7.github.io/KiteModels.jl/stable/), [WinchModels.jl](https://github.com/aenarete/WinchModels.jl), [KitePodModels.jl](https://github.com/aenarete/KitePodModels.jl) and [AtmosphericModels.jl](https://github.com/aenarete/AtmosphericModels.jl) 
with a Python interface. For now, only working on Linux. If you need Windows support, please create a GitHub issue.

Could also be extended with an interface for Matlab/ Simulink. If you need that, please create a GitHub issue.

## Prerequiste
Check that `systemctl` is installed on your system:
```bash
which systemctl
```
Expected output: 
```bash
/usr/bin/systemctl
```
or similar.

If you are using a docker container, please install [docker systemctl replacement](https://github.com/gdraheim/docker-systemctl-replacement) before you continue.

## Installation
Check out this repository with git:
```bash
git clone https://github.com/ufechner7/pykitemodels.git
cd pykitemodels
```

You can use the bash script `bin/install` to install `pixi` and Julia, to add the alias jl and py
for starting Julia and Python and to configure `ipython`. Just execute point one to seven.
```bash
cd bin
./install
```
Expected output:
```
(pykitemodels) ufechner@ufryzen:~/repos/pykitemodels/bin$ ./install 
1) Install pixi
2) Install ipython config file 
3) Install juliaup
4) Install Julia 1.10
5) Initial install of Julia packages
6) Add alias for jl and py to ~/.bashrc 
7) Install modelserver.service 
8) Update Julia packages
9) Quit
Please enter your choice, 9 to quit: 9
```
<details>
  <summary>Detailed installation instruction with using the install script</summary>
  
   ### pixi
   ```
   curl -fsSL https://pixi.sh/install.sh | bash
   ```

   ### Julia
   First, install the Julia installer `juliaup`:
   ```
   curl -fsSL https://install.julialang.org | sh
   ```
   Then, install Julia with the commands:
   ```
   juliaup add 1.10
   juliaup default 1.10
   ```
   Julia 1.10 is the current stable version at the time of writing, you can also use `juliaup` to install any other version.
</details>

<details>
  <summary>Python (pixi) projects</summary>
  
   ### Using pixi to create a new Python project
   **Remark:** Not needed if you just checkout this git repository.

   #### Create a new project

   ```
   pixi init new_project
   cd new_project
   pixi add python==3.8.19
   pixi add ipython
   pixi add numpy
   ```
   By default `conda` packages are installed, but with the parameter `--pypi` you can also install packages from the Python package index PyPI. You can specify version numbers, if you don't then the newest compatible version is installed.

   #### Use a project created with pixi
   ```bash
   pixi shell
   ```
   This gives you a project-specific prompt. From this prompt, you can launch for example `ipython`.
   Further reading: https://pixi.sh/latest/basic_usage/

   Alternatively, just use the script `bin/run_python`.
</details>
<details>
  <summary>Managing Julia projects without using the install script</summary>

   ### Installing the Julia packages
   Launch Julia with
   ```
   julia --project
   ```
   Then, execute in the Julia REPL:
   ```julia
   using Pkg
   Pkg.instantiate()
   ```
   ### Updating the Julia packages
   Launch Julia with
   ```
   julia --project
   ```
   Then, execute in the Julia REPL:
   ```julia
   using Pkg
   Pkg.update()
   ```
</details>

## Usage
### Running the model server service
In the bash terminal, type
```
bin/modelserver start
```
Other options are `stop`, `restart` and `status`.

<details>
  <summary>Running the model server for testing and debugging</summary>

   ### Running the model server for testing and debugging
   Start Julia by typing `jl`, and then execute:
   ```julia
   julia> "include(\"model_server.jl\")
   ```
</details>

<details>
  <summary>Creating a systemd service manually</summary>
  
   An example service file is provided: `utils/modelserver.service.template`.

   To install it, use the script `bin/install` and select option seven.

   Enable it with
   ```
   sudo systemctl enable modelserver.service
   ```
   Start it with
   ```
   sudo systemctl start modelserver.service
   ```
   After 10 s, check if it works with
   ```
   sudo systemctl status modelserver.service
   ```
   Expected output:
   ```
   fechner@ufryzen:/etc/systemd/system$ sudo systemctl status modelserver.service 
   ● modelserver.service - provide http functions for kite simulation
      Loaded: loaded (/etc/systemd/system/modelserver.service; enabled; vendor preset: enabled)
      Active: active (running) since Fri 2024-07-19 12:25:56 CEST; 20s ago
      Main PID: 41969 (run_modelserver)
         Tasks: 21 (limit: 37416)
      Memory: 445.5M
         CPU: 7.768s
      CGroup: /system.slice/modelserver.service
               ├─41969 /bin/bash /home/ufechner/repos/pykitemodels/bin/run_modelserver
               └─41973 /home/ufechner/.julia/juliaup/julia-1.10.4+0.x64.linux.gnu/bin/julia --project -t 2 --gcthreads=2,1 -e "include(\"model_server.jl\")"

   jul 19 12:26:02 ufryzen run_modelserver[41973]:   / __ \_  ____  ______ ____  ____
   jul 19 12:26:02 ufryzen run_modelserver[41973]:  / / / / |/_/ / / / __ `/ _ \/ __ \
   jul 19 12:26:02 ufryzen run_modelserver[41973]: / /_/ />  </ /_/ / /_/ /  __/ / / /
   jul 19 12:26:02 ufryzen run_modelserver[41973]: \____/_/|_|\__, /\__, /\___/_/ /_/
   jul 19 12:26:02 ufryzen run_modelserver[41973]:           /____//____/
   jul 19 12:26:02 ufryzen run_modelserver[41973]: [ Info: 📦 Version 1.5.12 (2024-06-18)
   jul 19 12:26:02 ufryzen run_modelserver[41973]: [ Info: ✅ Started server: http://127.0.0.1:8080
   jul 19 12:26:02 ufryzen run_modelserver[41973]: [ Info: 📖 Documentation: http://127.0.0.1:8080/docs
   jul 19 12:26:02 ufryzen run_modelserver[41973]: [ Info: 📊 Metrics: http://127.0.0.1:8080/docs/metrics
   ```

</details>


### Running the model_client script
Open a new bash terminal, then execute `bin/run_python` or use the alias `py`. Finally, execute:
```python
In [1]: %run src/model_client.py 
```
Expected output: The first and second state of a simulation as dictionaries.

### Running the stress test script
Start ipython with `py`, and then execute:
```python
In [1]: %run test/test_stress.py 
```
Expected output:
```
Time, elevation: 0.05 71.19
...
Time, elevation: 29.90 68.93
Time, elevation: 29.95 68.93
Time, elevation: 30.00 68.92
Errors:  0
```

### Test the error handling
Start ipython with `py`, and then execute:
```python
In [3]: %run test/test_error.py
```
Expected output:
```
Time, elevation: 0.05 71.19
...
Time, elevation: 67.45 1.11
Time, elevation: 67.50 0.75
Time, elevation: 67.55 0.40
AssertionError("height > 0")
Error in step()
Errors:  1
```
## Reference
### Provided functions
Using the command
```python
from src.model_client import *
```
you can import the following functions:
- set_data_path(path)
- set_set(setdict)
- init()
- step(v_ro = None, set_torque=None, v_wind_gnd=6.0, wind_dir=0.0, depower=0.25, steering=0.0)
- sys_state()
- settings()
- get_errors()
- get_last_error()
- clear_errors()

## Licence
This project is licensed under the MIT License. Please see the below WAIVER in association with the license.

## WAIVER
Technische Universiteit Delft hereby disclaims all copyright interest in the package “pykitemodels” (models of airborne wind energy systems) written by the Author(s).

Prof.dr. H.G.C. (Henri) Werij, Dean of Aerospace Engineering

## Donations
If you like this software, please consider donating to https://gofund.me/508e041b .
