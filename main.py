class Player:
    def __init__(self, sign, who_plays: bool):
        self.human_or_pc = who_plays  # 0-pc, 1-human
        self.sign = sign


class Game:
    matrix: [[]]
    players_turn: Player
    player1: Player
    player2: Player

    def __init__(self, human_or_pc1, n: int, m: int):
        self.N = n
        self.M = m
        self.matrix = [[" " for i in range(0, M)] for j in range(0, N)]  # [1,2,3 ... ,M+1]
        self.player1 = Player("X", human_or_pc1)
        self.player2 = Player("O", True)  # 2.player is always human
        self.players_turn = self.player1
        self.print_table()

    def play_a_turn(self):
        while True:
            try:
                row = int(input("Unesite vrstu polja: "))
                column = input("Unestie kolonu polja [A-Z]: ")
            except ValueError:
                return False
            else:
                break

        if self.move_valid(row, column):
            m = ord(column) - 65
            n = N - row
            if self.players_turn is self.player1:
                self.matrix[n][m] = 'X'
                self.matrix[n - 1][m] = 'X'
                self.players_turn = self.player2
            else:
                self.matrix[n][m] = 'O'
                self.matrix[n][m + 1] = 'O'
                self.players_turn = self.player1
            self.print_table()
            return True
        else:
            return False

    def move_valid(self, row, column):
        m = ord(column) - 65  # A -> 1
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

        # bottom part of the table
        # print(" ", end='')
        # for i in range(0, M):
        #   print("   =", end='')
        # print("")
        # print(" ", end='')  # corner
        # for i in range(0, M):
        #   print(f"   {chr(letter + i)}", end='')
        # print("")


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
    print("Igrac 2 je O")

    game = Game(human_or_pc, N, M)
    igrac1_na_potezu = True
    while True:
        if game.is_game_over():
            print("########################\nKraj igre!")
            print("Pobedio je 2. igrac - O!") if game.players_turn.sign == "X" else print("Pobedio je 1. igrac - X!")
            print("########################")
            break
        print("Igrac X je na potezu") if igrac1_na_potezu is True else print("Igrac O je na potezu")

        placed_correctly: bool = game.play_a_turn()
        while not placed_correctly:
            print("Nevalidan potez, pokusajte ponovo!")
            placed_correctly: bool = game.play_a_turn()
        igrac1_na_potezu = not igrac1_na_potezu
