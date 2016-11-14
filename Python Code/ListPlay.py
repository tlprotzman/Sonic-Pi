from psonic import *


def createList(length):
	num = [1, 1]
	while len(num) < length:
		index = len(num)
		print(len(num))
		num.append(num[index - 1] + num[index - 2])
	return num


notes = createList(12)
print(notes)

for i in notes:
	play(i)
	print(i)
	sleep(1)