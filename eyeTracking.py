"""
Author: Amanda Doucette
April 25, 2016
Edited: September 21, 2016
"""

try: input = raw_input
except NameError: pass

class region:
	"""
	Class for storing region data
	"""

	def __init__(self, x1, y1, x2, y2, regNum):
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2
		self.regNum = regNum

	def getRegNum(self):
		return self.regNum

class itemSummary:
	"""
	Class used for regionSummary objects
	Creates an object for one line in file. Takes line as array, 
	index of condition, item, and count of regions, and True/False
	if file contains Y coordinates.
	"""

	def __init__(self,line,conditionField,itemField,countField,hasY):
		self.item = int(line[itemField])
		self.condition = int(line[conditionField])
		self.count = int(line[countField])
		self.boundaries = [line[x] for x in range(len(line)) if x not in {conditionField,itemField,countField}]
		tmp = []
		if hasY:
			ctr = 1
			for a in range(0,len(self.boundaries)-2,2): #split array into tuples
				tmp.append(region(self.boundaries[a],self.boundaries[a+1],self.boundaries[a+2],self.boundaries[a+3],ctr))
				ctr = ctr+1
		else:
			tmp =  [region(self.boundaries[z],0,self.boundaries[z+1],0,z+1) for z in range(len(self.boundaries)-1)] #insert 0s for y coordinates
		self.boundaries = tmp

	def getItem(self):
		# returns item number
		return self.item

	def getCondition(self):
		# returns condition number
		return self.condition

	def getNumRegions(self):
		# returns number of regions
		return self.count

	def getBoundaries(self):
		# returns list of regions
		return self.boundaries

class regionSummary:
	"""
	Summary of regions for entire input file. Takes filename, index of condition, item, and count,
	and True/False if file contains y coordinates as arguments.
	"""
	def __init__(self, filename, conditionField, itemField, countField, hasY):
		f = open(filename, 'r')
		lines = []
		self.data = {}
		for line in f:
			if line != "":
				line = line.rstrip()
				line = line.split()
				line = [int(x) for x in line]
				lines.append(line)
		for x in lines:		# create list of itemSummary objects from file
			i = x[itemField]
			c = x[conditionField]
			if c not in self.data:
				self.data[int(c)] = {}
			self.data[c][i] = itemSummary(x,conditionField,itemField,countField,hasY)

	def getBoundaryList(self, condition, item):
		# returns list of regions
		return self.data[condition][item].getBoundaries()

	def labelRegion(self, condition, item, xIndex, yIndex=0):
		# returns the region of a character, first region=1
		boundaries = self.data[condition][item].getBoundaries()
		if (boundaries[-1].x2 <= xIndex and boundaries[-1].y2 is yIndex) or boundaries[-1].y2 < yIndex: #character is outside of last boundary
			return boundaries[-1]
		for r in boundaries:
			if (r.x2 > xIndex and r.y2 is yIndex) or r.y2 > yIndex:
				return r

	def numRegions(self, condition, item):
		# returns the number of regions in an item
		return self.data[condition][item].getNumRegions()

	def getRegion(self, condition, item, regNumber):
		# returns a region by number, first region = 1
		regions = self.data[condition][item].getBoundaries()
		return regions[regNumber-1]

class fixationSummary:
	"""
	Summary of individual fixations: x, y, start time, end time, and duration
	"""

	def __init__(self, xPos, yPos, start, end):
		self.x = xPos
		self.y = yPos
		self.start = start
		self.end = end
		self.dur = end-start

	def getX(self):
		return self.x

	def getY(self):
		return self.y

	def getStart(self):
		return self.start

	def getEnd(self):
		return self.end
		
	def getDur(self):
		return self.dur

class trialSummary:
	"""
	Summary of individual trial: index, condition, item, total time of fixations, total number of fixations, and list of fixation objects
	"""

	def __init__(self, index, condition, item, totalTime, numFixations, fixationsList):
		self.index = index
		self.item = item
		self.condition = condition
		self.totalTime = totalTime
		self.numFixations = numFixations
		self.fixationsList = fixationsList

	def getIndex(self):
		return self.index

	def getItem(self):
		return self.item

	def getCondition(self):
		return self.condition

	def getTotalTime(self):
		return self.totalTime

	def getNumFixations(self):
		return self.numFixations

	def getFixations(self):
		return self.fixationsList


class da1Summary:
	"""
	Summary of entire DA1 file: dictionary of trials by condition and item. Enter list index of fields for different file formats.
	Current DA1 formats are either: index = 0, condition = 1, item = 2, time = 3, fixations = 7, fixationsStart = 8

		or: index = 0, condition = 1, item = 2, time = 3, fixations = 5, fixationsStart = 6
	"""

	def __init__(self, filename, indexField, conditionField, itemField, timeField, fixationsField, fixationsStart):

		f = open(filename, 'r')
		lines = []
		self.trials = {}
		self.allTrials = []
		# Split file into lines
		for line in f:
			if line != "":
				line = line.rstrip()
				line = line.split()
				line = [int(x) for x in line]
				lines.append(line)

		for x in lines:
			# Get fields from line
			idx = x[indexField]
			itm = x[itemField]
			cond = x[conditionField]
			time = x[timeField]
			numFix = x[fixationsField]
			if cond not in self.trials:
				self.trials[cond] = {}

			fixations = []
			for f in range(fixationsStart, len(x), 4):	#loop through fixation groups: (x, y, start, end)
				fix = fixationSummary(x[f], x[f+1], x[f+2], x[f+3])
				fixations = fixations + [fix]

			# Add trialSummary to dictionary
			self.trials[cond][itm] = trialSummary(idx, cond, itm, time, numFix, fixations)
			self.allTrials += [trialSummary(idx, cond, itm, time, numFix, fixations)]

	def getTrial(self, cond, item):
		return self.trials[cond][item]

	def getIndex(self, cond, item):
		return self.trials[cond][item].getIndex()

	def getTotalTime(self, cond, item):
		return self.trials[cond][item].getTotalTime()

	def getNumFixations(self, cond, item):
		return self.trials[cond][item].getNumFixations()

	def getFixations(self, cond, item):
		return self.trials[cond][item].getFixations()

	def getAll(self):
		return self.allTrials

	
def regionCheck(region, fixation):
	if fixation.getX() == -1:
		return 'ignore'
		print('fixation out of bounds: [' + fixation.getX() + fixation.getY() + fixation.getStart() + fixation.getEnd() + ']')
	else:
		if (region.x1 <= fixation.getX() and region.x2 > fixation.getX() and region.y2 is fixation.getY()) or (region.x1 <= fixation.getX() and region.y2 > fixation.getY()):
			return 'within'
		elif (region.x1 > fixation.getX() and region.y1 is fixation.getY()) or region.y1 > fixation.getY():
			return 'before'
		else:
			return 'after'

def getFirstFix(region, fixations, lowCutoff, highCutoff):
	fixTime = 'NA'
	for f in fixations:
		if f.getDur() > lowCutoff and f.getDur() < highCutoff:
			if regionCheck(region, f) == 'within':
				fixTime = f.getDur()
				break
			elif regionCheck(region, f) == 'after':
				break
	return fixTime

def getFirstPass(region, fixations, lowCutoff, highCutoff):
	time = 0
	for f in fixations:
		dur = f.getDur()
		if regionCheck(region, f) == 'within':
			if dur>lowCutoff and dur<highCutoff:
				time = time + dur
			elif dur >= highCutoff:
				time = 0
				break
		elif regionCheck(region,f) == 'after':
			break
		elif time > 0 and regionCheck(region,f) == 'before':
			break

	if time == 0:
		time = 'NA'

	return time

def getRegPath(region, fixations, lowCutoff, highCutoff):
	time = 0

	for f in fixations:
		dur = f.getDur()
		if dur>lowCutoff and dur<highCutoff:
			if regionCheck(region,f) == 'after':
				break
			elif regionCheck(region,f) == 'within' or time>0:
				time = time + dur

	if time == 0:
		time = 'NA'

	return time

def getTotalTime(region, fixations, lowCutoff, highCutoff):
	time = 0

	for f in fixations:
		dur = f.getDur()
		if dur>lowCutoff and dur<highCutoff:
			if regionCheck(region,f) == 'within':
				time = time + dur

	if time == 0:
		time = 'NA'

	return time

def getRereadTime(region, fixations, lowCutoff, highCutoff):
	first = getFirstPass(region, fixations, lowCutoff, highCutoff)
	if first == 'NA':
		reread = getTotalTime(region, fixations, lowCutoff, highCutoff)
	else:
		reread = getTotalTime(region, fixations, lowCutoff, highCutoff) - first

	return reread

def getPerReg(region, fixations, lowCutoff, highCutoff):
	visitreg = 0
	reg = 0

	for f in fixations:
		dur = f.getDur()
		if dur>lowCutoff and dur<highCutoff:
			if regionCheck(region,f) == 'after':
				break
			elif regionCheck(region,f) == 'within':
				visitreg = 1
			elif visitreg == 1 and regionCheck(region,f) == 'before':
				reg = 1
				break

	if visitreg == 0:
		reg = 'NA'

	return reg

"""
If adding additional measures, do it here. See getFirstFix, getFirstPass, 
getRegPath, getTotalTime, getRereadTime, and getPerReg for examples. The regionCheck
function is used to check if a fixation is in a particular region. It returns 'after',
'within', or 'before'. Information about individual fixations can be obtained from
functions in the fixationSummary class. To add measure to output file, add it to
loop at the end of this file.
"""


if __name__ == '__main__':

	import os, sys

	mainDir = os.getcwd()

	regFile = input("Enter region file name: ")
	data = input("Enter directory of DA1 files: ")
	out = input("Enter output file name: ")

	lowCutoff = int(input("Enter low cutoff: "))
	while lowCutoff < 0:
		print("Low cutoff must be greater than 0.")
		lowCutoff = int(input("Enter low cutoff: "))

	highCutoff = int(input("Enter high cutoff: "))
	while highCutoff < 0:
		print("High cutoff must be greater than zero.")
		highCutoff = int(input("Enter high cutoff: "))
	while highCutoff < lowCutoff:
		print("High cutoff must be greater than low cutoff.")
		highCutoff = int(input("Enter high cutoff: "))

	print("Default region files are .cnt and .reg. The default order of fields in these files is as follows:")
	print("")
	print(".reg: Item = 0, Condition = 1, Number of Regions = 2, Region Boundaries")
	print(".cnt: Condition = 0, Item = 1, Number of Regions = 2, Region Boundaries")
	print("")
	print("If you are using one of these file types, enter it here. If not, press enter.")
	fileType = input("File type: ")
	if fileType.lower() == ".reg" or fileType.lower() == "reg":
		condition = 1
		item =0
		count =2
		y = False
	elif fileType.lower() == ".cnt" or fileType.lower() == "cnt":
		condition =0
		item =1
		count =2
		y =True
	else:
		print("Enter positions of condition, item, and number of regions fields. The first field is 0.")
		condition = int(input("Enter position of condition field: "))
		item = int(input("Enter position of item field: "))
		count = int(input("Enter position of number of regions field: "))
		y = input("Does the file use x,y coordinates? Enter 'yes' or 'no': ")
		if y.lower() == 'yes':
			y = True
		elif y.lower() == 'no':
			y = False

	print("What is the format of the DA1 files? Enter 1 or 2 for the formats shown below, or press enter to enter another format.")
	print("")
	print("1: index = 0, condition = 1, item = 2, time = 3, fixations = 7, fixationsStart = 8")
	print("2: index = 0, condition = 1, item = 2, time = 3, fixations = 5, fixationsStart = 6")
	print("")
	format = input("Enter DA1 format: ")
	if format == '1':
		dindex = 0
		dcondition = 1
		ditem = 2
		dtime = 3
		dfixations = 7
		dfixationsStart = 8
	elif format == '2':
		dindex = 0
		dcondition = 1
		ditem = 2
		dtime = 3
		dfixations = 5
		dfixationsStart = 6
	else:
		print("Enter the position of each field in the DA1 files. The first field is at position 0.")
		dindex = int(input("Enter position of index field: "))
		dcondition = int(input("Enter position of condition field: "))
		ditem = int(input("Enter position of item field: "))
		dtime = int(input("Enter position of time field: "))
		dfixations = int(input("Enter position of fixations field: "))
		dfixationsStart = int(input("Enter position of fixations start: "))

	print("Processing region file.")
	print("")
	reg = regionSummary(regFile, condition, item, count, y)
	print("Processing DA1 files.")

	maindir = os.getcwd()
	da1dir = os.path.join(maindir, data)
	da1s = os.listdir(da1dir)

	outfile = open(out, 'w')
	outfile.write('subj\tcond\titem\tvalue\tregion\tXstart\tXend\tYstart\tYend\tfixationtype\torder\tquestionRT\tquestionAcc\n')

	for f in da1s:
		print("Processing ", f)
		if f[-3:].lower() != 'da1':
			print("Not a DA1 file: ", f)
		else:
			fname = f[:-4]
			da1 = da1Summary(os.path.join(da1dir, f), dindex, dcondition, ditem, dtime, dfixations, dfixationsStart)
			trials = da1.getAll()

			for t in trials:
				trial_regions = reg.getBoundaryList(t.getCondition(), t.getItem())
				for r in trial_regions:

					"""If adding additional measures, add a line calling the function here."""
					ff = getFirstFix(r, t.getFixations(), lowCutoff, highCutoff)
					fp = getFirstPass(r, t.getFixations(), lowCutoff, highCutoff)
					rp = getRegPath(r, t.getFixations(), lowCutoff, highCutoff)
					pr = getPerReg(r, t.getFixations(), lowCutoff, highCutoff)
					rr = getRereadTime(r, t.getFixations(), lowCutoff, highCutoff)
					tt = getTotalTime(r, t.getFixations(), lowCutoff, highCutoff)

					"""Add output line for additional measure here."""
					trialData = [[fname, t.getCondition(), t.getItem(), ff, r.getRegNum(), r.x1, r.x2, r.y1, r.y2, 'ff', t.getIndex(), 'NA', 'NA'],
					[fname, t.getCondition(), t.getItem(), fp, r.getRegNum(), r.x1, r.x2, r.y1, r.y2, 'fp', t.getIndex(), 'NA', 'NA'],
					[fname, t.getCondition(), t.getItem(), rp, r.getRegNum(), r.x1, r.x2, r.y1, r.y2, 'rp', t.getIndex(), 'NA', 'NA'],
					[fname, t.getCondition(), t.getItem(), pr, r.getRegNum(), r.x1, r.x2, r.y1, r.y2, 'pr', t.getIndex(), 'NA', 'NA'],
					[fname, t.getCondition(), t.getItem(), rr, r.getRegNum(), r.x1, r.x2, r.y1, r.y2, 'rr', t.getIndex(), 'NA', 'NA'],
					[fname, t.getCondition(), t.getItem(), tt, r.getRegNum(), r.x1, r.x2, r.y1, r.y2, 'tt', t.getIndex(), 'NA', 'NA']]

					for line in trialData:
						outfile.write('\t'.join(str(x) for x in line)+'\n')

	outfile.close()
