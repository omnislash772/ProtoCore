import usb.core # type: ignore
import usb.util # type: ignore

Temperhum_Vendor = 0x1a86
Temperhum_Product = 0xe025
Temperhum_Interface = 1
Temperhum_ID = hex(Temperhum_Vendor) + ':' + hex(Temperhum_Product)
Temperhum_ID = Temperhum_ID.replace( '0x', '')

# Function to return a string of hex character representing a byte array

def byte_array_to_hex_string( byte_array ):
    array_size = len(byte_array)
    if array_size == 0:
        s = ""
    else:
        s = ""         
        for var in list(range(array_size)):
            b = hex(byte_array[var])
            b = b.replace( "0x", "")
            if len(b) == 1:
                b = "0" + b
            b = "0x" + b
            s = s + b + " "
    return (s.strip())

# The temperature is a 16 bit signed integer, this function converts it to signed decimal

def twos_complement(value,bits):
#    value = int(hexstr,16)
    if value & (1 << (bits-1)):
        value -= 1 << bits
    return value


def gethotmoist():
# Try to find the Temperhum usb device
    device = usb.core.find(idVendor = Temperhum_Vendor, idProduct = Temperhum_Product)
# If it was not found report the error and exit

    if device is None:
        return(0,0)
# check if it has a kernal driver, if so set a reattach flag and detach it

    if device.is_kernel_driver_active(1):
        result = device.detach_kernel_driver(1)
        if result != None:
            return(0,0)
        

# Extract the correct interface information from the device information

    cfg = device[0]
    inf = cfg[Temperhum_Interface,0]
    result = usb.util.claim_interface(device, Temperhum_Interface)
    
    if result != None:
        return(0,0)
    
# Extract the read and write endpoint information 
    ep_read = inf[0]
    ep_write = inf[1]

# Extract the addresses to read from and write to
    ep_read_addr = ep_read.bEndpointAddress
    ep_write_addr = ep_write.bEndpointAddress

    try:
        msg = b'\x01\x80\x33\x01\0\0\0\0'
        device.write(ep_write_addr, msg)
    except:
        return(0,0)
   
    try:
        data = device.read(ep_read_addr, 0x8)
    except:
        return(0,0)

# Decode the temperature and humidity
    temperature = round( ( twos_complement( (data[2] * 256) + data[3],16 ) ) / 100, 1 )
    humidity = int( ( (data[4] * 256) + data[5] ) / 100 )

# Output the temperature and humidity
    # Release the usb resources
    result = usb.util.dispose_resources(device)
    return(temperature, humidity)
