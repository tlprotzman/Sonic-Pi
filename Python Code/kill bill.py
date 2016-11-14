from psonic import *
from threading import Thread

notes = [C5, D5, E5, D5, C5, D5, E5, D5, C5, D5, E5, D5, C5, D5]

def loopOne():
	while True:
		for i in range(len(notes)):
			play(notes[i])
			print(notes[i])
			sleep(0.25)

def bassDrum():
	while True:
		sample(BD_808)
		sleep(1)

loopThread = Thread(target = loopOne)
bassThread = Thread(target = bassDrum)

loopThread.start()
bassThread.start()

sleep (10)
loopThread.stop()
bassThread.stop()