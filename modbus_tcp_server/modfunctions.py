slave_id = 17
rx_data = []

holdings = [0,0,0,0,0,0,0,0,0,0]

def split_int(x):
        y1 = bytes([x & 0xFF])
        y2 = bytes([(x >> 8) & 0xFF])
        return y1,y2

def join_bytes(y2,y1):
		return((y2<<8) + y1)
		
		
def assemble_header(rx_data,tx_data):
        return (rx_data[0:5] + bytes([len(tx_data)])) #6: assemble header
        
def func_01(rx_data):
        
        tx_data = []
        tx_data = (bytes([slave_id]) + b'\x01' + b'\x05' + b'\xcd' + b'\x6b'+ b'\xb2'+ b'\x0e' + b'\x1b' )
        tx_header = (rx_data[0:5] + bytes([len(tx_data)]))
        return ( tx_header + tx_data )
        
def func_03(rx_data):
        start_holding = rx_data[9]
        number_holdings = rx_data[11]
        end_holding = start_holding + number_holdings
        tx_data = []                                            #1: check for errors &clear tx data
        tx_data = (bytes([slave_id])+ b'\x03')                  #2: add slave id + function code
        tx_data = (tx_data + bytes([number_holdings*2]))        #3: add number of bytes to follow
        for i in range(start_holding,end_holding):              #5: add requested holding registers
                y1,y2 = split_int(holdings[i])
                tx_data = (tx_data + y2 + y1 )
        return ( (assemble_header(rx_data,tx_data)) + tx_data ) #7: assemble msg
                

def func_06(rx_data):
		to_write = join_bytes(rx_data[8],rx_data[9])
		val_to_write = join_bytes(rx_data[10],rx_data[11])  
		tx_data = []                                            #1: check for errors &clear tx data
		tx_data = (bytes([slave_id])+ b'\x06')                  #2: add slave id + function code
		tx_data = (tx_data + bytes(rx_data[8:12]))              #3: add rest of tx_frame
		holdings[to_write] = val_to_write                       #4: write value to register
		return ( (assemble_header(rx_data,tx_data)) + tx_data ) #7: assemble msg


def chk_func_code(rx_data):
	#holdings[0] = loop_counter
	holdings[1] = holdings[1] + 10
	holdings[2] = holdings[2] + 3
	
	if slave_id == rx_data[6]:
		if rx_data[7] == 1:
			return(func_01(rx_data))

		elif rx_data[7] == 3:
			return(func_03(rx_data))
			
		elif rx_data[7] == 6:
			return(func_06(rx_data))

def mod_main():
        import usocket as socket
        addr = socket.getaddrinfo('0.0.0.0', 502)[0][-1]

        s = socket.socket()
        s.bind(addr)
        s.listen(2)
        s.settimeout(300)

        print('listening on', addr)
        is_connected = False

        loop_counter = 0
        while True:
            loop_counter = loop_counter + 1
            #holdings[0] = loop_counter
            holdings[1] = holdings[1] + 10
            holdings[2] = holdings[2] + 3
            print("loop counter :" + str(loop_counter))
            
            if not is_connected:   
                cl, addr = s.accept()
                is_connected = True
                
            print('client connected from', addr)
            #print("receiving")
            try:
                    rx_data = cl.recv(300)
                    if rx_data == []:
                            cl.close()
                            is_connected = False

            except:
                    cl.close()
                    print("closed")
                    is_connected = False
                    
            print("rx full frame :"+str(rx_data))
            
            try:
                if slave_id == rx_data[6]:
                        if rx_data[7] == 1:
                           cl.send(func_01(rx_data))
                   
                
                        elif rx_data[7] == 3:
                             cl.send(func_03(rx_data))

                        elif rx_data[7] == 6:
                             cl.send(func_06(rx_data))    

                        
                        

            except:
                cl.close()
                is_connected = False
             
    
		
