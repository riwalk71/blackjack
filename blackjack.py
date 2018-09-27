
#	Blackjack Expected Value and Basic Strategy Calculator
#	Written by Ricky Walker
#
#	Released under WTFPL version 2.
#	Full license and terms available here: http://www.wtfpl.net/
#


import sys
import numbers


#	Basic settings
#
DEALER_HIT_SOFT_17 = False

WIN_PAYOUT = 1.0
LOSS_PAYOUT = -1.0
PUSH_PAYOUT = 0.0
BLACKJACK_PAYOUT = 1.5


#	Probability of seeing a card at any given time. 
#
p = {
	"2": (4.0/52.0),
	"3": (4.0/52.0),
	"4": (4.0/52.0),
	"5": (4.0/52.0),
	"6": (4.0/52.0),
	"7": (4.0/52.0),
	"8": (4.0/52.0),
	"9": (4.0/52.0),
	"10": (16.0/52.0),
	"A": (4.0/52.0)
}


# 	All hands, in the order that they should be processed. By evaluating hands in this order,
#	we can never draw a card and not end up on a total that did not exist earlier in the list.
#
hands = [ 
	'H30', 'H29', 'H28', 'H27', 'H26', 'H25', 'H24', 'H23', 'H22', 'H21', 
	'H20', 'H19', 'H18', 'H17', 'H16', 'H15', 'H14', 'H13', 'H12', 'H11',
	'S21', 'H10', 'S20', 'H9',  'S19', 'H8',  'S18', 'H7',  'S17', 'H6', 
	'S16', 'H5',  'S15', 'H4',  'S14', 'H3',  'S13', 'H2',  'S12', 'S11' 
]

#	A print friendly ordering of the values above
#
allhands = [
	 'H2',  'H3',  'H4',  'H5',  'H6',  'H7',  'H8',  'H9', 'H10', 'H11',
	'H12', 'H13', 'H14', 'H15', 'H16', 'H17', 'H18', 'H19', 'H20', 'H21',
	'H22', 'H23', 'H24', 'H25', 'H26', 'H27', 'H28', 'H29', 'H30', 
	'S11', 'S12', 'S13', 'S14', 'S15', 'S16', 'S17', 'S18', 'S19', 'S20', 'S21' ]

	

#	A subset of the hands above, representing the player hands normally shown in a basic strategy chart.
#
phands = [ 'H8', 'H9', 'H10', 'H11', 'H12', 'H13', 'H14', 'H15', 'H16', 'H17', 'H18', 'H19', 'H20', 'H21',
	'S12', 'S13', 'S14', 'S15', 'S16', 'S17', 'S18', 'S19', 'S20', 'S21' ]


#	A subset of the hands above, representing the dealer hands normally shown in a basic strategy chart
#	
dhands = [ 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10', 'S11' ]


#	A list of splittable hands
#
splithands = [ '2,2', '3,3', '4,4', '5,5', '6,6', '7,7', '8,8', '9,9', '10,10', 'A,A' ]


#	A list of cards
#
cards = [ '2', '3', '4', '5', '6', '7', '8', '9', '10', 'A' ]


#	Create empty entries for all player/dealer hands in the provided table
#
def empty_table(table, player_hands, dealer_hands, init_val=-100000000):
	for player_hand in player_hands:
		table[player_hand] = {}
		for dealer_hand in dealer_hands:
			table[player_hand][dealer_hand] = init_val
	

#	Print a table in CSV format
#
def print_table_csv(table, rows, columns):
	print "---",
	for column in columns:
		print ", " + column,
	print ""
	for row in rows:
		print row,
		for column in columns:
			print ", " + str(table[row][column]),
		print ""
	print ""
	

#	Print a table in a console friendly format
#
def pretty_print_table(table, rows, columns, label_width, col_width):

	row_label_width = 0
	for row in rows:
		if len(row) > row_label_width:
			row_label_width = len(row)
			
	if row_label_width < label_width:
		row_label_width = label_width

	print_row_divider(row_label_width, len(columns), col_width)
	
	sys.stdout.write("| ")
	print_cell(" ", row_label_width)
	sys.stdout.write(" |")
	
	for column in columns:
		sys.stdout.write(" ")
		print_cell(column, col_width)
		sys.stdout.write(" |")
		
	print ""
		
	print_row_divider(row_label_width, len(columns), col_width)
	
	for row in rows:
	
		sys.stdout.write("| ")
		print_cell(str(row), row_label_width)
		sys.stdout.write(" |")
		
		for column in columns:
			sys.stdout.write(" ")
			if isinstance(table[row][column], numbers.Number):
				print_cell('%f' % table[row][column], col_width)
			else:
				print_cell(table[row][column], col_width)
			sys.stdout.write(" |")
			
		print ""
		
		print_row_divider(row_label_width, len(columns), col_width)
		
	print ""
	
	
def print_row_divider(row_label_width, column_count, col_width):
	sys.stdout.write("+")
	sys.stdout.write("-"*(row_label_width+2))
	sys.stdout.write("+")
	for i in range(column_count):
		sys.stdout.write("-"*(col_width+2))
		sys.stdout.write("+")
	print ""
	

def print_cell(val, width):
	if len(val) < width:
		sys.stdout.write(" " * (width - len(val)) + val)
	elif len(val) > width:
		sys.stdout.write(val[:width])
	else:
		sys.stdout.write(val)


#	Return whether or not a dealer is required to hit the given hand
#
def should_dealer_hit(dealer_hand):
	
	dealer_value = int(dealer_hand[1:])
		
	if dealer_value <= 16:
		return True
	if dealer_value >= 18:
		return False
	if dealer_hand == "H17":
		return False
	
	return DEALER_HIT_SOFT_17
	

#	Return the payout assuming the game ends with the provided dealer and player hands
#
def get_hand_payout(player_hand, player_card_count, dealer_hand, dealer_card_count):
	
	player_value = int(player_hand[1:])
	dealer_value = int(dealer_hand[1:])
	
	if player_value > 21:	
		return LOSS_PAYOUT
	
	if player_value == 21 and player_card_count == 2:
		if dealer_value == 21 and dealer_card_count == 2:
			return PUSH_PAYOUT
		else:
			return BLACKJACK_PAYOUT
			
	if dealer_value == 21 and dealer_card_count == 2:
		return LOSS_PAYOUT
		
	if dealer_value > 21:
		return WIN_PAYOUT
	
	if dealer_value == player_value:
		return PUSH_PAYOUT
		
	if dealer_value > player_value:
		return LOSS_PAYOUT
	
	return WIN_PAYOUT
	

#	Returns what hand a player/dealer has when the draw a card with "value" (excluding an Ace)
#
def add_value(hand, value):
	hand_type = hand[:1]
	if hand[:1] == "H":
		return "H" + str(int(hand[1:]) + value)
	elif hand_type == "S":
		if int(hand[1:]) + value > 21:
			return "H" + str(int(hand[1:]) + value - 10)
		else:
			return "S" + str(int(hand[1:]) + value)
	else:
		if hand == str(value):
			return hand + "," + str(value)
		elif hand == "A":
			return add_value("S11", value)
		else:
			return add_value("H" + str(hand), value)
			
			

#	Returns what hand a player/dealer has when they draw an Ace
#
def add_ace(hand):
	hand_type = hand[:1]
	if hand_type == "H":
		if int(hand[1:]) + 11 <= 21:
			return "S" + str(int(hand[1:]) + 11)
		else:
			return "H" + str(int(hand[1:]) + 1)
	elif hand_type == "S":
		if int(hand[1:]) == 21:
			return "H12"
		else:
			return "S" + str(int(hand[1:]) + 1)
	else:
		if hand == "A":
			return "A,A"
		else:
			return add_ace("H" + hand)


#	Return all possible outcomes that can occur when a player/dealer has the provided
#	hand and draws a card. The result is a mapping of [outcome hand] -> [outcome probability]
#
def get_outcomes(hand, dealer_hole_card):

	if dealer_hole_card:
		
		#	A very strange thing happens when we are looking up outcomes
		#	for a dealer's hole card. If our total is H10 and this is the
		#	dealer's hole card, then it is *impossible* for the hole card to
		#	be an Ace. If the total is S11 and this is the dealer's hole
		#	card, then it is *impossible* for it to be a 10. The reason is
		#	because if the dealer had blackjack, the game would be over.
		#	
		#	Because the game is not over, it means that the dealer does not have
		#	have blackjack. Therefore, if the dealer has a 10 or an Ace showing,
		#	the probabilities must be adjusted to represent the 0% chance of having
		#	an Ace or 10 respectively.
		#
		if hand == "H10":
		
			sum_probabilities = p["2"] + p["3"] + p["4"] + p["5"] + p["6"] + p["7"] + p["8"] + p["9"] + p["10"]	
			
			return {
				add_value(hand, 2): p["2"] / sum_probabilities,
				add_value(hand, 3): p["3"] / sum_probabilities,
				add_value(hand, 4): p["4"] / sum_probabilities,
				add_value(hand, 5): p["5"] / sum_probabilities,
				add_value(hand, 6): p["6"] / sum_probabilities,
				add_value(hand, 7): p["7"] / sum_probabilities,
				add_value(hand, 8): p["8"] / sum_probabilities,
				add_value(hand, 9): p["9"] / sum_probabilities,
				add_value(hand, 10): p["10"] / sum_probabilities,
				add_ace(hand): 0.0
			}
			
		elif hand == "S11":
		
			sum_probabilities = p["2"] + p["3"] + p["4"] + p["5"] + p["6"] + p["7"] + p["8"] + p["9"] + p["A"]	
			
			return {
				add_value(hand, 2): p["2"] / sum_probabilities,
				add_value(hand, 3): p["3"] / sum_probabilities,
				add_value(hand, 4): p["4"] / sum_probabilities,
				add_value(hand, 5): p["5"] / sum_probabilities,
				add_value(hand, 6): p["6"] / sum_probabilities,
				add_value(hand, 7): p["7"] / sum_probabilities,
				add_value(hand, 8): p["8"] / sum_probabilities,
				add_value(hand, 9): p["9"] / sum_probabilities,
				add_value(hand, 10): 0.0,
				add_ace(hand): p["A"] / sum_probabilities
			}
			
		else:
		
			return {
				add_value(hand, 2): p["2"],
				add_value(hand, 3): p["3"],
				add_value(hand, 4): p["4"],
				add_value(hand, 5): p["5"],
				add_value(hand, 6): p["6"],
				add_value(hand, 7): p["7"],
				add_value(hand, 8): p["8"],
				add_value(hand, 9): p["9"],
				add_value(hand, 10): p["10"],
				add_ace(hand): p["A"]
			}
			
		
	else:
	
		return {
			add_value(hand, 2): p["2"],
			add_value(hand, 3): p["3"],
			add_value(hand, 4): p["4"],
			add_value(hand, 5): p["5"],
			add_value(hand, 6): p["6"],
			add_value(hand, 7): p["7"],
			add_value(hand, 8): p["8"],
			add_value(hand, 9): p["9"],
			add_value(hand, 10): p["10"],
			add_ace(hand): p["A"]
		}

	


#	Generates an expected value table for standing
#
def create_standing_table(output_table, lookup_table, dealer_card_count):

	empty_table(output_table, hands, hands)
	
	for player_hand in hands:

		for dealer_hand in hands:
	
			if not should_dealer_hit(dealer_hand):
				# If the dealer shouldn't hit, then we just need the payout.
				output_table[player_hand][dealer_hand] = get_hand_payout(player_hand, 3, dealer_hand, dealer_card_count)
			else:
				# If the dealer should hit, we calculate the weighted average of each outcome
				outcomes = get_outcomes(dealer_hand, dealer_card_count == 1)
				result = 0
				for outcome in outcomes:
					result += outcomes[outcome] * lookup_table[player_hand][outcome]
				output_table[player_hand][dealer_hand] = result
				

#	Generates an expected value table for hitting
#
def create_hitting_table(output_hit_table, output_ev_table, output_action_table, stand_table, lookup_table):

	empty_table(output_hit_table, hands, hands)
	empty_table(output_ev_table, hands, hands)
	empty_table(output_action_table, hands, hands)

	for player_hand in hands:

		for dealer_hand in hands:
	
			if int(player_hand[1:]) > 21:
				output_hit_table[player_hand][dealer_hand] = LOSS_PAYOUT
			elif player_hand == "H21":
				output_hit_table[player_hand][dealer_hand] = LOSS_PAYOUT		# Hitting a hard 21 means ... you lose
			else:
				outcomes = get_outcomes(player_hand, False)
				result = 0
				for outcome in outcomes:
					result += outcomes[outcome] * lookup_table[outcome][dealer_hand]
				output_hit_table[player_hand][dealer_hand] = result
		
			if output_hit_table[player_hand][dealer_hand] > stand_table[player_hand][dealer_hand]:
				output_action_table[player_hand][dealer_hand] = "H"
				output_ev_table[player_hand][dealer_hand] = output_hit_table[player_hand][dealer_hand]
			else:
				output_action_table[player_hand][dealer_hand] = "S"
				output_ev_table[player_hand][dealer_hand] = stand_table[player_hand][dealer_hand]
				

#	Generates an expected value table for doubling
#				
def create_doubling_table(output_doubling_table, output_action_table, output_ev_table, stand_table, hs_table, action_table):

	empty_table(output_doubling_table, hands, hands)
	empty_table(output_action_table, hands, hands)
	empty_table(output_ev_table, hands, hands)
	
	for player_hand in hands:
	
		for dealer_hand in hands:
		
			if int(player_hand[1:]) > 21:
				output_doubling_table[player_hand][dealer_hand] = 2 * LOSS_PAYOUT
			elif player_hand == "H21":
				output_doubling_table[player_hand][dealer_hand] = 2 * LOSS_PAYOUT	# Doubling on hard 21 means you lose ... twice
			else:
				outcomes = get_outcomes(player_hand, False)
				result = 0
				for outcome in outcomes:
					result += 2 * outcomes[outcome] * stand_table[outcome][dealer_hand]
				output_doubling_table[player_hand][dealer_hand] = result
				
			if output_doubling_table[player_hand][dealer_hand] > hs_table[player_hand][dealer_hand]:
				output_action_table[player_hand][dealer_hand] = "D/" + action_table[player_hand][dealer_hand]
				output_ev_table[player_hand][dealer_hand] = output_doubling_table[player_hand][dealer_hand]
			else:
				output_action_table[player_hand][dealer_hand] = action_table[player_hand][dealer_hand]
				output_ev_table[player_hand][dealer_hand] = hs_table[player_hand][dealer_hand]
				

#	Generates an expected value table for splitting
#
def create_split_table(output_split_table, output_action_table, output_ev_table, ev_table, action_table, ev_stand_table):

	empty_table(output_split_table, splithands, hands)
	empty_table(output_action_table, splithands, hands)
	empty_table(output_ev_table, splithands, hands)
	
	for player_hand in splithands:
		
		for dealer_hand in hands:
			
			no_split_hand = ""
			split_card = ""
			
			if player_hand == "A,A":
				split_card = "A"
				no_split_hand = "S12"
			else:
				split_card = player_hand.split(",")[0]
				no_split_hand = "H" + str(int(split_card) * 2)
				
			split_outcomes = get_outcomes(split_card, False)
			k = 0
			resplit_probability = 0
			
			for outcome in split_outcomes:
				if outcome == player_hand:
					resplit_probability = split_outcomes[outcome]
				else:
					#	Aces are special because they only get one card, which means we need the EV of standing.
					if player_hand == "A,A":
						k += split_outcomes[outcome] * ev_stand_table[outcome][dealer_hand]
					else:
						k += split_outcomes[outcome] * ev_table[outcome][dealer_hand]
			
			result = (2 * k) / (1 - 2 * resplit_probability)
			output_split_table[player_hand][dealer_hand] = result
			
			if result > ev_table[no_split_hand][dealer_hand]:
				output_action_table[player_hand][dealer_hand] = "P"
				output_ev_table[player_hand][dealer_hand] = result
			else:
				output_action_table[player_hand][dealer_hand] = action_table[no_split_hand][dealer_hand]
				output_ev_table[player_hand][dealer_hand] = ev_table[no_split_hand][dealer_hand]
			

#	Integrates the expected value of surrendering
#
def include_surrender_table(phands, dhands, output_action_table, output_ev_table, ev_table, action_table):

	empty_table(output_action_table, phands, dhands)
	empty_table(output_ev_table, phands, dhands)
	
	for player_hand in phands:
	
		for dealer_hand in dhands:
		
			if ev_table[player_hand][dealer_hand] < -0.5:
				output_ev_table[player_hand][dealer_hand] = -0.5
				output_action_table[player_hand][dealer_hand] = "X/" + action_table[player_hand][dealer_hand]
			else:
				output_ev_table[player_hand][dealer_hand] = ev_table[player_hand][dealer_hand]
				output_action_table[player_hand][dealer_hand] = action_table[player_hand][dealer_hand]
	

#	First, we get the expected value of standing. Note that the expected value of standing is dependent on how
#	many cards the dealer has due to some strange things that happen with the dealer hole card (see comments
#	in get_outcomes(...) for more details).

ev_stand_d3 = {}
ev_stand_d2 = {}
ev_stand_d1 = {}

create_standing_table(ev_stand_d3, ev_stand_d3, 3)
create_standing_table(ev_stand_d2, ev_stand_d3, 2)
create_standing_table(ev_stand_d1, ev_stand_d2, 1)


#	Next, we need to calculate the expected value of hitting and combine that with standing to get the expected
#	value of hitting or standing (hs)

ev_hit = {}
ev_hs = {}
hs_actions = {}

create_hitting_table(ev_hit, ev_hs, hs_actions, ev_stand_d1, ev_hs)


#	Add doubling
#
ev_double = {}
ev_hsd = {}
hsd_actions = {}

create_doubling_table(ev_double, hsd_actions, ev_hsd, ev_stand_d1, ev_hs, hs_actions)



#	Add splitting
#
ev_split = {}
ev_split_hsd = {}
split_actions = {}

create_split_table(ev_split, split_actions, ev_split_hsd, ev_hsd, hsd_actions, ev_stand_d1)



#	Add surrendering
#
final_action_table = {}
final_ev_table = {}
final_split_action_table = {}
final_split_ev_table = {}

include_surrender_table(hands, hands, final_action_table, final_ev_table, ev_hsd, hsd_actions)
include_surrender_table(splithands, hands, final_split_action_table, final_split_ev_table, ev_split_hsd, split_actions)


#	Calculate the final expected value
#
ev = 0
er = {}

empty_table(er, hands, hands, 0)
empty_table(er, splithands, hands, 0)

for player_card_1 in cards:
	for player_card_2 in cards:
		for dealer_card in cards:
		
			dealer_hand = "S11" if dealer_card == "A" else "H" + str(dealer_card)
			player_hand = ""
			split_hand = False
			blackjack_loss_ev = LOSS_PAYOUT
			
			if player_card_1 == player_card_2:
				player_hand = player_card_1 + "," + player_card_2
				split_hand = True
			elif player_card_1 == "A":
				player_hand = add_ace("H" + player_card_2)
			elif player_card_2 == "A":
				player_hand = add_ace("H" + player_card_1)
			else:
				player_hand = "H" + str(int(player_card_1) + int(player_card_2))
				
			hand_ev = final_split_ev_table[player_hand][dealer_hand] if split_hand else final_ev_table[player_hand][dealer_hand]
			hand_likelyhood = p[player_card_1] * p[player_card_2] * p[dealer_card]
			
			if player_hand == "S21":
				hand_ev = BLACKJACK_PAYOUT
				blackjack_loss_ev = PUSH_PAYOUT
				
			if dealer_card == 'A':
				ev += hand_likelyhood * (p['10'] * blackjack_loss_ev + (1 - p['10']) * hand_ev)
				er[player_hand][dealer_hand] += hand_likelyhood * (p['10'] * blackjack_loss_ev + (1 - p['10']) * hand_ev)
			elif dealer_card == '10':
				ev += hand_likelyhood * (p['A'] * blackjack_loss_ev + (1 - p['A']) * hand_ev)
				er[player_hand][dealer_hand] += hand_likelyhood * (p['A'] * blackjack_loss_ev + (1 - p['A']) * hand_ev)
			else:
				ev += hand_likelyhood * hand_ev
				er[player_hand][dealer_hand] += hand_likelyhood * hand_ev

print ""
print "Basic Strategy:"
print ""

pretty_print_table(final_action_table, phands, dhands, 5, 3)
pretty_print_table(final_split_action_table, splithands, dhands, 5, 3)

print "Expected Value:", ev
print ""

