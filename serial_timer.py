def serial_timer(q_in, q_out, t0, ser, time, good=[1,2], bad=[5], total_time=2000.0, verbose=False):
    delta_t = time() - t0
    print("Child: started after %sms" % delta_t)
    while True:
        t0 = q_in.get(block=True, timeout=None)
        if t0 == 'stop':
            break

        timeout = total_time
        while True:
            ser.timeout = timeout / 1000.0 # serial port wants seconds
            inp = ser.read(1)
            if verbose: print("Child: serial read %s" % inp)
            if inp in bad:
                timeout = (total_time - (time() - t0))
                continue
            elif inp in good:
                t = time() - t0
                if verbose: print("Child: %s arrived from serial after %s" % (inp, t))
                q_out.put((inp, t), block=True, timeout=None)
                break
            elif inp == '':
                t = time() - t0
                print("Child timeout: nothing arrived from serial after %s" % t)
                q_out.put(('timeout', t), block=True, timeout=None)
                break
            else:
                print("Child: Something wrong happened.")
                raise Exception
    
