from board import Backgammon
from dice import roll_die, roll_dice

def prompt_for_input_from_list(options : set):
	response = None
	formatted_options = sorted(options)
	options = {str(x) for x in options}
	while response not in options:
		print("Možnosti: ", formatted_options)
		response = input("Tvůj výběr  -> ")
		if response not in options:
			print("Nejde provést.")
	return response


class BackgammonGame(Backgammon):
	START_BOARD = [0, 2, 0, 0, 0, 0, -5, 0, -3, 0, 0, 0, 5, -5, 0, 0, 0, 3, 0, 5, 0, 0, 0, 0, -2, 0]

	def __init__(self, start_board=START_BOARD):
		white_to_move = self.determine_start_player()

		super().__init__(start_board, white_to_move)
		print("""Bílý:      Černý:
->->|              <-<-^
<-<-ˇ              ->->|
""")     
		self.dice = []
		self.turn()

	def determine_start_player(self):
		white_roll = roll_die()
		print("Bílý hodil", white_roll)
		black_roll = roll_die()
		print("Černý hodil", black_roll)
		if white_roll == black_roll:
			print("Hází se znovu.")
			return self.determine_start_player()
		elif white_roll > black_roll:
			print("Bílý začíná.")
			return True
		else:
			print("Černý začíná.")
			return False

	def roll_and_parse_dice(self):
		dice = roll_dice()
		print("Hodil: ", dice)
		if dice[0] == dice[1]: # dvojitá
			self.dice = [dice[0]] * 4
		else:
			self.dice = list(dice)

	def turn(self):
		print(self)

		print(("Bílý" if self.white_to_move else "Černý") + " hraje.")
		self.roll_and_parse_dice()

		possible_turns = self.generate_valid_turns(self.dice)
		while self.dice:
			if not possible_turns: # žádné možnosti
				# print("Žádné možnosti.")
				self.flip_turn()
				return

			possible_start_indices = set(turn[0][0] for turn in possible_turns)
			print("Vyber počáteční pozici.")
			start = int(prompt_for_input_from_list(possible_start_indices))

			possible_end_indices = set(turn[0][1] for turn in possible_turns if turn[0][0] == start)
			print("Vyber konečnou pozici.")
			end = int(prompt_for_input_from_list(possible_end_indices))
			self.move(start, end)
			self.dice.remove(abs(start - end))
			possible_turns = self.generate_valid_turns(self.dice)

		self.flip_turn()
	
	def flip_turn(self):
		print()
		game_over = self.white_won if self.white_to_move else self.black_won
		if game_over:
			print(("Bílý" if self.white_to_move else "Černý") + " vyhrál!")
			return
		self.white_to_move = not self.white_to_move
		self.turn()


if __name__ == '__main__':
	game = BackgammonGame()