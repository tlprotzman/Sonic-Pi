'''IMPORT NECESSARY LIBRARIES'''
import random
import math
import weather
from psonic import *
from threading import Thread

'''LIST OF CHORD PROGRESSIONS'''
CHORDPROGRESSIONS = [ [[1,  MAJOR],
					   [6,  MINOR],
					   [4,  MAJOR],
					   [5,  MAJOR]],

					  [[1,  MAJOR],
					   [4,  MAJOR],
					   [5,  MAJOR],
					   [4,  MAJOR]],

					  [[1, MAJOR],
					   [4, MAJOR],
					   [5, MAJOR],
					   [1, MAJOR]],

					  [[1, MINOR],
					   [7, MAJOR],
					   [6, MAJOR],
					   [1, MINOR]],

					  [[1, MINOR],
					   [4, MINOR],
					   [7, MAJOR],
					   [1, MINOR]],

					  [[1, MINOR],
					   [4, MINOR],
					   [5, MINOR],
					   [1, MINOR]],					 
					]
'''
					  [[1, MAJOR],
					   [2, MAJOR],
					   [3, MINOR],
					   [3, MAJOR],
					   [5, MAJOR],
					   [6, MINOR],
					   [7, MAJOR],
					   [8, MAJOR]],

					  [[1, MAJOR],
					   [4, MAJOR],
					   [2, MINOR],
					   [3, MINOR],
					   [4, MAJOR],
					   [1, MAJOR],
					   [2, MINOR],
					   [5, MAJOR]],
'''
'''LIST OF INTERVALS'''
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

BACKGROUNDSYNTHS = [
		  GROWL,
		 # PIANO,
		  TRI,
		  SUBPULSE]

'''
POSSIBLE SYNTHS
DTRI
GROWL
PIANO
PROPHET
'''

'''INITIALIZERS'''
def initizalizeChords():
	data = weather.getData()
	print(data)
	progression = random.randint(0, len(CHORDPROGRESSIONS)-4)
	if random.randint(0, int(data[1])) > 10:
		print('MINOR')
		progression += 3
	CHORDS =  CHORDPROGRESSIONS[progression]
	KEY = A3
	BPM = ((data[0] + 23) * 2.4) + 45
	amplitude = -1 * (data[2]**2 / 192) + (data[2] / 8) + 0.25
	print(BPM) 
	print(amplitude)
	return (CHORDS, KEY, 60 / BPM, amplitude)

def initializeBackground():
	mainBackNotes = []
	lastBackNotes = []
	possibleNotes = [1, 3, 5]
	n1 = random.randint(1, 4)
	n2 = random.randint(1, 4)
	for i in range(n1):
		mainBackNotes.append( possibleNotes[random.randint(0, 2)] )
	for i in range(n2):
		lastBackNotes.append( possibleNotes[random.randint(0, 2)] )
	return [mainBackNotes, lastBackNotes]
	
def initializeChorus():
	CHORUS = []
	numBars = random.randint(2, 4)*len(CHORDS)
	possibleNotes = [1, 3, 5]
	for i in range(numBars):
		if i > 1 and i < numBars-2 and random.randint(1,2)==1:
			CHORUS.append(CHORUS[len(CHORUS)-2])
			CHORUS.append(CHORUS[len(CHORUS)-2])
			i = i + 2
		elif random.randint(1,3)==1:
			CHORUS.append([1])
		else:
			line = []
			n = random.randint(3, 4)
			for j in range(n):
				line.append( random.randint(1, 7) )
			CHORUS.append(line)
	return CHORUS

def initializeSynths():
	bassLineSynth = random.randint(0, len(BACKGROUNDSYNTHS) - 1)
	print("bassline synth:", bassLineSynth)
	backgroundSynth = random.randint(0, len(BACKGROUNDSYNTHS)) - 1
	print("background synth:", backgroundSynth)
	return (bassLineSynth, backgroundSynth)
	
'''PLAY NOTE/CHORD METHODS'''
def playChord(i, synth):
	use_synth(synth)
	play(chord(KEY+INTERVALS[CHORDS[i][1]][CHORDS[i][0]], CHORDS[i][1]), sustain = BPM/2,amp = amplitude)
	
def playNote(note, interval, synth, octave = 0):
	use_synth(synth)
	baseNote =  CHORDS[note][0]
	chordType = CHORDS[note][1]
	actualInterval = 1
	if interval > 0:
		actualInterval = interval%8 + interval//8
	elif interval < 0:
		actualInterval = 8 - interval%8 - interval//8
	if actualInterval > 8:
		actualInterval = 8
	play ( KEY + INTERVALS[chordType][baseNote] + INTERVALS[chordType][actualInterval] + octave*12 + 12*(interval//8), amp = amplitude)
	
def playScale():
	for i in range(8):
		playNote(1, i+1)
		sleep(BPM/2)

'''THREADS'''
def bassLine():
	#while True:
	for i in range(len(CHORDS)):
		playChord(i, BACKGROUNDSYNTHS[bassLineSynth])
		sleep(BPM)

def background():
	#while True:
	for i in range(len(CHORDS)):
		backNotes = mainBackNotes
		if i == len(CHORDS)-1:
			backNotes = lastBackNotes
		for j in range(len(backNotes)):
			playNote(i, backNotes[j], BACKGROUNDSYNTHS[backgroundSynth])
			sleep(BPM/len(backNotes))

def playChorus():
	#while True:
	for i in range(len(CHORUS)):
		for j in range(len(CHORUS[i])):
			playNote(i%(len(CHORDS)), CHORUS[i][j], TRI)
			sleep(BPM/len(CHORUS[i]))

def mainLine():
	note = 60
	#while True:
	for i in range(2):
		play(note, attack = .1, release = random.random() * .2 + .2, amp = amplitude)
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
	if whichDrumLoop == 0:
		for i in range(len(CHORDS)):
			sample(DRUM_HEAVY_KICK, amp = amplitude)
			sleep(BPM/2)
			sample(DRUM_SNARE_HARD, amp = amplitude)
			sleep(BPM/2)
	elif whichDrumLoop == 1:
		for i in range(len(CHORDS)):
			sample(DRUM_CYMBAL_CLOSED, amp = amplitude)
			sample(DRUM_HEAVY_KICK, amp = amplitude)
			sleep(BPM / 4)
			sample(DRUM_CYMBAL_CLOSED, amp = amplitude)
			sleep(BPM / 4)
			sample(DRUM_CYMBAL_CLOSED, amp = amplitude)
			sample(DRUM_SNARE_HARD, amp = amplitude)
			sleep(BPM / 4)
			sample(DRUM_CYMBAL_CLOSED, amp = amplitude)
			sleep(BPM / 4)
	elif whichDrumLoop == 2:
		for i in range(len(CHORDS)):
			sample(DRUM_HEAVY_KICK, amp = amplitude)
			sleep(BPM/2)
			sample(DRUM_CYMBAL_HARD, amp = amplitude)
			sleep(BPM/2)


'''INITIALIZE CHORDS'''
keyInfo = initizalizeChords()
CHORDS = keyInfo[0]
KEY	= keyInfo[1]
BPM = keyInfo[2]
amplitude = keyInfo[3]
print(CHORDS, KEY)

'''INITIALIZE SYNTHS'''
allSynths = initializeSynths()
bassLineSynth = allSynths[0]
backgroundSynth = allSynths[1]

'''INITIALIZE BACKGROUNDS'''
backgroundInfo = initializeBackground()
mainBackNotes = backgroundInfo[0]
lastBackNotes = backgroundInfo[1]

'''INITIALIZE DRUMS'''
whichDrumLoop = random.randint(0, 2)

'''INITIALIZE CHORUS'''
CHORUS = initializeChorus()

'''INITIALIZE THREADS'''
scale_thread = [ Thread(target=playScale) ]
background_thread = [ Thread(target=background) ]
bassLine_thread = [ Thread(target=bassLine) ]
mainLine_thread = [ Thread(target=mainLine) ]
mainLine_thread2 = [ Thread(target=mainLine) ]
drum_thread = [ Thread(target=drumLoop) ]
chorus_thread = [ Thread(target=playChorus) ]

'''START THREADS'''

def songManager():
	measures = 0
	chorusPlays = 0
	
	while True:

		#background
		if measures>1:
			background_thread.append( Thread(target=background) )
			background_thread[-1].start()
		
		#bassline
		if measures>0:
			bassLine_thread.append( Thread(target=bassLine) )
			bassLine_thread[-1].start()
		
		#drums
		drum_thread.append( Thread(target=drumLoop) )
		drum_thread[-1].start()
		
		#measures
		measures += 1
		if measures%(len(CHORDS))==0:
			chorusPlays += 1
			
		#chorus
		if measures%(len(CHORDS))==0 and chorusPlays > 0:
			chorus_thread.append( Thread(target=playChorus) )
			chorus_thread[-1].start()
		
		sleep(BPM*len(CHORDS))
		
songManager()