import argparse
import os
import pickle
import sys

from tictactoe.agent import Qlearner, SARSAlearner
from tictactoe.teacher import Teacher
from tictactoe.game import Game


class GameLearning(object):
    """
    A class that holds the state of the learning process. Learning
    agents are created/loaded here, and a count is kept of the
    games that have been played.
    """
    def __init__(self, args, alpha=0.5, gamma=0.9, epsilon=0.1):

        if args.load:
            # load an existing agent and continue training
            if not os.path.isfile(args.path):
                raise ValueError("Cannot load agent: file does not exist.")
            try:
                with open(args.path, 'rb') as f:
                    agent = pickle.load(f)
            except (pickle.UnpicklingError, EOFError) as e:
                raise ValueError("Failed to load the agent: {}".format(e))
        else:
            # check if agent state file already exists, and ask
            # user whether to overwrite if so
            if os.path.isfile(args.path):
                print('Agen sudah disimpan di {}.'.format(args.path))
                while True:
                    response = input("Apakah Anda yakin ingin menimpa? [y/n]: ")
                    if response.lower() in ['y', 'yes']:
                        break
                    elif response.lower() in ['n', 'no']:
                        print("OK. Keluar.")
                        sys.exit(0)
                    else:
                        print("Masukkan tidak valid. Silahkan pilih 'y' atau 'n'.")
            if args.agent_type == "q":
                agent = Qlearner(alpha,gamma,epsilon)
            else:
                agent = SARSAlearner(alpha,gamma,epsilon)

        self.games_played = 0
        self.path = args.path
        self.agent = agent

    def beginPlaying(self):
        """ Loop through game iterations with a human player. """
        print("Selamat datang di permainan Tic-Tac-Toe. Kamu adalah 'X' dan komputer adalah 'O'.")

        def play_again():
            print("Permainan yang dimainkan: %i" % self.games_played)
            while True:
                play = input("Apakah kamu ingin bermain lagi? [y/n]: ")
                if play == 'y' or play == 'yes':
                    return True
                elif play == 'n' or play == 'no':
                    return False
                else:
                    print("Masukkan tidak valid. Silahkan pilih 'y' atau 'n'.")

        while True:
            game = Game(self.agent)
            game.start()
            self.games_played += 1
            self.agent.save(self.path)
            if not play_again():
                print("OK. Keluar.")
                break

    def beginTeaching(self, episodes):
        """ Loop through game iterations with a teaching agent. """
        teacher = Teacher()
        # Train for alotted number of episodes
        while self.games_played < episodes:
            game = Game(self.agent, teacher=teacher)
            game.start()
            self.games_played += 1
            # Monitor progress
            if self.games_played % 1000 == 0:
                print("Permainan yang dimainkan: %i" % self.games_played)
                self.agent.save(self.path)  # Save progress periodically
        # save final agent
        self.agent.save(self.path)


if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Play Tic-Tac-Toe.")
    parser.add_argument('-a', "--agent_type", type=str, default="q",
                        choices=['q', 's'],
                        help="Specify the computer agent learning algorithm. "
                             "AGENT_TYPE='q' for Q-learning and AGENT_TYPE='s' "
                             "for Sarsa-learning.")
    parser.add_argument("-p", "--path", type=str, required=False,
                        help="Specify the path for the agent pickle file. "
                             "Defaults to q_agent.pkl for AGENT_TYPE='q' and "
                             "sarsa_agent.pkl for AGENT_TYPE='s'.")
    parser.add_argument("-l", "--load", action="store_true",
                        help="whether to load trained agent")
    parser.add_argument("-t", "--teacher_episodes", default=None, type=int,
                        help="employ teacher agent who knows the optimal "
                             "strategy and will play for TEACHER_EPISODES games")
    parser.add_argument("--alpha", type=float, default=0.5, help="Learning rate")
    parser.add_argument("--gamma", type=float, default=0.9, help="Discount factor")
    parser.add_argument("--epsilon", type=float, default=0.1, help="Exploration rate")
    
    args = parser.parse_args()

    # Validate input for teacher_episodes
    if args.teacher_episodes is not None and args.teacher_episodes <= 0:
        raise ValueError("Number of teacher episodes must be a positive integer.")

    # set default path
    if args.path is None:
        args.path = 'q_agent.pkl' if args.agent_type == 'q' else 'sarsa_agent.pkl'

    # initialize game instance with custom parameters
    gl = GameLearning(args, alpha=args.alpha, gamma=args.gamma, epsilon=args.epsilon)

    # play or teach
    if args.teacher_episodes is not None:
        gl.beginTeaching(args.teacher_episodes)
    else:
        gl.beginPlaying()
