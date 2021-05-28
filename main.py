import socket
import time
import sys
import signal
import wmi

def signal_handler(signal_received, frame):
    print('Monitor exit')
    sys.exit()


def is_internet_alive(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
    except OSError as error:
        # print(error.strerror)
        return False
    else:
        s.close()
        return True

def changeGateway():
    # Obtain network adaptors configurations
    nic_configs = wmi.WMI().Win32_NetworkAdapterConfiguration(IPEnabled=True)

    # First network adaptor
    nic = nic_configs[0]

    # IP address, subnetmask and gateway values should be unicode objects
    ip = u'192.168.204.158'
    subnetmask = u'255.255.255.0'
    gateway = u'192.168.204.2'

    # Set IP address, subnetmask and default gateway
    # Note: EnableStatic() and SetGateways() methods require *lists* of values to be passed
    nic.EnableStatic(IPAddress=[ip],SubnetMask=[subnetmask])
    nic.SetGateways(DefaultIPGateway=[gateway])

def run_monitor():
    while True:
        signal.signal(signal.SIGINT, signal_handler)
        if(is_internet_alive()):
            print('alive')
        else:
            print('down')
        time.sleep(1)


if __name__ == '__main__':
    run_monitor()