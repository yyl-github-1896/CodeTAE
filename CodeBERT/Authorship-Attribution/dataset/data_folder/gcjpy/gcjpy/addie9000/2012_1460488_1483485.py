#!/usr/bin/python
 import sys, string
 
 # make the googlerese dic
 gdic = {}
 sample_googlerese = "yqeeejpmysljylckdkxveddknmcrejsicpdrysirbcpcypcrtcsradkhwyfrepkymveddknkmkrkcddekrkdeoyakwaejtysrreujdrlkgcjv"
 sample_plain_text = "azooourlanguageisimpossibletounderstandtherearetwentysixfactorialpossibilitiessoitisokayifyouwanttojustgiveup"
 for gletter, pletter in zip(sample_googlerese, sample_plain_text):
 	if gletter in gdic:
 		if not gdic[gletter] == pletter:
 			print "ERROR!! Can't analyze the sample text."
 			sys.exit()
 	else:
 		gdic[gletter] = pletter
 
 if len(gdic) == 25:
 	candidate_gletter = set(string.ascii_lowercase) - set(sample_googlerese)
 	candidate_pletter = set(string.ascii_lowercase) - set(sample_plain_text)
 	if len(candidate_gletter) == 1 and len(candidate_pletter) == 1:
 		gdic[candidate_gletter.pop()] = candidate_pletter.pop()
 
 gdic[' '] = ' '
 
 # open the file
 r = sys.stdin
 
 if len(sys.argv) > 1:
 	r = open(sys.argv[1], 'r')
 
 # solve the cases 
 total_cases = r.readline()
 for case_number in range(1, int(total_cases) + 1):
 	googlerese_text = r.readline().rstrip()
 	plain_text = ""	
 	for gletter in googlerese_text:
 		plain_text = plain_text + gdic[gletter]
 
 	print "Case #%d: %s" % (case_number, plain_text)
