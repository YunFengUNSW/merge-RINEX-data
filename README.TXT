Required Environment:
	Python3+, code is tested pass under Python3.7
		please pre-install the lib: pip, urllib, gzip

		install tips: install the tool 'pip' from https://pypi.python.org/pypi/pip
			then use command:
			      	pip -install urllib
		              	pip -install gzip

	teqc: please download any version that suits your computing environment from https://www.unavco.org/software/data-processing/teqc/teqc.html

	      set up your environment of teqc

Basic functions:
	Download RINEX files based on the input time range, merges all the data inside this range through 'teqc', results are saved in one single 
	file whose name is automatically generated or by user input. downloaded files are inside the time range hourly unless data is already 
	merged by day at server side. To assign the name of the final results of that single file, command is like:

		python grab_data.py pbch 2017-03-24T23:11:22Z 2017-03-27T01:33:44Z RESULT_NAME

	i.e. appende one more string at the end of command

	Downloaded files are at .bz compressed format and program will uncompress them automotically and delete all the temp files when finishes


example command:

   normal:
	python grab_data.py pbch 2017-03-24T23:11:22Z 2017-03-27T01:33:44Z

		tips: if you are using linux system which has both Python2.7 and Python3.7, please use the 
		      command python3 grab_data.py pbch 2017-03-24T23:11:22Z 2017-03-27T01:33:44Z

   assign the name of result file:

	python grab_data.py pbch 2017-03-24T23:11:22Z 2017-03-27T01:33:44Z EXAMPLE_NAME.OBJ

		tips: if you are using linux system which has both Python2.7 and Python3.7, please use the command python3 grab_data.py pbch 2017-03-24T23:11:22Z 2017-03-27T01:33:44Z

   with error of reversed start_time and end_time: (system will try to use lower time as the start time instead)

	python grab_data.py pbch 2017-03-27T23:11:22Z 2017-03-24T01:33:44Z


Rubustable error:
	1. invalid time format
	2. insufficient inputs


Good Luck!

-----------------------Yun FENG-----------------------------
----------------yunfeng.unsw@gmail.com---------------------
----------------------0423472617---------------------------

