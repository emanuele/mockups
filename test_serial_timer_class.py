import time
from serial_timer import SerialTimer
from fake_serial import Serial
from time import sleep
# import sys


def mytime():
    return time.time() * 1000.0


if __name__ == '__main__':

    verbose = True
    
    # f = open('log.txt', 'w')
    # sys.stdout = f

    ser = Serial(values=['1','2','5','5','5','5','5','5','5','5'], timeout=2.0, seed=1, verbose=verbose)
    ser.open()

    print("Parent: Creating SerialTimer.")
    st = SerialTimer(t0=mytime(), ser=ser, time=mytime, good=['1','2'], bad=['5'], total_time=2000.0, flush=True, verbose=verbose)

    print("Condition 1")
    print("")

    for i in range(10):
        print("Parent: iteration %d" % i)
        st.start_timer()
        print("Parent: waiting some seconds.")
        sleep(4)
        key, elapsed_time = st.get_timing()
        print("Key pressed: %s , after %sms." % (key, elapsed_time))
        print("")

    time.sleep(2)

    print("Condition 2")
    print("")

    for i in range(10):
        print("Parent: iteration %d" % i)
        st.start_timer()
        print("Parent: waiting some seconds.")
        sleep(4)
        key, elapsed_time = st.get_timing()
        print("Key pressed: %s , after %sms." % (key, elapsed_time))
        print("")

    
    st.stop()
    
