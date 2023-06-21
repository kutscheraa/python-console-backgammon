class Backgammon:
	bar_white_idx = 0
	bar_black_idx = 25
	START_BOARD = [0, 2, 0, 0, 0, 0, -5, 0, -3, 0, 0, 0, 5, -5, 0, 0, 0, 3, 0, 5, 0, 0, 0, 0, -2, 0]
	
	def __init__(self, start_board=START_BOARD, white_to_move=True):
		self.board = start_board
		self.white_to_move = white_to_move
		
	@property
	def bar_white(self) -> int:
		return self.board[self.bar_white_idx]

	@property
	def bar_black(self) -> int:
		return self.board[self.bar_black_idx]

	@property
	def white_on_bar(self) -> bool:
		return self.bar_white != 0
	
	@property
	def black_on_bar(self) -> bool:
		return self.bar_black != 0

	@property
	def white_indices(self) -> list:
		return [i for i, x in enumerate(self.board) if x > 0]

	@property
	def black_indices(self) -> list:
		return [i for i, x in enumerate(self.board) if x < 0]

	@property
	def white_farthest_occupied_point(self) -> int:
		return min(self.white_indices)

	@property
	def black_farthest_occupied_point(self) -> int:
		return max(self.black_indices)

	@property
	def white_bearing_off(self) -> bool:
		count_not_home_board = sum(self.board[i] for i in self.white_indices if self.bar_white_idx <= i <= 18)
		return not bool(count_not_home_board)

	@property
	def black_bearing_off(self) -> bool:
		count_not_home_board = sum(self.board[i] for i in self.black_indices if 7 <= i <= self.bar_black_idx)
		return not bool(count_not_home_board)

	@property
	def white_won(self) -> bool:
		return not bool(self.white_indices)

	@property
	def black_won(self) -> bool:
		return not bool(self.black_indices)

	def move(self, start : int, end : int):
		if self.white_to_move:
			assert self.board[start] > 0, "Chybný pohyb: bílý je na řadě"
			self.board[start] -= 1
			if end >= self.bar_black_idx:
				assert self.white_bearing_off, "Chybný pohyb: bílý nevyndavá kámen"
			else:
				assert self.board[end] >= -1, "Chybný pohyb: zablokován"
				if self.board[end] == -1:
					self.board[self.bar_black_idx] -= 1
					self.board[end] = 1
				else:
					self.board[end] += 1
		else:
			assert self.board[start] < 0, "Chybný pohyb: černý je na řadě"
			self.board[start] += 1
			if end <= self.bar_white_idx:
				assert self.black_bearing_off, "Chybný pohyb: černý nevyndavá kámen"
			else:
				assert self.board[end] <= 1, "Chybný pohyb: zablokován"
				if self.board[end] == 1:
					self.board[self.bar_white_idx] += 1
					self.board[end] = -1
				else:
					self.board[end] -= 1

	def valid_move(self, start : int, end : int) -> bool:
		has_checkers = self.board[start] >= 1 if self.white_to_move else self.board[start] <= -1
		in_range = (self.bar_white_idx < end < self.bar_black_idx)
		if not in_range:
			bearing_off = self.white_bearing_off if self.white_to_move else self.black_bearing_off
			if self.white_to_move:
				valid_bear_off = (end == self.bar_black_idx) or ((end > self.bar_black_idx) and (start == self.white_farthest_occupied_point))
			else:
				valid_bear_off = (end == self.bar_white_idx) or ((end < self.bar_white_idx) and (start == self.black_farthest_occupied_point))
			return has_checkers and bearing_off and valid_bear_off
		blocked = self.board[end] <= -2 if self.white_to_move else self.board[end] >= 2
		return has_checkers and (not blocked)
		
	def generate_valid_moves(self, dice : list) -> list:
		on_bar = self.white_on_bar if self.white_to_move else self.black_on_bar
		bar_index = self.bar_white_idx if self.white_to_move else self.bar_black_idx 
		possible_start_indices = [bar_index] if on_bar else (self.white_indices if self.white_to_move else self.black_indices)
		valid_moves = []
		for die in dice:
			die = die if self.white_to_move else (-die)
			valid_moves += [(i, i+die) for i in possible_start_indices if self.valid_move(i, i+die)]
		return valid_moves

	def generate_valid_turns(self, dice : list) -> list:
		def move_die(move):
			def keep_in_range(index):
				return max(min(index, self.bar_white_idx), self.bar_black_idx)
			return abs(keep_in_range(move[1]) - keep_in_range(move[0]))

		def raw_move_die(move):
			return abs(move[1] - move[0])

		def sum_dice_turn(turn):
			return sum(move_die(move) for move in turn)

		valid_moves = self.generate_valid_moves(set(dice))
		remaining_checkers = abs(sum(self.board[i] for i in (self.white_indices if self.white_to_move else self.black_indices)))
		if len(dice) == 1 or remaining_checkers == 1:
			return [[move] for move in valid_moves]
		valid_turns = []
		for move in valid_moves:
			remaining_dice = dice[:]
			remaining_dice.remove(raw_move_die(move))
			copy = self.copy()
			copy.move(*move)
			valid_turns += [[move] + continuation for continuation in copy.generate_valid_turns(remaining_dice)]
		if not valid_turns:
			return []
		most_dice = max(len(turn) for turn in valid_turns)
		if most_dice == 1: # Must play larger die
			larger = max(dice)
			valid_turns = [turn for turn in valid_turns if raw_move_die(turn[0]) == larger]
		else: # Must play most dice possible
			valid_turns = [turn for turn in valid_turns if len(turn) == most_dice]
			max_dice_value = max(sum_dice_turn(turn) for turn in valid_turns)
			valid_turns = [turn for turn in valid_turns if sum_dice_turn(turn) == max_dice_value]
		return valid_turns
		
	def copy(self):
		return Backgammon(self.board[:], self.white_to_move)
		
	def __str__(self):
		def tile_to_string(val : int) -> str:
			if val == 0:
				return "   "
			if val > 0:
				return f"{val:2d}B"
			if val < 0:
				return f"{abs(val):2d}Č"

		out = " " + "   ".join(f"{x:2d}" for x in range(1, 7))
		out += "   bar   "
		out += "   ".join(f"{x:2d}" for x in range(7, 13))
		out += '\n' + '- ' * 33 + '\n'
		out += '  '.join(tile_to_string(x) for x in self.board[1:7]) + " |"
		out += tile_to_string(self.bar_white) + ' | '
		out += '  '.join(tile_to_string(x) for x in self.board[7:13])
		out += '\n' + '- ' * 33 + '\n'
		out += '  '.join(tile_to_string(x) for x in self.board[24:18:-1]) + " |"
		out += tile_to_string(self.bar_black) + ' | '
		out += '  '.join(tile_to_string(x) for x in self.board[18:12:-1])
		out += '\n' + '- ' * 33 + '\n'
		out += " " + "   ".join(f"{x:2d}" for x in range(24, 18, -1))
		out += "   bar   "
		out += "   ".join(f"{x:2d}" for x in range(18, 12, -1))
		out += "\n"
		return out
		

if __name__ == '__main__':
	game = Backgammon()
	print(game)
	print(game.generate_valid_turns([5]))
	print(game.generate_valid_turns([5, 5]))

	game.move(1, 3)
	print(game)
	game.white_to_move = False
	game.move(6, 3)
	print(game)
	game.white_to_move = True

	print(game.generate_valid_turns([5, 6]))


	print([turn[0][0] for turn in game.generate_valid_turns([5, 6])])
