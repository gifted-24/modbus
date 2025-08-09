from pymodbus.client.sync import ModbusTcpClient

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

def main():
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
    return None
    
if __name__ == '__main__':
    main()
    