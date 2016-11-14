from psonic import *

chords = [(chord(C4, MINOR), 'release = 0.2'), (chord(G3, MINOR), 'release = 0.2'), (chord(E4, DIM), 'release = 1')]

use_synth(FM)
for i in range(len(chords)):
	play(chords[i])
	sleep(0.5)