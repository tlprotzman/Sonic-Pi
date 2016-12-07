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

'''LIST OF SYNTHS TO USE'''
BACKGROUNDSYNTHS = [
		  GROWL,
		  TRI,
		  PIANO,
		  SUBPULSE]

'''INITIALIZERS'''
def initizalizeChords():
	data = weather.getData()										#Gets the needed weather and time data
	print(data)
	progression = random.randint(0, len(CHORDPROGRESSIONS)-4)		#Selects a random major chord progression
	if random.randint(0, int(data[1])) > 10:						#Switches to a minor chord progression on random chance
		print('MINOR')													#and expected rain over next five days
		progression += 3
	CHORDS =  CHORDPROGRESSIONS[progression]						#Sets the progression to be used
	KEY = A3														#Sets the key to be used
	BPM = ((data[0] + 23) * 2.4) + 45								#Sets the tempo of the piece, mapping -10 to 43 Celsius to 60 to 200 BMP
	amplitude = -1 * (data[2]**2 / 192) + (data[2] / 8) + 0.25		#Maps the amplitude to the time of day, with noon being loudest
	print(BPM) 
	print(amplitude)
	return (CHORDS, KEY, 60 / BPM, amplitude)


def initializeAccompaniment():										#Sets up the accompaniment to be used
	mainBackNotes = []
	lastBackNotes = []												#The notes are different for the last chord in the progression
	possibleNotes = [1, 3, 5]										#Plays either a first, third or fifth of the scale
	n1 = random.randint(1, 4)										#Determine how many notes to play per measure, between 1 (whole note)
	n2 = random.randint(1, 4)											#and 4 (quarter note)
	for i in range(n1):
		mainBackNotes.append( possibleNotes[random.randint(0, 2)] )
	for i in range(n2):
		lastBackNotes.append( possibleNotes[random.randint(0, 2)] )
	return [mainBackNotes, lastBackNotes]

def initializeMelody():
	MELODY = []														#list of one measure sequences
	numBars = random.randint(2, 4)*len(CHORDS)						#Number of such sequences to exist
	for i in range(numBars):
		if i > 1 and i < numBars-2 and random.randint(1,2)==1:		#Sometimes, repeat the last two bars
			MELODY.append(MELODY[len(MELODY)-2])
			MELODY.append(MELODY[len(MELODY)-2])
			i = i + 2
		elif random.randint(1,3)==1:								#Sometimes, play the tonic for an entire measure
			MELODY.append([1])
		else:														#Otherwise, create a random phrase of random length
			line = []				
			n = random.randint(3, 4)
			for j in range(n):
				line.append( random.randint(1, 7) )
			MELODY.append(line)
	return MELODY

def initializeSynths():												#Determine which synths to use, and output them
	bassLineSynth = random.randint(0, len(BACKGROUNDSYNTHS) - 1)
	print("bassline synth:", bassLineSynth)
	backgroundSynth = random.randint(0, len(BACKGROUNDSYNTHS)) - 1
	print("background synth:", backgroundSynth)
	return (bassLineSynth, backgroundSynth)
	
'''PLAY NOTE/CHORD METHODS'''
def playChord(i, synth):											#Play the ith chord in the progression
	'''
	Takes a note and a synth, and plays it
	'''
	use_synth(synth)
	play(chord(KEY+INTERVALS[CHORDS[i][1]][CHORDS[i][0]], CHORDS[i][1]), sustain = BPM/2,amp = amplitude)
	
def playNote(note, interval, synth, octave = 0):					#Plays a note based on the base and interval
	use_synth(synth)
	baseNote =  CHORDS[note][0]
	chordType = CHORDS[note][1]
	actualInterval = 1
	if interval > 0:												#Modulus allows for octave wrapping
		actualInterval = interval%8 + interval//8
	elif interval < 0:												#Negative intervals
		actualInterval = 8 - interval%8 - interval//8
	if actualInterval > 8:											#Safety to prevent crashing with invalid intervals
		actualInterval = 8
	play ( KEY + INTERVALS[chordType][baseNote] + INTERVALS[chordType][actualInterval] + octave*12 + 12*(interval//8), amp = amplitude)
	
def bassLine():														#Plays chords  in the progression
	for i in range(len(CHORDS)):
		playChord(i, BACKGROUNDSYNTHS[bassLineSynth])
		sleep(BPM)

def playAccompaniment():											#Plays the pre-initialized accompaniment
	for i in range(len(CHORDS)):
		backNotes = mainBackNotes
		if i == len(CHORDS)-1:
			backNotes = lastBackNotes
		for j in range(len(backNotes)):
			playNote(i, backNotes[j], BACKGROUNDSYNTHS[backgroundSynth])
			sleep(BPM/len(backNotes))

def playMelody():													#Play the pre-initialized melody
	for i in range(len(MELODY)):
		for j in range(len(MELODY[i])):
			playNote(i%(len(CHORDS)), MELODY[i][j], TRI)
			sleep(BPM/len(MELODY[i]))
			
def drumLoop():														#Selects a random drum loop to play
	if whichDrumLoop == 0:	
		for i in range(len(CHORDS)):
			sample(DRUM_HEAVY_KICK, amp = amplitude-.2) 			# Beats 1 and 3
			sleep(BPM/2)
			sample(DRUM_SNARE_HARD, amp = amplitude-.2)				# Beats 2 and 4
			sleep(BPM/2)
	elif whichDrumLoop == 1:
		for i in range(len(CHORDS)):
			sample(DRUM_CYMBAL_CLOSED, amp = amplitude-.2)
			sample(DRUM_HEAVY_KICK, amp = amplitude-.2)
			sleep(BPM / 4)
			sample(DRUM_CYMBAL_CLOSED, amp = amplitude-.3)
			sleep(BPM / 4)
			sample(DRUM_CYMBAL_CLOSED, amp = amplitude-.3)
			sample(DRUM_SNARE_HARD, amp = amplitude-.2)
			sleep(BPM / 4)
			sample(DRUM_CYMBAL_CLOSED, amp = amplitude-.3)
			sleep(BPM / 4)
	elif whichDrumLoop == 2:
		for i in range(len(CHORDS)):
			sample(DRUM_HEAVY_KICK, amp = amplitude-.2)
			sleep(BPM/2)
			sample(DRUM_CYMBAL_HARD, amp = amplitude-.3)
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
backgroundInfo = initializeAccompaniment()
mainBackNotes = backgroundInfo[0]
lastBackNotes = backgroundInfo[1]

'''INITIALIZE DRUMS'''
whichDrumLoop = random.randint(0, 2)

'''INITIALIZE MELODY'''
MELODY = initializeMelody()

'''INITIALIZE THREADS'''
scale_thread = [ Thread(target=playScale) ]
background_thread = [ Thread(target=playAccompaniment) ]
bassLine_thread = [ Thread(target=bassLine) ]
drum_thread = [ Thread(target=drumLoop) ]
melody_thread = [ Thread(target=playMelody) ]

'''SONG MANAGER'''

def songManager():
	measures = 0
	melodyPlays = 0
	
	while True:

		#background
		if measures>1:
			background_thread.append( Thread(target=playAccompaniment) )
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
			
		#melody
		if measures%(len(CHORDS))==0 and melodyPlays > 0:
			melody_thread.append( Thread(target=playMelody) )
			melody_thread[-1].start()
		
		sleep(BPM*len(CHORDS))
		
songManager()