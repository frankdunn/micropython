
import modfunctions as m
import machine
from  machine import Timer

tim = Timer(-1)
p0 = machine.Pin(2, machine.Pin.IN)     # create input pin on D4 on nodeMcu


def func(t):
    m.holdings[8] = m.holdings[8] + 1
    print ("timer_func")
    print(p0.value())       # get value, 0 or 1
    m.holdings[5] = p0.value()
    
tim.init(period=100, mode=Timer.PERIODIC, callback=func)

m.mod_main()








    
    



	

	
	
   	
	 



