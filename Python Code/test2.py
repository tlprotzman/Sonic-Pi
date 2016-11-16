import random
from psonic import *
from threading import Thread

CHORDS =  [[1,  MAJOR],
		   [6,	MINOR],
		   [4,  MAJOR],
		   [5,  MAJOR]]

KEY = A3

INTERVALS = {	MAJOR : {  1  :  0,
						   2  :  2,
			     		   3  :  4,
						   4  :  5,
						   5  :  7,
						   6  :  9,
						   7  :  11  },
						   
				MINOR : {  1  :  0,
						   2  :  2,
					  	   3  :  3,
						   4  :  5,
						   5  :  7,
						   6  :  8,
						   7  :  10  }}

bpm = 80
bpm = 60 / bpm

def playChord(i):
	play(chord(chords[i][0], chords[i][1]))
	
def playNote(note, interval):
	baseNote =  CHORDS[note][0]
	chordType = CHORDS[note][1]
	play(KEY + INTERVALS[chordType][baseNote] + INTERVALS[chordType][interval])

def bassLine():
	while True:
		for i in range(4):
			playChord(i)
			sleep(bpm*2)

def melody():
	while True:
		for i in range(4):
			for j in range(2):
				playNote(i, 3)
				sleep(bpm/2)
				playNote(i, 1)
				sleep(bpm/2)
				
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
		# print(currentBeat)
		sample(DRUM_HEAVY_KICK)
		sleep(bpm)
	# while True:
	# 	sample(LOOP_AMEN)
	# 	sleep(0.877)

melody_thread = Thread(target=melody)
bassLine_thread = Thread(target=bassLine)
mainLine_thread = Thread(target=mainLine)
mainLine_thread2 = Thread(target=mainLine)
drum_thread = Thread(target=drumLoop)

melody_thread.start()
bassLine_thread.start()
# mainLine_thread.start()
# mainLine_thread2.start()
drum_thread.start()



