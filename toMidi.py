
# default set:
# X: repeat time
# T: title
# M: temple
# C: Author
# K: Major


# important: timeSignature-C(after key signiature)
import os


path = './primus_conversor/output.semantic'


# tempo_transform = {'eighth':1/8, 'sixteenth':1/16, 'thirty_second':}

class Converter:
	def __init__(self, basename):
		self.default_set = ['X:1', 'T:B&J\'s work', 'M:4/4', 'C:Powered by B&J', 'K:G']
		self.default_tone = ['C', 'Treble']
		self.save_dir = '../Output/'+basename
	def segToABC(self, segNotes):
		notes = []
		for seg in segNotes:
			# deal with note
			if seg[0:5]=="note-":
				note = ''
				if not seg[6].isdigit():
					# deal with note range
					segNum = int(seg[7])
					if segNum==4:
						note+= seg[5]
					elif segNum==5:
						note+=seg[5].lower()
					elif segNum>5:
						note+=seg[5].lower()
						note+= '\''*(segNum-5)
					elif segNum<4:
						note+= seg[5]
						note+= ','*(4-segNum)
					
					# deal with note accidental
					if seg[6] == '#':
						note+='^'
					elif seg[6] == '-':
						note+='_'

				else:
					segNum = int(seg[6])

					if segNum==4:
						note+= seg[5]
					elif segNum==5:
						note+=seg[5].lower()
					elif segNum>5:
						note+=seg[5].lower()
						note+= '\''*(segNum-5)
					elif segNum<4:
						note+= seg[5]
						note+= ','*(4-segNum)	
				notes.append(note)
				# tempo


			# deal with symbol

			# barline
			elif seg == 'barline':
				notes.append('|')

			elif seg[0:9] == 'multirest':
				notes.append('z'+seg[10])
			# clef
			elif seg[0:4] == 'clef':
				if seg[0:6] == 'clef-F':
					self.default_tone[1] = 'Bass'
				else:
					self.default_tone[1] = 'Treble'
				notes.append(self.default_tone[1])				
			# key
			elif seg[0:13] == 'keySignature-':
				tone = seg[13:len(seg)]
				if tone[len(tone)-1] == 'M':
					tone_array = list(tone)
					tone_array[len(tone)-1] = 'm'
					tone = ''
					for i in tone_array:
						tone+=i
				self.default_tone[0] = tone
				notes.append(self.default_tone[0])	
			else:
				notes.append('')	
		
		return notes

	def notesToMidi(self, array_of_notes):
		# timeSigniture =''
		# single_measure = []
		notes = ''
		space = False
		former_symbol=''
		tie_note = ''
		tie_req = False

		for line in array_of_notes:
			for note in line:
				# To avoid not enough rest
				# 4/4

				# if note == 'timeSignature-C':
				# 	timeSigniture = 'timeSignature-C'
				
				# if timeSigniture =='timeSignature-C':
				# 	if note[0:5] == 'note-':
				# 		single_measure.append(note)
				# 	elif note =='barline':
				# 		tempo_sum = 0
				# 		for former_note in single_measure:
				# 			tempo = ''
				# 			if not former_note[6].isdigit():
				# 				tempo = former_note[9:len(former_note)]
				# 			else:
				# 				tempo = former_note[8:len(former_note)]
				# 			# transfer to num
				# 			if tempo == 'eighth':
				# 				tempo_sum+=1/8
				# 			elif tempo == 'sixteenth':
				# 				tempo_sum+=1/16
				# 			elif tempo == 'thirty_second':
				# 				tempo_sum+=




				# To avoid mis recongnize double barline
				# if former_symbol == note == 'barline':
				# 	continue
				if note == 'barline':
					continue
				# if note =='tie':
				# 	tie_note== former_symbol
				# 	tie_req = True
				# elif tie_req == True:
				# 	note = tie_note
				# 	tie_req = False
				
				if space:
					notes= notes+' '+ note
				else:
					notes =notes+note
					space = True

				# if note != 'tie':
				# 	former_symbol = note
		print(notes)
		if os.path.exists(path):
			os.remove(path)
		f = open(path,'w')
		f.write(notes)
		f.close()
		
		os.chdir('./primus_conversor')
		cmd = "./semantic_conversor.sh output.semantic "+self.save_dir+"_output.mid"
		
		os.system(cmd)
		cmd = "./semantic_conversor.sh output.semantic output.mid"
		
		os.system(cmd)
		os.chdir('..')
# test_data=[['clef-G2', 'keySignature-DM', 'note-D6_quarter', 'note-B5_quarter', 'note-G#5_eighth.', 'note-F#5_eighth.', 'note-E5_eighth', 'barline', 'note-E5_quarter', 'rest-eighth', 'note-E5_quarter', 'note-F#5_eighth', 'note-G#5_eighth.', 'note-F#5_sixteenth', 'barline', 'rest-quarter', 'rest-eighth', 'note-B4_eighth', 'note-B4_quarter', 'note-C#5_quarter', 'barline', 'multirest-4', 'barline']]



# c = converter()
# c_datas = c.notesToMidi(test_data)



