from psonic import *

rest = 0.1
use_synth(FM)
for i in range(400, 1000,):
	play(i/10)
	#play(150 - i)
	sleep(rest)
	#print(i)
for i in range(1000, 400, -1):
	play(i/10)
	#play(150 - i)
	#print(i)
	sleep(rest)