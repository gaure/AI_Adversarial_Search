"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(state, player):
    # TODO: finish this function!
    #raise NotImplementedError
    return float(len(state.get_legal_moves(player)))


def custom_score_2(state, player):
    # TODO: finish this function!
    return float(len(state.get_legal_moves(player)) -
                 len(state.get_legal_moves(state.get_opponent(player))))


def custom_score_3(state, player):
    # TODO: finish this function!
    return float(len(state.get_blank_spaces()))
    #my_moves = len(state.get_legal_moves(player))
    #return float(remaining_spaces - my_moves)
    #return float(len(state.get_legal_moves(player)) -
    #             len(state.get_legal_moves(state.get_opponent(player))))
    


class IsolationPlayer:
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1,-1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return  self.minimax(game, self.search_depth)
        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # TODO: finish this function!
        # Max function

        legal_moves = game.get_legal_moves()
        def max_play(state,depth):
            # Cut-off function, time, terminal node, depth
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()

            if depth == 0 or not state.get_legal_moves():
                return self.score(state,self)

            # Set the score to a small number
            best_score = float('-inf')
            # Iterate over Max moves and calculate best score
            for a in state.get_legal_moves():
                best_score = max(best_score, min_play(state.forecast_move(a),
                                                       depth-1))
            # Return best score
            return best_score

        # Min function 
        def min_play(state,depth):
            # Cut off function by time, termina state  and depth
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            
            if  depth == 0 or not state.get_legal_moves():
                return self.score(state,self) 

            # Set the score to a big number
            best_score = float('inf')
            #Iterate over Min moves and return the worst score
            for a in state.get_legal_moves():
                best_score = min(best_score, max_play(state.forecast_move(a),
                                                       depth-1))
            # Return the smallest score
            return best_score
        return max(legal_moves, key=lambda a: min_play(game.forecast_move(a),
                                   depth-1)) if legal_moves else (-1,-1)

    



class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        self.time_left = time_left

        # TODO: finish this function!
        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1,-1)
        try:
            depth=1
            while True:
                best_move =  self.alphabeta(game, depth)
                depth = depth+1
        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # TODO: finish this function
        # AlphaBeta function

        ########################### 
        #### MAX_Play function ####
        ###########################
        def max_play(state,depth,alpha,beta):
            # Cut-off function, time, terminal node, depth
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()

            if depth == 0 or not state.get_legal_moves():
                return self.score(state,self)

            # Set the score to a small number
            best_score = float('-inf')
            # Iterate over Max moves and calculate best score
            for a in state.get_legal_moves():
                best_score = max(best_score, min_play(state.forecast_move(a),
                                                       depth-1,alpha,beta))
                # Check if best_score is greater than beta on this branch
                # If greater return the best score as the lower boundary
                # and stop searching this branch
                if best_score >= beta:
                    return best_score
                # Make alpha the bigger between alpha and the 
                # best score
                alpha = max(alpha,best_score)
            # Return best score
            return best_score

        ########################### 
        #### MIN_Play function ####
        ###########################
        def min_play(state,depth,alpha,beta):
            # Cut off function by time, termina state  and depth
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            
            if  depth == 0 or not state.get_legal_moves():
                return self.score(state,self) 

            # Set the score to a big number
            best_score = float('inf')
            #Iterate over Min moves and return the min of the best  score
            for a in state.get_legal_moves():
                best_score = min(best_score, max_play(state.forecast_move(a),
                                                       depth-1,alpha,beta))
                # Check if best score is less or equal to the upper limit
                # if less return best_score
                if best_score <= alpha:
                    return best_score
                # Make beta equal to the smallest number between the
                # best_score and the value of the lower boundary
                beta = min(beta,best_score)
            # Return the smallest score
            return best_score

        ########################### 
        #### ALPHABETA ROOT    ####
        ###########################
        legal_moves = sorted(game.get_legal_moves())
        #return max(legal_moves, key=lambda a: min_play(game.forecast_move(a),
        #                           depth,alpha,beta)) if legal_moves else (-1,-1)
        best_score = float('-inf')
        if len(legal_moves) != 0:
            best_action = legal_moves[0]
            for a in legal_moves:
                move = a
                score = min_play(game.forecast_move(a),
                                      depth-1,alpha,beta)
                alpha = max(score,alpha)
                if score > best_score:
                    best_score = score
                    best_action = a
            return best_action
        else:
            return (-1,-1)

#if __name__ == "__main__":
#    from isolation import Board
#    from sample_players import RandomPlayer
#    from sample_players import GreedyPlayer
#    from sample_players import HumanPlayer
#    from game_agent import AlphaBetaPlayer
#
#
#    player1 = AlphaBetaPlayer() 
#    player2 = RandomPlayer()
#    game = Board(player1,player2)
#    game.apply_move((3,2))
#    game.apply_move((0,0))
#
#    winner,history, outcome = game.play()
#    print ("\nWinner: {}\nOutcome: {}".format(winner,outcome))
#    print (game.to_string())
#    print("Move history:\n{!s}".format(history))
