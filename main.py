import copy

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

    def __init__(self, human_or_pc1, n: int, m: int, print_states: bool):
        self.N = n
        self.M = m
        self.print_ava_states = print_states
        self.matrix = [[" " for i in range(0, M)] for j in range(0, N)]  # [1,2,3 ... ,M+1]
        self.matrix_states = []
        self.add_new_state()
        self.player1 = Player("X", human_or_pc1)
        self.player2 = Player("O", True)  # 2.player is always human
        self.players_turn = self.player1
        #self.print_table()

    def play_a_turn(self):
        self.find_all_available_states()
        
        if self.print_ava_states:
            self.print_states(self.players_turn.all_available_states) #Da li zelimo da stampamo sve slobodne poteze
        print("\nTrenutno stanje table")
        self.print_table()
        if self.players_turn is self.player2:  #player1 ce biti kompjuter
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
        else:
            row, column = self.alpha_beta(5, False)
            self.place_item(row,column,False)
            self.players_turn = self.player2
            #if self.move_valid(row-1, column):
               # m = column
               # n = N - row - 1

        self.add_new_state()

        ############  Da li zelimo da stampa sva stanja do sada  ############
        #self.print_states(self.matrix_states)
        return True



    def alpha_beta(self, RECURSIVITY :int , dir: bool): #dir = HORIZONTAL = False
        #i=0
        #j=0
        print("computers turn using alpha beta")
        e, i, j = self.alphabeta(RECURSIVITY, False, 0, 0, -self.N*self.M, self.N*self.M)
        return i,j

    def alphabeta(self,recursivity: int, dir: bool, ri, rj, alpha, beta):
        if recursivity == 0:
            return self.get_possibilities(dir) - self.get_possibilities(not dir), ri, rj

        #fi=0
        #fj=0
        for i in range(0,self.N):
            for j in range(0,self.M):
                if self.place_item(i, j, dir):
                    e, ri, rj = self.alphabeta(recursivity-1, not dir, 0, 0, -beta, -alpha)
                    e = - e
                    self.remove_item(i, j, dir)
                    if e > alpha:
                        alpha = e
                        ri = i
                        rj = j
                        if alpha >= beta:
                            return beta, ri, rj

        return alpha, ri, rj
    def place_item(self,row, col, dir):
        col_m = 0
        row_m = 0
        if not dir:  #dir == Vertical == False? == 'X'
            row_m = 1
        else:
            col_m = 1

        if row+row_m >= self.N or col+col_m >= self.M or self.matrix[row+row_m][col] != ' ' or self.matrix[row][col+col_m] != ' ':
            return False
        else:
            self.matrix[row][col] = 'O' if dir else 'X'
            self.matrix[row+row_m][col+col_m] = 'O' if dir else 'X'
            return True

    def remove_item(self, row, col, dir):
        if not dir:
            self.matrix[row][col] = ' '
            self.matrix[row+1][col] = ' '
        else:
            self.matrix[row][col] = ' '
            self.matrix[row][col+1] = ' '


    def move_valid(self, row, column):
        if isinstance(column,str):
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

    def get_possibilities(self, dir: bool):  #moram lepo da proverim za dir
        broj_stanja = 0
        self.players_turn.all_available_states.clear()
        if dir:  # any two empty vertical spaces?
            for i in range(0, self.N - 1):
                for j in range(0, self.M):
                    if self.matrix[i][j] == ' ' and self.matrix[i + 1][j] == ' ':
                        self.matrix[i][j] = 'X'
                        self.matrix[i + 1][j] = 'X'
                        self.player1.all_available_states.append(copy.deepcopy(self.matrix))
                        self.matrix[i][j] = ' '
                        self.matrix[i + 1][j] = ' '
                        broj_stanja+=1
        else:
            for i in range(0, self.N):
                for j in range(0, self.M - 1):
                    if self.matrix[i][j] == ' ' and self.matrix[i][j + 1] == ' ':
                        self.matrix[i][j] = 'O'
                        self.matrix[i][j + 1] = 'O'
                        self.player2.all_available_states.append(copy.deepcopy(self.matrix))
                        self.matrix[i][j] = ' '
                        self.matrix[i][j + 1] = ' '
                        broj_stanja+=1
        return broj_stanja


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
        self.matrix_states.append(copy.deepcopy(self.matrix)) #Kopira trenutno stanje table i dodaje u listu stanja


    def print_states(self,matrica):
        #Stampa sva dosadasnja stanja u terminalu
        for k in range(0, len(matrica)):
            if(matrica == self.matrix_states):
                print(f"\nStanje igre: {k+1}")
            else:
                print(f"\nSlobodan potez broj: {k+1}")
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

    human_or_pc = bool(input("Igrac 1 je X...\nDa li je on covek ili racunar? (0-racunar, 1-covek): "))
    print_states = input("Da li zelite prikaz svih mogucih poteza? (0-Ne, 1-Da): ")
    print_states = True if (print_states == '1' or print_states == 'Da' or print_states == 'da') else False
    print("Igrac 2 je O")

    game = Game(human_or_pc, N, M, print_states)
    igrac1_na_potezu = True
    while True:
        if game.is_game_over():
            print("###############################\nKraj igre!")
            game.print_table()
            print("Pobedio je 2. igrac - O!") if game.players_turn.sign == "X" else print("Pobedio je 1. igrac - X!")
            print("###############################")
            break
        print("\nIgrac X je na potezu") if igrac1_na_potezu is True else print("Igrac O je na potezu")

        placed_correctly: bool = game.play_a_turn()
        while not placed_correctly:
            print("Nevalidan potez, pokusajte ponovo!")
            placed_correctly: bool = game.play_a_turn()
        igrac1_na_potezu = not igrac1_na_potezu
