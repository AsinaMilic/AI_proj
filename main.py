import copy
import math
class Player:
    def __init__(self, sign, who_plays: bool):
        self.human_or_pc = who_plays  # 0-pc, 1-human
        self.sign = sign
        self.all_available_states = []
class Game:
    matrix: None
    matrix_states: None
    players_turn: Player
    player1: Player
    player2: Player
    print_ava_states: bool

    def __init__(self, human_or_pc1, n: int, m: int, print_states: bool, depth ):
        self.depth = depth
        self.i = None #valid i for alphabeta
        self.j = None #valid j for alphabeta
        self.N = n
        self.M = m
        self.print_ava_states = print_states
        self.matrix = [[" " for i in range(0, M)] for j in range(0, N)]  # [1,2,3 ... ,M+1]
        self.matrix_states = []
        self.add_new_state()
        self.player1 = Player("X", human_or_pc1)
        self.player2 = Player("O", True)  # 2.player is always human
        self.players_turn = self.player1
        # self.print_table()

    def play_a_turn(self):
        self.find_all_available_states() #do not comment
        if self.print_ava_states: #do we?
            self.print_states(self.players_turn.all_available_states)  # Do we want to print all available states?
        print("\nTrenutno stanje table")
        self.print_table()

        if self.players_turn is self.player2:
            while True:
                try:
                    row = int(input("Unesite vrstu polja: "))
                    column = input("Unestie kolonu polja [A-Z]: ")
                    if self.move_valid(row, column):
                        m = ord(column) - 65  # A -> 1
                        n = N - row
                        self.matrix[n][m] = 'O'
                        self.matrix[n][m + 1] = 'O'
                        self.players_turn = self.player1
                    else:
                        return False
                except ValueError:
                    return False
                else:
                    break
        elif self.players_turn is self.player1 and self.player1.sign == "X" and self.player1.human_or_pc == True:
            while True:
                try:
                    row = int(input("Unesite vrstu polja: "))
                    column = input("Unestie kolonu polja [A-Z]: ")
                    if self.move_valid(row, column):
                        m = ord(column) - 65
                        n = N - row
                        self.matrix[n][m] = 'X'
                        self.matrix[n-1][m] = 'X'
                        self.players_turn = self.player2
                    else:
                        return False
                except ValueError:
                    return False
                else:
                    break
        else: #else COMPUTER plays
            matrix2 = copy.deepcopy(self.matrix)
            _, row, column = self.alphabeta(self.depth, False, -math.inf, math.inf)
            print(f"Kompjuter je igrao: [{row},{column}]" )
            self.matrix = matrix2
            self.set_domino(row, column, False)
            self.players_turn = self.player2

        self.add_new_state()
        return True

    #short and optimized version of alphabeta.    Why using separate functions for the max player and the min player, when I can use payer.
    def alphabeta(self, depth: int, player: bool, a, b):
        if depth == 0: #cant go any deeper,
            return self.heuristics(player) #use heuristic to estimate how good the move was.

        ri, rj = -12345, -12345 # random init
        for i in range(self.N):
            for j in range(self.M):
                if self.set_domino(i, j, player): #try to play that position for every field in the matrix (top g)
                    if not player: # so, placement is ok, if X plays, remember that
                        self.i, self.j = i, j
                    eva, _, _ = self.alphabeta(depth - 1, not player, -b, -a) #The algorithm alternates between the max player and the min player, and at each step, it updates the alpha and beta values
                    eva = - eva
                    self.remove_item(i, j, player) #remove placed item, we need to evaluate for the other positions also
                    if eva > a: # The value of eval is used to update the alpha value, which represents the best value that the current player (the "max player") can guarantee
                        a = eva
                        ri,rj=i,j #these are good placements
                        if b <= a:  #If the alpha value ever becomes greater than or equal to the beta value, the search is cut off (also called a "cutoff") because the min player will not allow the max player to have a value greater than beta.
                            return b, ri, rj  #return the evaluation and indexes. If the evaluation is good for that placement, we'll store them. ri(return i), rj(return j)

        return a, ri if ri >= 0 else self.i, rj if rj >= 0 else self.j  #self.i and self.j are valid, if ri and rj ain't
    def heuristics(self, dir):           #that player               vs              opponent
        return self.get_num_of_ava_placements(dir) - self.get_num_of_ava_placements(not dir), None, None
    def set_domino(self, row, col, dir):
        col_m, row_m = 0, 0
        if not dir:  # dir == Vertical == False? == 'X'
            row_m = 1
        else:
            col_m = 1
        if row + row_m >= self.N or col + col_m >= self.M or self.matrix[row + row_m][col] != ' ' or self.matrix[row][
            col + col_m] != ' ':
            return False
        else:
            self.matrix[row][col] = 'O' if dir else 'X'
            self.matrix[row + row_m][col + col_m] = 'O' if dir else 'X'
            return True

    def remove_item(self, row, col, dir):
        if not dir:
            self.matrix[row][col] = ' '
            self.matrix[row + 1][col] = ' '
        else:
            self.matrix[row][col] = ' '
            self.matrix[row][col + 1] = ' '

    def move_valid(self, row, column):
        if isinstance(column, str):
            m = ord(column) - 65  # A -> 1
        else:
            m = column
        n = self.N - row  # inverted rows

        if self.players_turn is self.player1:  # checking if vertical one can be placed
            if row < 0 or row >= N or m < 0 or m > M:
                return False

            if self.matrix[n][m] == ' ' and self.matrix[n - 1][m] == ' ':
                return True
            else:
                return False
        else:  # checking horizontal one
            if row < 0 or row > N or m < 0 or m >= M - 1:
                return False
            if self.matrix[n][m] == ' ' and self.matrix[n][m + 1] == ' ':
                return True
            else:
                return False
    def is_game_over(self):
        if self.players_turn is self.player1:  # any two empty vertical spaces?
            for i in range(0, self.N - 1):
                for j in range(0, self.M):
                    if self.matrix[i][j] == ' ' and self.matrix[i + 1][j] == ' ':
                        return False
        else:  # any two empty horizontal spaces?
            for i in range(0, self.N):
                for j in range(0, self.M - 1):
                    if self.matrix[i][j] == ' ' and self.matrix[i][j + 1] == ' ':
                        return False
        return True
    def get_num_of_ava_placements(self, dir: bool):
        num_of_states = 0
        self.players_turn.all_available_states.clear()
        if dir:  # any two empty vertical spaces?
            for i in range(0, self.N - 1):
                for j in range(0, self.M):
                    if self.matrix[i][j] == ' ' and self.matrix[i + 1][j] == ' ':
                        num_of_states += 1
        else:
            for i in range(0, self.N):
                for j in range(0, self.M - 1):
                    if self.matrix[i][j] == ' ' and self.matrix[i][j + 1] == ' ':
                        num_of_states += 1
        return num_of_states
    def find_all_available_states(self):
        self.players_turn.all_available_states.clear()
        if self.players_turn is self.player1:  # any two empty vertical spaces?
            for i in range(0, self.N - 1):
                for j in range(0, self.M):
                    if self.matrix[i][j] == ' ' and self.matrix[i + 1][j] == ' ':
                        self.matrix[i][j] = 'X'
                        self.matrix[i + 1][j] = 'X'
                        self.player1.all_available_states.append(copy.deepcopy(self.matrix))
                        self.matrix[i][j] = ' '
                        self.matrix[i + 1][j] = ' '
        else:
            for i in range(0, self.N):
                for j in range(0, self.M - 1):
                    if self.matrix[i][j] == ' ' and self.matrix[i][j + 1] == ' ':
                        self.matrix[i][j] = 'O'
                        self.matrix[i][j + 1] = 'O'
                        self.player2.all_available_states.append(copy.deepcopy(self.matrix))
                        self.matrix[i][j] = ' '
                        self.matrix[i][j + 1] = ' '
    def add_new_state(self):
        self.matrix_states.append(copy.deepcopy(self.matrix))  # Kopira trenutno stanje table i dodaje u listu stanja
    def print_states(self, matrica):
        # Stampa sva dosadasnja stanja u terminalu
        for k in range(0, len(matrica)):
            if matrica == self.matrix_states :
                print(f"\nStanje igre: {k + 1}")
            else:
                print(f"\nSlobodan potez broj: {k + 1}")
            letter = 65  # A
            # vrh table
            print(" ", end='')  # corner
            for i in range(0, M):
                print(f"   {chr(letter + i)}", end='')  # The end key will set the string that needs to be appended
            print('')
            print(" ", end='')
            for i in range(0, M):
                print("   =", end='')
            print('')

            for i in range(0, N):
                print(f"{N - i}||", end='')
                for j in range(0, M):  # counting backwards
                    print(f" {matrica[k][i][j]} |", end='')
                print(f"|{N - i}")
                print("  ", end='')
                for _ in range(0, M):
                    print(" ---", end='')
                print("  ")
    def print_table(self):
        letter = 65  # A
        # vrh table
        print(" ", end='')  # corner
        for i in range(0, M):
            print(f"   {chr(letter + i)}", end='')  # The end key will set the string that needs to be appended
        print('')
        print(" ", end='')
        for i in range(0, M):
            print("   =", end='')
        print('')

        # matrix
        for i in range(0, N):
            print(f"{N - i}||", end='')
            for j in range(0, M):  # counting backwards
                print(f" {self.matrix[i][j]} |", end='')
            print(f"|{N - i}")
            print("  ", end='')
            for _ in range(0, M):
                print(" ---", end='')
            print("  ")

if __name__ == "__main__":
    print("### Game Domineering ###")

    while True:
        try:
            N = int(input("Unesite broj vrsta table: "))
            M = int(input("Unesite broj kolona table: "))
        except ValueError:
            print("Nevalidan unos, pokusajte ponovo!")
            continue
        else:
            break
    human_or_pc = int(input("Igrac 1 je X\nDa li je on covek ili racunar? (0-racunar, 1-covek): "))
    depth= None
    if not human_or_pc:
        depth = int(input("Dubina preporuke: Za tablu 4x4 na dubini 8, kompjuter je nepobediv, a za 8x8 na dubini 5, bice razumno brz.\nDubina alphabete: "))
    print_states = input("Da li zelite prikaz svih mogucih poteza? (0-Ne, 1-Da): ")
    print_states = True if (print_states == '1' or print_states == 'Da' or print_states == 'da') else False
    print("Igrac 2 je O i on ce biti covek")
    game = Game(bool(human_or_pc), N, M, print_states, depth)
    player1_plays = True
    while True:
        if game.is_game_over():
            print("###############################################\nKraj igre!")
            game.print_table()
            print("Pobedio je 2. igrac - O!") if game.players_turn.sign == "X" else print("Pobedio je 1. igrac - X!")
            print("###############################################")
            break
        print("\nIgrac X je na potezu") if player1_plays is True else print("Igrac O je na potezu")

        placed_correctly: bool = game.play_a_turn()
        while not placed_correctly:
            print("Nevalidan potez, pokusajte ponovo!")
            placed_correctly: bool = game.play_a_turn()
        player1_plays = not player1_plays