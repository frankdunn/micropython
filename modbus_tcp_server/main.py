
import modfunctions as m
from machine import Timer
#timer_disable = False
timer_disable = True
tim = Timer(-1)

def func(t):
    m.holdings[8] = m.holdings[8] + 1
    print ("timer_func")
    
tim.init(period=1000, mode=Timer.PERIODIC, callback=func)

m.mod_main()








    
    



	

	
	
   	
	 



