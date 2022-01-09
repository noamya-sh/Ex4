import subprocess
import sys
from PokemonGame import PokemonGame

"""
run file for pokemon game
"""
if __name__ == '__main__':
    args = sys.argv
    subprocess.Popen(['powershell.exe', 'java -jar Ex4_Server_v0.0.jar {}'.format(args[1])])
    PokemonGame()
