
from random import randint

"""
TODO: 1) Allow for multiple players
      2) Allow for board-sizes larger than 3x3
      3) Allow computer vs computer (skilled and random player)
      4) Prioritize 3 in a row for self over opponent
"""

class Board:
    def __init__(self, dimension):
        self._board = self.create_board(dimension)
        self._dimension = dimension
        self._number_of_moves = 0


    def move(self, row, column, piece):
        """ Makes the move based on row and column and piece """

        if row < 0 or row >= self._dimension or column < 0 or column >= self._dimension or self._board[row][column] != ' ':
            print('Move cannot be made')
            return False
        else:
            self._board[row][column] = piece
            self._number_of_moves += 1


    def check_move(self, row, column):
        """ Determines if a move is possible """

        return self._board[row][column] == ' '


    def game_over(self):
        """ Determines if game has finished """

        if self._number_of_moves == 9:
            return True

        return self._number_of_moves == 9 or self.winner_found()


    def winner_found(self):
        """ Sees if there is a winner """

        first_row = self.find_three_in_row([self._board[0][0], self._board[0][1], self._board[0][2]])
        second_row = self.find_three_in_row([self._board[1][0], self._board[1][1], self._board[1][2]])
        third_row = self.find_three_in_row([self._board[2][0], self._board[2][1], self._board[2][2]])
        winner_in_rows = first_row or second_row or third_row

        first_column = self.find_three_in_row([self._board[0][0], self._board[1][0], self._board[2][0]])
        second_column = self.find_three_in_row([self._board[0][1], self._board[1][1], self._board[2][1]])
        third_column = self.find_three_in_row([self._board[0][2], self._board[1][2], self._board[2][2]])
        winner_in_columns = first_column or second_column or third_column

        first_diagonal = self.find_three_in_row([self._board[0][0], self._board[1][1], self._board[2][2]])
        second_diagonal = self.find_three_in_row([self._board[2][0], self._board[1][1], self._board[0][2]])
        winner_in_diagonals = first_diagonal or second_diagonal

        return winner_in_rows or winner_in_columns or winner_in_diagonals


    def find_three_in_row(self, row):
        """ Checks if a row has three in a row """

        if row[0] != ' ' and row[0] == row[1] and row[1] == row[2]:
            return True
        else:
            return False 


    def create_board(self, dimension):
        """ Creates the board based on dimension """

        board = []

        for i in range(dimension):
            row = []
            for j in range(dimension):
                row.append(' ')
            board.append(row)

        return board


    def get_empty_positions(self):
        """ Returns all available moves """

        empty_positions = []

        for i in range(self._dimension):
            for j in range(self._dimension):
                if self._board[i][j] == ' ':
                    empty_positions.append((i, j))

        return empty_positions


    def get_piece(self, row, column):
        """ Gets the piece in a given position """
        return self._board[row][column]

    def get_number_of_moves(self):
        """ Returns the number of moves since the beginning of game """
        return self._number_of_moves


    def get_dimension(self):
        """ Gets the Dimension of board """
        return self._dimension


    def print_board(self):
        """ Displays the board """

        print('-----'*self._dimension)
        for row in range(len(self._board)):
            print(' | ', end='')
            for column in range(len(self._board)):
                print(self._board[row][column], end=' | ')
            print('\n'+'-----'*self._dimension)
        print('\n')


class Player:
    """ Class Player for a Human"""

    def __init__(self, piece, opponents):
        self._piece = piece
        self._opponents = opponents


    def get_piece(self):
        return self._piece


    def move(self, board):
        move = input('Please enter a position to move using coordinates: i.e. 0,0 for top-left corner -> ').split(',')
        return (int(move[0]), int(move[1]))


class RandomPlayer(Player):
    """ Randommly makes moves """

    def move(self, board):
        """ Determines a random move for the player """

        move = (randint(0, board.get_dimension()-1), randint(0, board.get_dimension()-1))

        while not board.check_move(move[0], move[1]):
            move = (randint(0, board.get_dimension()-1), randint(0, board.get_dimension()-1))

        return move



class YellowJ(Player):
    """ Class that gives player some intelligence """

    def move(self, board):
        """ Determines the best move for the player """

        if board.get_number_of_moves() == 0:
            random_row = randint(0, 2)
            random_column = randint(0, 2)

            if random_row == 1 or random_column == 1:
                random_row = 1
                random_column = 1
            elif random_row == 2:
                random_row = board.get_dimension()-1

            if random_column == 2:
                random_column = board.get_dimension()-1

            move = (random_row, random_column)
        elif board.get_number_of_moves() == 1 or board.get_number_of_moves() == 2:
            if board.get_piece(1,1) == ' ':
                move = (1, 1)
            else:
                board_dimension = board.get_dimension()-1
                corners = [(0, 0), (0, board_dimension), (board_dimension, 0), (board_dimension, board_dimension)]
                corners = self.remove_filled_positions(corners, board)

                move = corners[randint(0, len(corners)-1)]
        else:
            move = self.check_for_winner(board)

            if move == (-1, -1):
                board_dimension = board.get_dimension()-1
                corner1_moves = self.remove_filled_positions([(0, 0), (2, 2)], board)
                corner2_moves = self.remove_filled_positions([(0, 2), (2, 0)], board)

                non_corner_moves = self.remove_filled_positions([(1, 0), (2, 1), (1, 2), (0, 1)], board)

                center_piece = board.get_piece(1, 1)
                corner_pieces = [board.get_piece(0, 0), board.get_piece(board_dimension, 0), board.get_piece(0, board_dimension), board.get_piece(board_dimension, board_dimension)]

                if corner_pieces[0] != self._piece and corner_pieces[0] != ' ' and corner_pieces[0] == corner_pieces[3]:
                    move = non_corner_moves[randint(0, 3)]
                elif corner_pieces[1] != self._piece and corner_pieces[1] != ' ' and corner_pieces[1] == corner_pieces[2]:
                    move = non_corner_moves[randint(0, 3)]
                elif len(corner2_moves) > 0 and corner_pieces[0] != self._piece and corner_pieces[0] == center_piece and corner_pieces[3] == self._piece:
                    move = corner2_moves[0]
                elif len(corner1_moves) > 0 and corner_pieces[1] != self._piece and corner_pieces[1] == center_piece and corner_pieces[2] == self._piece:
                    move = corner1_moves[0]
                elif len(corner1_moves) > 0 and corner_pieces[2] != self._piece and corner_pieces[2] == center_piece and corner_pieces[1] == self._piece:
                    move = corner1_moves[0]
                elif len(corner2_moves) > 0 and corner_pieces[3] != self._piece and corner_pieces[3] == center_piece and corner_pieces[0] == self._piece:
                    move = corner2_moves[0]
                else:
                    move = self.can_complete_two_in_row(board)

                    if move == (-1, -1):
                        move = (randint(0, board.get_dimension()-1), randint(0, board.get_dimension()-1))

                        while not board.check_move(move[0], move[1]):
                            move = (randint(0, board.get_dimension()-1), randint(0, board.get_dimension()-1))

        return move


    def check_for_winner(self, board):
        """ Determines if there is a move that will win the game for the player or opponent """

        potential_move = (-1, -1)

        # Find Potential Three in a Row for Rows
        first_row = [(0, 0), (0, 1), (0, 2)]
        first_row_index = self.can_complete_three_in_row(first_row, board)
        if first_row_index[0] >= 0:
            return first_row[first_row_index[0]]
        elif first_row_index[1] >= 0:
            potential_move = first_row[first_row_index[1]]

        second_row = [(1, 0), (1, 1), (1, 2)]
        second_row_index = self.can_complete_three_in_row(second_row, board)
        if second_row_index[0] >= 0:
            return second_row[second_row_index[0]]
        elif second_row_index[1] >= 0:
            potential_move = second_row[second_row_index[1]]

        third_row = [(2, 0), (2, 1), (2, 2)]
        third_row_index = self.can_complete_three_in_row(third_row, board)
        if third_row_index[0] >= 0:
            return third_row[third_row_index[0]]
        elif third_row_index[1] >= 0:
            potential_move = third_row[third_row_index[1]]


        # Find Potential Three in a Row for Columns
        first_column = [(0, 0), (1, 0), (2, 0)]
        first_column_index = self.can_complete_three_in_row(first_column, board)
        if first_column_index[0] >= 0:
            return first_column[first_column_index[0]]
        elif first_column_index[1] >= 0:
            potential_move = first_column[first_column_index[1]]

        second_column = [(0, 1), (1, 1), (2, 1)]
        second_column_index = self.can_complete_three_in_row(second_column, board)
        if second_column_index[0] >= 0:
            return second_column[second_column_index[0]]
        elif second_column_index[1] >= 0:
            potential_move = second_column[second_column_index[1]]

        third_column = [(0, 2), (1, 2), (2, 2)]
        third_column_index = self.can_complete_three_in_row(third_column, board)
        if third_column_index[0] >= 0:
            return third_column[third_column_index[0]]
        elif third_column_index[1] >= 0:
            potential_move = third_column[third_column_index[1]]


        # Find Potential Three in a Row for Diagonals
        first_diagonal = [(0, 0), (1, 1), (2, 2)]
        first_diagonal_index = self.can_complete_three_in_row(first_diagonal, board)
        if first_diagonal_index[0] >= 0:
            return first_diagonal[first_diagonal_index[0]]
        elif first_diagonal_index[1] >= 0:
            potential_move = first_diagonal[first_diagonal_index[1]]

        second_diagonal = [(2, 0), (1, 1), (0, 2)]
        second_diagonal_index = self.can_complete_three_in_row(second_diagonal, board)

        if second_diagonal_index[0] >= 0:
            return second_diagonal[second_diagonal_index[0]]
        elif second_diagonal_index[1] >= 0:
            potential_move = second_diagonal[second_diagonal_index[1]]

        return potential_move

    def can_complete_three_in_row(self, row_positions, board):
        """ Checks if there can be three in a row for a given position """

        row = [board.get_piece(row_positions[0][0], row_positions[0][1]), board.get_piece(row_positions[1][0], row_positions[1][1]), board.get_piece(row_positions[2][0], row_positions[2][1])]

        if row.count(' ') == 1 and row.count(self._piece) == 2:
            self_winner = row.index(' ')
        else:
            self_winner = -1


        if row.count(' ') == 1 and  row.count(self._piece) == 0:
            opponent_winner = row.index(' ')
        else:
            opponent_winner = -1
        
        return (self_winner, opponent_winner)

    # TODO: find a way to detect potential two in a two in a row
    def can_complete_two_in_row(self, board):
        """ Used to determine if two in a row can be made for two rows """

        row1 = [(0, 0), (0, 1), (0, 2)]
        row2 = [(1, 0), (1, 1), (0, 2)]

        return (-1, -1)

    def remove_filled_positions(self, positions, board):
        """ Removes positions that are already taken """

        new_positions = []
        for p in positions:
            if board.check_move(p[0], p[1]):
                new_positions.append(p)
        return new_positions



def computer_vs_computer(number_of_games, print_board=False):
    """ Run X number of games where computer plays against itself """
    games_won = 0
    games_lost = 0
    games_tied = 0

    for i in range(number_of_games):
        board = Board(3)
        players = [YellowJ('X', ['O']), RandomPlayer('O', ['X'])]
        
        if print_board:
            print('GAME', (i+1))

        while not board.game_over():
            player_to_move = players[board.get_number_of_moves()%2]
            move = player_to_move.move(board)

            board.move(int(move[0]), int(move[1]), player_to_move.get_piece())
            if print_board:
                board.print_board()

        if board.game_over() and board.winner_found():
            winner = players[(board.get_number_of_moves()+1)%2]
            
            if print_board:
                print('%s won' % (winner.get_piece()))

            if winner.get_piece() == 'X':
                games_won += 1
            else:
                games_lost += 1
        else:
            games_tied += 1

        if print_board:
            print()
            print('-------')


    print('%d - Games Won' % (games_won))
    print('%d - Games Lost' % (games_lost))
    print('%d - Games Tied' % (games_tied))


def human_vs_computer():
    """ Create a game for Human vs Computer """
    
    board, players = setup_game()
    board.print_board()

    while not board.game_over():
        player_to_move = players[board.get_number_of_moves()%2]
        move = player_to_move.move(board)

        board.move(int(move[0]), int(move[1]), player_to_move.get_piece())
        board.print_board()

    if board.game_over() and board.winner_found():
        print('Game Ended with \'%s\' Player Winning' % (player_to_move.get_piece()))
    else:
        print('Game Ended in a Draw.')

# TODO: Modify to allow more than 2 Players
# TODO: Modify to allow use of boards larger than 3x3
def setup_game():
    dimension = 3 #int(input('Please enter the size of the board: i.e. 3 for a 3x3 -> '))
    board = Board(dimension)

    first_player = input('Would you like to move first? yes or no -> ')

    if first_player.lower() == 'no':
        players = [YellowJ('X', ['O']), Player('O', ['X'])]
    else:
        players = [Player('X', ['O']), YellowJ('O', ['X'])]

    return board, players


if __name__ == '__main__':
    human_vs_computer()
    # computer_vs_computer(1000000, False)
