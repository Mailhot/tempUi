import serial
ser = serial.Serial('/dev/ttyUSB1')
ser.flushInput()

device_addresses = {'3BAADF410BF40DF1': 'grill_temp',
                    '3BE5EC410BF42D49': 'meat_temp',
                    }


while True:
    try:
        ser_bytes = ser.readline()
        decoded_bytes = str(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
        print(decoded_bytes)
        if decoded_bytes.startswith('Device_Address:'):
            _, device_address, _, temp_c = decoded_bytes.split(' ')
            device = device_addresses.get(device_address)
            print(device, temp_c)

    except Exception as e:
        print(e)
        print("Keyboard Interrupt")
        break