import random
from psonic import *
from threading import Thread



INTERVALS = {	MAJOR : {  1  :  0,
						   2  :  2,
						   3  :  4,
						   4  :  5,
						   5  :  7,
						   6  :  9,
						   7  :  11,
						   8  :  12},
						   
				MINOR : {  1  :  0,
						   2  :  2,
						   3  :  3,
						   4  :  5,
						   5  :  7,
						   6  :  8,
						   7  :  10, 
						   8  :  12}}





def initizalizeChords():
	CHORDS =  [[1,  MAJOR],
			   [2,	MAJOR],
			   [3,  MINOR],
			   [3,  MAJOR],
			   [5,  MAJOR],
			   [6,  MAJOR],
			   [7,  MAJOR],
			   [8,  MAJOR]]
	KEY = A4
	BPM = 80
	return (CHORDS, KEY, 60 / BPM)

def playChord(i):
	play(chord(KEY+INTERVALS[CHORDS[i][1]][CHORDS[i][0]], CHORDS[i][1]))
	
def playNote(note, interval, octave = 0):
	baseNote =  CHORDS[note][0]
	chordType = CHORDS[note][1]
	actualInterval = 1
	if interval > 0:
		actualInterval = interval%8 + interval//8
	elif interval < 0:
		actualInterval = 8 - interval%8 - interval//8
	if actualInterval > 8:
		actualInterval = 8
	play(KEY + INTERVALS[chordType][baseNote] + INTERVALS[chordType][actualInterval] + octave*12 + 12*(interval//8))

def playScale():
	while True:
		for i in range(0, -100, -1):
			playNote(1, i+1)
			sleep(BPM/2)
			
def bassLine():
	while True:
		for i in range(len(CHORDS)):
			playChord(i)
			sleep(BPM*2)

def melody():
	while True:
		for i in range(len(CHORDS)):
			for j in range(2):
				playNote(i, 3)
				sleep(BPM/2)
				playNote(i, 1)
				sleep(BPM/2)
				
def mainLine():
	note = 60
	while True:
		for i in range(2):
			play(note, attack = .1, release = random.random() * .2 + .2)
			sleep(BPM)
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
		sleep(BPM)
	# while True:
	# 	sample(LOOP_AMEN)
	# 	sleep(0.877)



keyInfo = initizalizeChords()
CHORDS = keyInfo[0]
KEY	= keyInfo[1]
BPM = keyInfo[2]
print(CHORDS, KEY)
scale_thread = Thread(target=playScale)
melody_thread = Thread(target=melody)
bassLine_thread = Thread(target=bassLine)
mainLine_thread = Thread(target=mainLine)
mainLine_thread2 = Thread(target=mainLine)
drum_thread = Thread(target=drumLoop)

# scale_thread.start()
melody_thread.start()
bassLine_thread.start()
# mainLine_thread.start()
# mainLine_thread2.start()
drum_thread.start()



