# Modbus TCP Lab — pymodbus + mbpoll

### Files contained in this single script:

1) README (this header)
2) modbus_server.py      --> Minimal pymodbus TCP server (simulator)
3) python_client.py      --> Minimal pymodbus client for automation tests (optional)
4) mbpoll_tests.sh       --> Bash script with mbpoll commands to exercise the server
5) requirements.txt      --> Python dependencies

### Purpose:
- Provide a ready-to-run Modbus TCP simulator using pymodbus on a non-privileged port (default 5020).
- Provide quick examples showing how to query and write registers using `mbpoll` from the terminal.
- Provide a simple Python client you can extend for scripted test scenarios.

### Notes / Prerequisites (Debian / Termux):
- Python 3.8+ (python3)
- pip (python3 -m pip)
- Install Python deps: 
```bash
python3 -m pip install -r requirements.txt
```
- Install mbpoll: 
```bash
sudo apt install mbpoll
``` 
(or compile/install from https://github.com/epsilonrt/mbpoll)

- Use a non-privileged port (5020) so root is not required. If you must use port 502, run as root (not recommended).

### How to run:
1. Start the simulated Modbus TCP server:
```bash
python modbus_server.py
```
2. In another terminal, run the mbpoll test script (make it executable first):
```bash
chmod 0755 mbpoll_tests.sh
./mbpoll_tests.sh
```

3. Optionally run python_client.py to perform scripted reads/writes.

## requirements.txt

- pymodbus provides Modbus client/server functionality
```plaintext
pymodbus
```

## modbus_server.py

- Minimal synchronous pymodbus TCP server with a simple holding-register datastore.

- Listens on 0.0.0.0:5020 and exposes 100 holding registers (addresses 0..99).
```python
from pymodbus.server.sync import StartTcpServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.transaction import ModbusSocketFramer
import logging
import threading

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

def run_server(host='0.0.0.0', port=5020):
    # Initial data: 100 holding registers initialized to incremental values for easy testing
    initial_values = [i for i in range(100)]
    block = ModbusSequentialDataBlock(0, initial_values)

    store = ModbusSlaveContext(hr=block, di=None, co=None, ir=None)
    context = ModbusServerContext(slaves=store, single=True)

    log.info(f"Starting Modbus TCP server on {host}:{port} (100 holding registers: 0..99)")
    StartTcpServer(context, address=(host, port), framer=ModbusSocketFramer)

if __name__ == '__main__':
    try:
        run_server()
    except Exception as e:
        log.exception('Server terminated with exception: %s', e)
```

## python_client.py

- Minimal pymodbus client to read/write holding registers programmatically.
- Use this to create automated test sequences instead of calling mbpoll.
```python
from pymodbus.client.sync import ModbusTcpClient
import time

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5020
UNIT_ID = 1


def read_holding(client, address=0, count=10, unit=UNIT_ID):
    rr = client.read_holding_registers(address, count, unit=unit)
    if rr.isError():
        print(f"Error reading regs @ {address}:{count} -> {rr}")
        return None
    return rr.registers


def write_register(client, address, value, unit=UNIT_ID):
    rq = client.write_register(address, value, unit=unit)
    if rq.isError():
        print(f"Error writing reg {address} = {value} -> {rq}")
        return False
    return True


if __name__ == '__main__':
    client = ModbusTcpClient(SERVER_HOST, port=SERVER_PORT)
    if not client.connect():
        print('Unable to connect to server')
        exit(1)

    print('Reading first 10 holding registers:')
    regs = read_holding(client, address=0, count=10)
    print(regs)

    print('Writing 999 to register 10')
    ok = write_register(client, 10, 999)
    print('Write ok:', ok)

    print('Reading register 10 back:')
    regs = read_holding(client, address=10, count=1)
    print(regs)

    client.close()
```

## mbpoll_tests.sh

- Small Bash script with mbpoll commands to exercise the local server.
```bash
#!/usr/bin/env bash
set -euo pipefail

HOST=127.0.0.1:5020
UNIT=1

echo "=== Read 10 holding registers (0..9) ==="
mbpoll -m tcp ${HOST} -a ${UNIT} -t 4 -r 0 -c 10 || echo "mbpoll read failed"

echo
echo "=== Write 555 to holding register 20 ==="
# mbpoll write syntax: mbpoll -m tcp host -a unit -t <type> -r <address> <value>
mbpoll -m tcp ${HOST} -a ${UNIT} -t 4 -r 20 555 || echo "mbpoll write failed"

echo
echo "=== Read register 20 back ==="
mbpoll -m tcp ${HOST} -a ${UNIT} -t 4 -r 20 -c 1 || echo "mbpoll read failed"


echo
echo "=== Read large block (50 regs starting @ 30) ==="
mbpoll -m tcp ${HOST} -a ${UNIT} -t 4 -r 30 -c 50 || echo "mbpoll read failed"


echo
echo "=== Done ==="
```
