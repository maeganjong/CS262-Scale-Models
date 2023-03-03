# CS262-Scale-Models
Engineering Ledger: https://docs.google.com/document/d/18v5nVU6SXk_cNxRAmRWeSkrR3bIV8FubQHznuHwNOJY/edit?usp=sharing

## Running the Code

### Setup
1. Setup a new environment through `spec-file.txt`. Run `conda create --name <env> --file spec-file.txt`
2. Run `conda activate <env>`
3. Change the server address `SERVER` value in `commands.py` to the `hostname` of your server. To find hostname, enter `hostname` on your terminal.

### Running the Server
1. Open a new terminal session
2. Run `python3 run_server.py`

### Running the Processes
To simulate this model, we require 3 new separate terminal session beyond the one previously ran for the server. Each of these terminal sessions will simulate a separate process.
1. Open 3 separate terminal sessions
2. Run `python3 run_process.py --p <process_number>` such that `process_number` is either `0`, `1`, or `2`. Ensure that `process_number` is different for each terminal session.

The three commands that should be used for each of your terminal session are:
- `python3 run_process.py --p 0`
- `python3 run_process.py --p 1`
- `python3 run_process.py --p 2`
<!-- 3. [Optional] Customize the range of clockspeeds the processes can be assigned to by passing an additional commandline argument  -->

## Understanding the Simulation

### Accessing the Files
Each of the processes's log files can be found at the root directory in file `<process_num>.log` under the respective `process_num`.

You can reference prior experiments by accessing the `Experiments` folder. Log files with the same header are from the same experimental run.

## Interpreting the Logs

Each of the processes report the assigned clockspeed at the start of the log. 

Subsequently, each of the processes log different events:
- Sent message
    - Records when the process sends a message to another process. 
    - Includes the recipient of the message, the logical clock time, and the system clock when the sent action occurs. 
- Internal message 
    - Records when the process just wakes up and does nothing. 
    - Includes the the logical clock time and the system clock when the sent action occurs. 
- Receive message 
    - Records when the process receives a message from the queue. 
    - Includes the sender of the message, the logical clock time, and the system clock when the sent action occurs. 
    - The logical clock time is the max of the reciepient's clock time and the message's clock time, incremented by one.
