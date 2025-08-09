from pymodbus.server.sync import StartTcpServer
from pymodbus.datastore import (
    ModbusSlaveContext, 
    ModbusServerContext, 
    ModbusSequentialDataBlock
)
from pymodbus.transaction import ModbusSocketFramer
import logging

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
    
def main():
    try:
        run_server()
    except Exception as e:
        log.exception('Server terminated with exception: %s', e)

if __name__ == '__main__':
    main()