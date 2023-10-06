file = open('general_data.txt', 'r', encoding='utf-8')
file1 = open('data_for_eyes.txt', 'w', encoding='utf-8')
line = file.read()
array = line.split('\n')
for i in array:
	print(i.split('@'))
	file1.write('\n' + str(i.split('@')))