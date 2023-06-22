class Vrhcaby_board:
	bar_white_idx = 0
	bar_black_idx = 25
	start_board = [0, 2, 0, 0, 0, 0, -5, 0, -3, 0, 0, 0, 5, -5, 0, 0, 0, 3, 0, 5, 0, 0, 0, 0, -2, 0]
	
	def __init__(self, start_board=start_board, white_to_move=True):
		self.board = start_board
		self.white_to_move = white_to_move
		
	@property #pocet bilych kamenu na zacatku desky
	def bar_white(self) -> int:
		return self.board[self.bar_white_idx]

	@property #pocet cernych kamenu na konci desky
	def bar_black(self) -> int:
		return self.board[self.bar_black_idx]

	@property #kontroluje jestli jsou na desce bile kameny
	def white_on_bar(self) -> bool:
		return self.bar_white != 0
	
	@property #kontroluje jestli jsou na desce cerne kameny
	def black_on_bar(self) -> bool:
		return self.bar_black != 0

	@property #seznam indexu na kterych jsou bile kameny
	def white_stones(self) -> list:
		return [i for i, x in enumerate(self.board) if x > 0]

	@property #seznam indexu na kterych jsou cerne kameny
	def black_stones(self) -> list:
		return [i for i, x in enumerate(self.board) if x < 0]

	@property #určení nejvzdálenějšího obsazeného indexu bílých kamenů
	def white_farthest_occupied_point(self) -> int:
		return min(self.white_stones)

	@property #určení nejvzdálenějšího obsazeného indexu černých kamenů
	def black_farthest_occupied_point(self) -> int:
		return max(self.black_stones)

	@property #kontrola jestli bile kameny mohou opustit desku, vse na min 19 pointu
	def white_bearing_off(self) -> bool:
		count_not_home_board = sum(self.board[i] for i in self.white_stones if self.bar_white_idx <= i <= 18)
		return not bool(count_not_home_board)

	@property #kontrola jestli cerne kameny mohou opustit desku, vse na min 6 pointu
	def black_bearing_off(self) -> bool:
		count_not_home_board = sum(self.board[i] for i in self.black_stones if 7 <= i <= self.bar_black_idx)
		return not bool(count_not_home_board)

	@property #kontrola jestli jsou na desce bile kameny, win statement
	def white_won(self) -> bool:
		return not bool(self.white_stones)

	@property #kontrola jestli jsou na desce cerne kameny, win statement
	def black_won(self) -> bool:
		return not bool(self.black_stones)

	def move(self, start : int, end : int):
		if self.white_to_move: #bily tahne
			assert self.board[start] > 0,"Chybný pohyb: bílý je na řadě" #kontrola počtu kamenu na startu
			self.board[start] -= 1 #odečtení kamene na starting indexu
			if end >= self.bar_black_idx: #kontrola jestli je end index za lištou (domácí pole)
				assert self.white_bearing_off, "Chybný pohyb: bílý nemůže vyndat kámen"
			else:
				assert self.board[end] >= -1, "Chybný pohyb: zablokován"
				if self.board[end] == -1: #kontrola jestli na indexu je value cerneho kamene
					self.board[self.bar_black_idx] -= 1 #vyhozeni enemy kamene
					self.board[end] = 1
				else:
					self.board[end] += 1 #pricte kamen na zvoleny end index
		else: #cerny tahne
			assert self.board[start] < 0, "Chybný pohyb: černý je na řadě" #kontrola poctu kamenu
			self.board[start] += 1
			if end <= self.bar_white_idx:
				assert self.black_bearing_off, "Chybný pohyb: černý nemůže vyndat kámen"
			else:
				assert self.board[end] <= 1, "Chybný pohyb: zablokován"
				if self.board[end] == 1: #kontrola jestli je na indexu bily kamen
					self.board[self.bar_white_idx] += 1 #vyhozeni bileho
					self.board[end] = -1  #pricteni cerneho kamene
				else:
					self.board[end] -= 1 #pricteni cerneho kamene na prazdne misto

	def valid_move(self, start : int, end : int) -> bool: #valid_move overeni
		has_checkers = self.board[start] >= 1 if self.white_to_move else self.board[start] <= -1 #kontrola dostatku kamenu obou hracu
		in_range = (self.bar_white_idx < end < self.bar_black_idx) #kontrola jestli je cilova pozice viditelna v gui
		if not in_range: #odvod kamenu
			bearing_off = self.white_bearing_off if self.white_to_move else self.black_bearing_off #kdo je na řadě
			if self.white_to_move:
				valid_bear_off = (end == self.bar_black_idx) or ((end > self.bar_black_idx) and (start == self.white_farthest_occupied_point))
			else:
				valid_bear_off = (end == self.bar_white_idx) or ((end < self.bar_white_idx) and (start == self.black_farthest_occupied_point))
			return has_checkers and bearing_off and valid_bear_off
		blocked = self.board[end] <= -2 if self.white_to_move else self.board[end] >= 2 #kontrola jestli na end indexu jsou dva enemy kameny
		return has_checkers and (not blocked)
		
	def generate_valid_moves(self, dice : list) -> list: #tahy
		on_bar = self.white_on_bar if self.white_to_move else self.black_on_bar #proměná on_bar dostává hodnotu atributu white_on_bar jestli téhne bílej
		bar_index = self.bar_white_idx if self.white_to_move else self.bar_black_idx #proměná bar_index dostává hodnotu atributu bar_white_idx jestli téhne bilej
		possible_start_stones = [bar_index] if on_bar else (self.white_stones if self.white_to_move else self.black_stones)#pokud on_bar=true do possible_start uloží bar_index
		valid_moves = [] #pokud on_bar=false do possible_start... se uloží atribut white/black_stones
		for die in dice: #prochazi seznam
			die = die if self.white_to_move else (-die) #upravuje hodnotu kostky podle toho kdo tahne
			valid_moves += [(i, i+die) for i in possible_start_stones if self.valid_move(i, i+die)] #platne dvojice do seznamu
		return valid_moves #i,i+die pohyb

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
		remaining_checkers = abs(sum(self.board[i] for i in (self.white_stones if self.white_to_move else self.black_stones)))
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
		if most_dice == 1:
			larger = max(dice)
			valid_turns = [turn for turn in valid_turns if raw_move_die(turn[0]) == larger]
		else:
			valid_turns = [turn for turn in valid_turns if len(turn) == most_dice]
			max_dice_value = max(sum_dice_turn(turn) for turn in valid_turns)
			valid_turns = [turn for turn in valid_turns if sum_dice_turn(turn) == max_dice_value]
		return valid_turns
		
	def copy(self):
		return Vrhcaby_board(self.board[:], self.white_to_move)
		
	def __str__(self):
		def tile_to_string(val : int) -> str:
			#řetězcová reprezentace herní desky, každé pole string o 3 místech
			if val == 0: #je-li value 0 na dasce 3xspace
				return "   " 
			if val > 0:
				return f"{val:2d}B" #pole černý kamen, value kladne
			if val < 0:
				return f"{abs(val):2d}Č" #pole bilý kamen, value zaporne

		out = " " + "   ".join(f"{x:2d}" for x in range(1, 7)) #pole 1-6, dvouciferny int
		out += "   bar   "
		out += "   ".join(f"{x:2d}" for x in range(7, 13))
		out += '\n' + '- ' * 33 + '\n' #vršek desky, zalomeno \n
		out += '  '.join(tile_to_string(x) for x in self.board[1:7]) + " |" #vertikální oddělení baru, 1-6 řetězce spojeny
		out += tile_to_string(self.bar_white) + ' | '
		out += '  '.join(tile_to_string(x) for x in self.board[7:13]) #druhé vertikální oddělení
		out += '\n' + '- ' * 33 + '\n' #střed desky
		out += '  '.join(tile_to_string(x) for x in self.board[24:18:-1]) + " |"
		out += tile_to_string(self.bar_black) + ' | '
		out += '  '.join(tile_to_string(x) for x in self.board[18:12:-1])
		out += '\n' + '- ' * 33 + '\n' #spodek desky
		out += " " + "   ".join(f"{x:2d}" for x in range(24, 18, -1))
		out += "   bar   "
		out += "   ".join(f"{x:2d}" for x in range(18, 12, -1))
		out += "\n"
		return out
		