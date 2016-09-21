This script processes .DA1 and .reg or .cnt files into a format for R. To run, put script in a directory containing:

	- Region file (.reg or .cnt)
	- Directory of .DA1 files (file names will be used as subject numbers/names)

The script works with Python 2 and Python 3. To run, open terminal and change directory to the folder containing the script and files. Type the following command to run:

	python eyeTracking.py

The terminal will prompt you to enter information needed to run the script. Everything should be entered as it appears in the file directory, without quotes.

	1. Region file name
	2. DA1 file directory
	3. Output file name (file results will be written to)
	4. Low cutoff
	5. High cutoff

Next, it will ask what the format of the region file is. There are two existing options, .cnt and .reg. Enter the one that matches the format of your region file, or enter if none match. The two formats are as follows:

	.cnt: Item, Condition, Number of Regions, List of Region Boundaries
	.reg: Condition, Item, Number of Regions, List of Region Boundaries

If neither of these match, you will be prompted to manually enter the location of the item, condition, and number of region fields. The first position in the list is 0. It will also ask if the region file uses x,y coordinates. Enter yes if it does, or no if it only uses x coordinates.

Finally, the script will ask for the format of the DA1 files. There are two existing options. If neither of these options apply, hit enter, and the script will prompt you to enter the positions of each field. The two options are (x is an irrelevant field):

	1: Index, Condition, Item, Time, x, x, x, Number of Fixations, Start of Fixations
	2: Index, Condition, Item, Time, x, Number of Fixations, Start of Fixations

The script will process the DA1 files in the directory and output a file with the following measures:

	ff: First Fixation
	fp: First Pass
	rp: Regression Path
	pr: Percent Regression
	rr: Reread Time
	tt: Total Time

The output file has these columns:
	
	Subject - from DA1 file name
	Condition
	Item
	Value - numerical value of measure
	Region number
	X Start - x position of first character in region
	X End - x position of last character in region
	Y Start - y position of first character in region
	Y End - y position of first character in region
	Fixation Type - 2 letter code for measure
	Order - Index from DA1 file
	questionRT
	questionAcc
