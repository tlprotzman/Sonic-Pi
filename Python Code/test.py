from psonic import *
import random

while True:
	notes = random.randint(1, 5)
	for i in range(notes):
		play(random.randint(30, 80))	
	time = random.randint(0,100) / 100
	sleep(time)