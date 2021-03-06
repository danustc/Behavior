import time
import serial


def pump_initial(serial_port):
    ser = serial.Serial(serial_port,19200,timeout=.1)
    print('connected to', ser.name)

def find_pumps(ser,tot_range=10):
    pumps = []
    for i in range(tot_range):
        ser.write('%iADR\x0D'.encode()%i)
        output = ser.readline()
        if len(output)>0:
            pumps.append(i)
    return pumps

def query(ser):
    cmd = '\r\x0D'.encode()
    ser.write(cmd)
    output = ser.readline().decode()
    return output


def run_all(ser):
    cmd = '*RUN\x0D'
    ser.write(cmd.encode())
    output = ser.readline().decode()
    if '?' in output: print(cmd.strip()+' from run_all not understood')

def stop_all(ser):
    cmd = '*STP\x0D'.encode()
    ser.write(cmd)
    output = ser.readline().decode()
    if '?' in output: print(cmd.decode().strip()+' from stop_all not understood')

def stop_pump(ser,pump):
    cmd = '%iSTP\x0D'%pump
    ser.write(cmd.encode())
    output = ser.readline().decode()
    if '?' in output: print(cmd.strip()+' from stop_pump not understood')
    print(output)

def set_direct(ser,pump,dire):
    if dire==1:
        direction = 'INF'
    else:
        direction = 'WDR'
    frcmd = '%iDIR%s\x0D'%(pump,direction)
    ser.write(frcmd.encode())
    output = ser.readline().decode()
    if '?' in output: print(frcmd.strip()+' from set_rate not understood')
    print("Direct:", output)

def set_rate(ser, pump, flowrate):
    # set single rate 
    cmd = ''
    direction = 'INF'
    if flowrate<0:
        direction = 'WDR'
    frcmd = '%iDIR%s\x0D'%(pump,direction)
    ser.write(frcmd.encode())
    output = ser.readline().decode()
    if '?' in output: print(frcmd.strip()+' from set_rate not understood')
    fr = abs(flowrate)

    if fr<5000:
        cmd += str(pump)+'RAT'+str(fr)[:5]+'UH*'
    else:
        fr = fr/1000.0
        print(fr)
        cmd += str(pump)+'RAT'+str(fr)[:5]+'MH*'
    print('The rate is set at:')
    print((cmd.strip()))
    print(cmd)
    cmd += '\x0D'
    ser.write(cmd.encode())
    output = ser.readline().decode()
    if '?' in output: print(cmd.strip()+' from set_rates not understood')


def set_rates(ser,rate):
#    cmd = ''
    for pump in rate:
        cmd = ''
        flowrate = float(rate[pump])
        direction = 'INF'.encode()
        if flowrate<0: direction = 'WDR'.encode()
        frcmd = '%iDIR%s\x0D'.encode()%(pump,direction)
        ser.write(frcmd)
        output = ser.readline().decode()
        if '?' in output: print(frcmd.decode().strip()+' from set_rate not understood')
        fr = abs(flowrate)
        if fr<5000:
            cmd += str(pump)+'RAT'+str(fr)[:5]+'UH*'
        else:
            fr = fr/1000.0
            print(fr)
            cmd += str(pump)+'RAT'+str(fr)[:5]+'MH*'
        print('The rate is set at:')
        print((cmd.strip()))
        print(cmd)
        cmd += '\x0D'
        ser.write(cmd.encode())
        output = ser.readline().decode()
        if '?' in output: print(cmd.decode().strip()+' from set_rates not understood')

def get_rate(ser,pump):
    #get direction
    cmd = '%iDIR\x0D'%pump
    ser.write(cmd.encode())
    output = ser.readline().decode()
    sign = ''
    if output[4:7]=='WDR':
        sign = '-'
    cmd = '%iRAT\x0D'%pump
    ser.write(cmd.encode())
    output = ser.readline().decode()
    if '?' in output: print(cmd.strip()+' from get_rate not understood')
    units = output[-3:-1]
    if units=='MH':
        rate = str(float(output[4:-3])*1000)
    if units=='UH':
        rate = output[4:-3]
    return sign+rate

def get_rates(ser,pumps):
    rates = dict((p,get_rate(ser,p).split('.')[0]) for p in pumps)
    return rates

def set_diameter(ser,pump,dia):
    cmd = '%iDIA%s\x0D'%(pump,dia)
    ser.write(cmd.encode())
    output = ser.readline().decode()
    if '?' in output: print(cmd.strip()+' from set_diameter not understood')

def get_diameter(ser,pump):
    cmd = '%iDIA\x0D'%pump
    ser.write(cmd.encode())
    output = ser.readline().decode()
    if '?' in output: print(cmd.strip()+' from get_diameter not understood')
    dia = output[4:-1]
    return dia

def prime(ser,pump):
    # set infuse direction
    cmd = '%iDIRINF\x0D'%pump
    ser.write(cmd.encode())
    output = ser.readline().decode()
    if '?' in output: print(cmd.strip()+' from prime not understood')

    # set rate
    cmd = '%iRAT10.0MH\x0D'%pump
    ser.write(cmd.encode())
    output = ser.readline().decode()
    if '?' in output: print(cmd.strip()+' from prime not understood')

    # run
    cmd = '%iRUN\x0D'%pump
    ser.write(cmd.encode())
    output = ser.readline().decode()
    if '?' in output: print(cmd.strip()+' from prime not understood')


def run_pump(ser, pump):
    cmd = '%iRUN\x0D'%pump
    ser.write(cmd.encode())
    output = ser.readline().decode()
    if '?' in output:
        print(cmd.strip()+' from run not understood')
        return -1
    else:
        return 0

def set_vol(ser, pump, fvol):
    print(fvol)
    cmd_0 =  '%iVOLUL\x0D'%pump
    cmd = '%iVOL%s\x0D'%(pump,fvol)
    ser.write(cmd_0.encode())
    output = ser.readline().decode()
    ser.write(cmd.encode())
    output = ser.readline().decode()
    if '?' in output: print(cmd.strip()+' from set_vol not understood')
    print(cmd.strip())
    print("set_volume:", output)

def get_dis(ser, pump):
    cmd = '%iDIS\x0D'%pump
    ser.write(cmd.encode())
    output = ser.readline().decode()
    print(output)
    return output


def cld_dis(ser,pump):    # next:
    cmd = 'CLD\x0D'
    ser.write(cmd.encode())
    output = ser.readline().decode()
    if '?' in output: print(cmd.strip()+' from cld_dis not understood')
    print('Dispensed volume cleared.')

