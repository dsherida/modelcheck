############################################################
# 					CSE 355, Fainekos					   #
# 					 Optional Project					   #
# 				Filename	: modelcheck.py 			   #
#				Author		: Doug Sheridan 			   #
#				Time spent	: 				 			   #
############################################################
# Version : Milestone I 		 						   #
############################################################

import os, sys, copy

############################################################
# 					Specify the input file 				   #
############################################################
script_dir = os.path.dirname(__file__)

##################### STRING INFO ##########################
depth = 1
string_n = ""

##################### TEST SELECTOR ########################
tNum = 1
##################### TEST PATHS ###########################
if tNum == 1:
	rel_path = "project_files(1)/exmp01_pt40.txt"
if tNum == 2:
	rel_path = "project_files(1)/exmp01_pt60.txt"
if tNum == 3:
	rel_path = "project_files(1)/exmp01_pt80.txt"
if tNum == 4:
	rel_path = "project_files(1)/exmp01_pt100.txt"
############################################################

abs_file_path 	= os.path.join(script_dir, rel_path)
f 				= open(abs_file_path, 'r')

############################################################
# 			Section header string constants 			   #
############################################################
Alphabet 				= '%Alphabet'
SpecificationAutomaton 	= '%Specificationautomaton'
InitialState 			= '%Initialstate'
FinalStates 			= '%Finalstates'
SystemAutomaton 		= '%Systemautomaton'

############################################################
# 				Global variables and structures 		   #
############################################################
ALPHABET 	= []
SPEC_RULES 	= []
MODEL_RULES = []

SpecificationTransitions 	= []
spec_init					= []
spec_final 					= []
spec_nodes					= []

ModelTransitions	= []
model_init 			= []
model_final			= []
model_nodes			= []

nextLine = ""

class Node(object):
	def __init__(self):
		self.name 		 = None
		self.initial 	 = None
		self.final 		 = None		
		self.next_states = {}

	def create_node(self, name, initial, final, transitions):
		self.name 		 	= name
		self.initial 		= initial
		self.final 			= final
		self.next_states 	= transitions

	def add_transition(self, obj):
		self.next_states.append(obj)

spec_tree = Node()

############################################################
#					 Main Functions 					   #
############################################################
def main():
	parse_inputFile()

############################################################
# 					Support Functions 					   #
############################################################
def parse_inputFile():
	# Get the alphabet
	parse_alphabet()

	# Create rules for the Specification Automaton
	parse_specifcationAutomaton()
	parse_rules(SPEC_RULES)
	print_rules(SpecificationTransitions)
	parse_init_final()

	# Create rules for the Model Automaton
	'''
	
	'''

	# Create the nodes with which to build the parse tree
	build_nodes(SpecificationTransitions)
	
	# Create a simple parse tree
	build_tree(spec_nodes)
	
	# Get one string in the language
	root = spec_init[0]
	root = find_node(spec_nodes, root)
	string = get_string(root)
	print "First string found: " + string

def parse_alphabet():
	# Read the next line
	global nextLine
	nextLine = f.readline()
	nextLine = ''.join(nextLine.split())

	# Check next token for expected value: Alphabet
	if nextLine == Alphabet:
		#print "Building alphabet..."

		# Parse until SpecificationAutomaton token is found
		nextLine = f.readline()
		nextLine = ''.join(nextLine.split())
		while nextLine != SpecificationAutomaton:
			ALPHABET.append(nextLine)
			nextLine = f.readline()
			nextLine = ''.join(nextLine.split())
		#print ALPHABET
	else:
		print "Syntax error, Alphabet section expected."
		sys.exit(0)


def parse_specifcationAutomaton():
	global nextLine

	# Check next token for expected value: Alphabet
	if nextLine == SpecificationAutomaton:
		#print "Building specification automaton..."

		# Parse until SpecificationAutomaton token is found
		nextLine = f.readline()
		nextLine = ''.join(nextLine.split())
		while nextLine != InitialState:
			SPEC_RULES.append(nextLine)
			nextLine = f.readline()
			nextLine = ''.join(nextLine.split())
		#print SPEC_RULES
	else:
		print "Syntax error, Specification automaton section expected."
		sys.exit(0)


def parse_init_final():
	global nextLine
	
	# Check next token for expected value: Alphabet
	if nextLine == InitialState:
		#print "Getting initial and final state..."

		# Parse the line after InitialState token
		nextLine = f.readline()
		nextLine = ''.join(nextLine.split())

		spec_init.append(nextLine)

		# Parse the line after the initial state value
		nextLine = f.readline()
		nextLine = ''.join(nextLine.split())

		if nextLine == FinalStates:
			# Parse the line after FinalStates token
			nextLine = f.readline()
			nextLine = ''.join(nextLine.split())
			while (nextLine != SystemAutomaton) and (nextLine != ""):
				spec_final.append(nextLine)
				# Parse another line to check if there exists another final state
				nextLine = f.readline()
				nextLine = ''.join(nextLine.split())
		
		#print spec_init
		#print spec_final
	else:
		print "Syntax error, Initial state section expected."
		sys.exit(0)


def parse_rules(ruleList):	#todo: account for case where multiple rules follow an input transition
	global SpecificationTransitions

	#print "Building specification automaton transitions..."

	for rule in ruleList:
		if len(rule) > 1:
			# New transition:input found
			SpecificationTransitions.append("#")
			for char in rule:
				SpecificationTransitions.append(char)
		else:
			SpecificationTransitions.append(rule)
	

def print_rules(ruleList):
	start_state = 0
	input_symbol = ""

	print "#######################"
	print "#  Automaton grammar  #"
	print "#######################"

	# ---------------
	# Output example:
	# ---------------
	# 1 --a--> 6
	# 1 --b--> 2 ...
	i = 0
	while i != len(ruleList):
		if ruleList[i] == '#':
			i = i+1
			start_state = ruleList[i]
			i = i+1
			input_symbol = ruleList[i]
			i = i+1
			while True:
				try:
					while (ruleList[i] != "#"):
						print start_state + " --" + input_symbol + "--> " + ruleList[i]
						i = i+1
					break
				except IndexError:
					break
		else:
			i = i+1

	print "#######################"


def build_nodes(ruleList):
	global spec_nodes

	# Debug
	#print ruleList

	i = 0
	while i != len(ruleList):
		current_state = None
		input_symbol = ""
		next_states = []
		transitions = {}
		node = Node()
		found = False

		if ruleList[i] == '#':
			i = i+1
			current_state = ruleList[i]
			i = i+1
			input_symbol = ruleList[i]
			i = i+1
			while True:
				try:
					while (ruleList[i] != "#"):
						next_states.append(ruleList[i])
						i = i+1

					transitions = {input_symbol:next_states}
					
					if spec_nodes:
						found = find_node(spec_nodes, current_state)

					if found:
						found.next_states.update(transitions)
					else:
						node.create_node(current_state, 0, 0, transitions)
						spec_nodes.append(node)
					break
				except IndexError:
					transitions = {input_symbol:next_states}
					
					if spec_nodes:
						found = find_node(spec_nodes, current_state)

					if found:
						found.next_states.update(transitions)
					else:
						node.create_node(current_state, 0, 0, transitions)
						spec_nodes.append(node)
					break
		else:
			i = i+1

	# Debug
	# for e in spec_nodes:
	# 	print e.name + str(e.next_states)
			

def build_tree(nodeList):
	#-----------------------------------------------------------
	# Description:		Converts the next_states list into object 
	#					pointers that point to the node in which 
	#					the integer represents.
	#-----------------------------------------------------------
	for node in nodeList:
		for input_symbol in node.next_states:
			for i, transition in enumerate(node.next_states[input_symbol]):
				f = find_node(nodeList, transition)
				#print node.next_states[state][i]
				node.next_states[input_symbol][i] = f


def get_string(node):
	# -----------------------------------------------------------
	# Description:		Check the next_states list for a final state
	# Returns:			If found, return the input_symbol that got us there
	# 					If not found, return 0
	# -----------------------------------------------------------
	global string_n
	string_n = ""

	for input_symbol in node.next_states:
		for transition in node.next_states[input_symbol]:
			if is_final(transition.name):
				return input_symbol
	
	# A final state was not found
	for input_symbol in node.next_states:
		for transition in node.next_states[input_symbol]:
			if node.name != transition.name:
				string_n += input_symbol
				string_n += get_string(transition)
				return string_n


def is_final(state):
	for final in spec_final:
		# print state
		# print final
		if state == final:
			return True

	return False

			
def find_node(nodeList, name):
	#-----------------------------------------------------------
	# Description:		Checks nodeList for the input state.
	# Returns:			If found, returns the node that has
	#					the same name as the state we searched for.
	#					If not found, returns 0.
	#-----------------------------------------------------------
	for node in nodeList:
		if name == node.name:
			return node
	return False

############################################################
# 					Program calls 						   #
############################################################
main()
