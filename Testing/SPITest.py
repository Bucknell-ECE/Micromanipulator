## not used (7/5/18)

import spidev
import time
spi = spidev.SpiDev() # create spi object
spi.open(0, 1) # open spi port 0, device (CS) 1
try:
 while True:
 resp = spi.xfer2([0xAA]) # transfer one byte
 time.sleep(0.1) # sleep for 0.1 seconds
 #end while
except KeyboardInterrupt: # Ctrl+C pressed, so…
 spi.close() # … close the port before exit
#end try