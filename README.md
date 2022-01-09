<p align="center">
  <img src="https://user-images.githubusercontent.com/77248387/148674772-f9b01ba4-74ee-4d78-b468-c55c35dde741.jpg" width="450" height="190">
</p>

# Pokemon Game - Ex4
#### Noamya Shani and Eitan Shenkolevski


### Abstract
In this project we design a "Pokemon game" where given a weighted graph, a group of "agents" must be placed on it so that they can "catch" as much "Pokemon" as possible. The Pokemon are placed at the (directed) edges of the graph, therefore, the agent must take (also known to walk) the appropriate edge to "catch" the Pokemon.
The game is run in the form of a client and server. The server keeps the data and updates it all the time, and the client receives information from the server and sends commands back to the server (such as where to send the agent and when to move it).
To run the program, we created several classes, some secondary and some central - the secondary classes are `Pokemon`, `Agent` designed to create Pokemon or Agent what json object the server gives, and `edge_pok` class which we use to know How many Pokemon values ​​are at a certain end and have we already assigned him an agent.

The main classes are `Controller` and `PokemonGame`, where `Controller` is the main calculation of the agents' locations and their next step as well as giving the command when to move them. The role of the `PokemonGame` class is to draw the graph with the Pokemon and agents and to simulate the movement of the agents, the capture of the Pokemon and their reappearance in another location.
The structure of the project is done according to **MVC** so that the `PokemonGame` department draws the game according to data it receives from the `Controller`, and only the `Controller` has access to send and receive data from the server.
<br><br>
*UML of the project:*<br>
![image](https://user-images.githubusercontent.com/77248387/148674616-9f4ffb04-9091-443c-8453-c8c559828b9d.png)

Controller class:
In this class we first built a basic build of the game, made a connection to the server and then kept the data with us - we got the data on Pokemon locations and value, and plotted by edge how many 'Pokemon' values ​​there are on it, then sorted by values ​​(from high to low).
We then add agents (the amount given in json given by the server) and place them according to the sorted array of the edges on which the Pokemon are located. If there are more agents left place them randomly.
We keep a list of each agent's his path so we can always know what his next step is. First we will list the source of the edge to which it is embedded.
In the 'get_next' function we return the next node to which the agent has to go according to the data that appears in his path.
In the 'on_edge' function we calculate according to the position of the Pokemon on which edge it is located.
In the 'attach' function we sort the edgepoke according to their value, and the agents according to their speed and then insert each suitable edge agent so that the fastest agent gets the edge with the highest value. After we have assigned an agent to each edge we update the agent's its trajectory by adding the 'shortestpath' between the agent's location and the source of the edge. We will also indicate that this edge has already been assigned an agent.
In the 'moving' function we basically schedule when the agents will perform 'movement'. We check if the agent's distance from the Pokemon is close enough for him to 'capture' him in the same 'movement', and we also inform the server what the next step the agent should do. At the end we make sure that the amount of 'moves' does not exceed the required limit of an average of 10 'moves' per second.
Note that in order to create a graph and execute algorithms on it, we used the 'networkx' library.
In the 'Gui' class we implemented the graphical interface of the game. We used 'pygame' for that.
We initialized a Controller variable and from it we got the data on the graph, the Pokemon and the agents. We drew the nodes and edges as well as the Pokemon and agents (Pikachu if the dest of the edge is larger than the source, and otherwise 'Squirtle'. 'Pokeball' represents the agents.)
Also appear on the screen the time left for the game, the score and the amount of 'moves' made. There is also a 'stop' button where you can stop the game at any given moment.
During the game run we constantly re-insert the agents (by the 'attach' function) and perform 'moves' taking into account the time left for the game.
Run the program-
In order to run the program, the following command must be entered in the command line-
'java -jar Ex4_Server_v0.0.jar 0' (where the last digit represents which 'case' you want to run, there are 16 cases). After giving the command, one should run the Ex4.py file and then the game will start running.
