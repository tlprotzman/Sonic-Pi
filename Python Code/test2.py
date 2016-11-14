import random
from psonic import *
from threading import Thread

key =  [C4,    A3,    F3,    G3]
type = [MAJOR, MINOR, MAJOR, MAJOR]
notes = [E4, C4, 
		 C4, A3,
		 A3, F3,
		 D4, G4]

bpm = 80
bpm = 60 / bpm


def bassLine():
	while True:
		for i in range(4):
			play(chord(key[i], type[i]), sustain=1.5)
			sleep(2)
		
def melody():
	while True:
		for i in range(4):
			for j in range(2):
				play(notes[i*2-1])
				sleep(0.5)
				play(notes[i*2])
				sleep(0.5)
def mainLine():
	note = 60
	while True:
		for i in range(2):
			use_synth(PROPHET)
			play(note, attack = .1, release = random.random() * .2 + .2)
			sleep(bpm)
		note = pickNote(note)

def pickNote(note):
	# print(note)
	maxNote = 90
	minNote = 50
	randomInterval = random.randint(1,3) 
	direction = random.randint(1, 2)
	if note >= maxNote:
		direction = 2
	elif note <= minNote:
		direction = 1
	# print(direction)
	if randomInterval == 2:
		if direction == 1:
			note += 4
		else:
			note -= 4
	elif randomInterval == 3:
		if direction == 1:
			note += 7
		else:
			note -= 7
	return note

def drumLoop():
	while True:
		print(currentBeat)
		sample(DRUM_HEAVY_KICK)
		sleep(bpm)
	# while True:
	# 	sample(LOOP_AMEN)
	# 	sleep(0.877)

def trackBeat():
	beatsPerMeasure = 4
	while True:
		print(currentBeat)
		sleep(bpm)
		if currentBeat < beatsPerMeasure:
			currentBeat += 1
		else:
			currentBeat = 1
	

currentBeat = 1

melody_thread = Thread(target=melody)
bassLine_thread = Thread(target=bassLine)
mainLine_thread = Thread(target=mainLine)
mainLine_thread2 = Thread(target=mainLine)
drum_thread = Thread(target=drumLoop)
beat_thread = Thread(target = trackBeat)




beat_thread.start()
# melody_thread.start()
# bassLine_thread.start()
mainLine_thread.start()
# mainLine_thread2.start()
drum_thread.start()



