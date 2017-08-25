from isolation import Board
from sample_players import RandomPlayer
from sample_players import GreedyPlayer
from collections import deque
import pprint


def find_all_paths(graph, start, end, path=[]):
    path = path + [start]
    # If the start is the end return list of paths
    if start == end:
        return [path]
    # If the start value is not in the original
    # graph return nothing.
    if start not in  graph:
        return None
    # Initializa an empty list for the paths
    paths = []
    # Iterate over the children of the start node
    for node in graph[start]:
        if node not in path:
            # Call itself, this time passing the children
            # of the start node
            newpaths = find_all_path(graph, node, end, path)
            # For each node children append it to the list of paths
            for newpath in newpaths:
                paths.append(newpath)
    return paths

player1 = RandomPlayer()
player2 = GreedyPlayer()
game = Board(player1,player2)

game.apply_move((2,3))
game.apply_move((0,5))

# graph = {'A': ['B','C'], 'B': ['D','E'], 'E':['F']}
tree_list = []
level = 0
depth = 1
def create_children(state, children, tree, root_children=""):
    # If children is None this is the root node children.
    if children == None:
        # Assign the root node childre to node
        children = sorted(state.get_legal_moves(player1))
        # Place holder to hold the root children to use it
        # to parse its silblings
        root_children = deque(children)
    # Create the tree as a dictionary with the player loc as nodes and
    # succesors as valid action. Sorted the actions to always create
    # the tree from left to right.
    tree[state.get_player_location(player1)]=sorted(children)
    # Define a based case to stop the tree creation based on levels
    if len(tree) == 47:
        return tree
    # Every iteration that is not the first create the succesors
    # of the state as a list of legal actions
    children = state.get_legal_moves(player1)
    # For each child run the recursive function
    for child in sorted(children):
        # Create the succesors of each child
        children = (state.forecast_move(child)).get_legal_moves(player1)
        # Check if the child does not have successors, this means this is
        # a leave of the tree.
        if len(children) == 0:
            # Add leave to the tree
            tree[(state.forecast_move(child)).get_player_location(player1)] =\
            child
            # Check if there is still root node siblings
            if len(root_children) != 0:
                # Move to next siblin of the root node
                children = list(root_children.popleft())
            else:
                return tree
        return create_children(state.forecast_move(child),children,tree)



def minimax(game_state):
    moves = game_state.get_legal_moves()
    best_move = moves[0]
    best_score = float('-inf')
    for move in moves:
        clone = game.forecast_move(move)
        score = min_play(clone)
        if score > best_score:
            best_move = move
            best_score = score
    return best_move
    
def min_play(game_state):
    if game_state.is_winner(player1):
        return 100
    moves = game_state.get_legal_moves()
    best_score = float('-inf')
    for move in moves:
        clone = game_state.forecast_move(move)
        score = max_play(clone)
        if score < best_score:
            best_move = move
            best_score = score
    return best_score

def max_play(game_state):
    if game_state.is_loser(player1):
        return -1
    moves = game_state.get_legal_moves()
    best_score = float('-inf')
    for move in moves:
        clone = game_state.forecast_move(move)
        score = min_play(clone)
        if score > best_score:
            best_move = move
            best_score = score
    return best_score

def evaluate(game_state):
    return game_state.get_legal_moves()


#pprint.pprint(create_children(game,children=None, tree={}))
pprint.pprint(minimax(game))

