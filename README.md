
![ezgif com-gif-maker](https://user-images.githubusercontent.com/77248387/148675942-80ada8b0-3f19-43ee-9326-0645ddae2838.gif)


# Pokemon Game - Ex4
#### Noamya Shani and Eitan Shenkolevski


### Abstract
In this project we design a "Pokemon game" where given a weighted graph, a group of "agents" must be placed on it so that they can "catch" as much "Pokemon" as possible. The Pokemon are placed at the (directed) edges of the graph, therefore, the agent must take (also known to walk) the appropriate edge to "catch" the Pokemon.
The game is run in the form of a client and server. The server keeps the data and updates it all the time, and the client receives information from the server and sends commands back to the server (such as where to send the agent and when to move it).<br><br>
To run the program, we created several classes, some secondary and some central - the secondary classes are `Pokemon`, `Agent` designed to create Pokemon or Agent what json object the server gives, and `edge_pok` class which we use to know How many Pokemon values ​​are at a certain end and have we already assigned him an agent.

The main classes are `Controller` and `PokemonGame`, where `Controller` is the main calculation of the agents' locations and their next step as well as giving the command when to move them. The role of the `PokemonGame` class is to draw the graph with the Pokemon and agents and to simulate the movement of the agents, the capture of the Pokemon and their reappearance in another location.
The structure of the project is done according to **MVC** so that the `PokemonGame` department draws the game according to data it receives from the `Controller`, and only the `Controller` has access to send and receive data from the server.
<br><br>
*UML of the project:*<br>
![image](https://user-images.githubusercontent.com/77248387/148674616-9f4ffb04-9091-443c-8453-c8c559828b9d.png)

### Run Game
1. Make sure your python has 'Numpy', 'Pygame', and 'Networkx' libraries installed.
2. Download rar of the project from here __
3. Open 2 cmd windows from the folder to which you extracted the files. First run - 
 ```
java -jar Ex4_Server_v0.0.jar <[0-15]>
```
When at the end you have to choose a digit that represents the case you want to run.
In the second window run -
 ```
python Ex4.py
```


### Classes and functions
* **`Controller`**:<br>
In this class we first built a basic build of the game, made a connection to the server and then kept the data with us - we got the data on Pokemon locations and value, and plotted by edge how many 'Pokemon' values ​​there are on it, then sorted by values ​​(from high to low).
We then add agents (the amount given in json given by the server) and place them according to the sorted array of the edges on which the Pokemon are located. If there are more agents left place them randomly.
We keep a list of each agent's his path so we can always know what his next step is. In init function of controller we will list the source of the edge to which it is embedded.
In *'init_graph'* you initialize a graph from the json format to a weighted directed graph from the networkx directory
In the *'get_next'* function we return the next node to which the agent has to go according to the data that appears in his path.<br>
In the *'find_edge'* and *'on_edge'* function we calculate according to the position of the Pokemon on which edge it is located.<br>
In the '*attach'* function we sort the edgepoke according to their value, and the agents according to their speed,
and then insert each suitable edge agent so that the slowest agent gets the edge with the highest value (In order to reach the maximum speed of all agents). After we have assigned an agent to each edge we update the agent's its trajectory by adding the 'shortestpath' between the agent's location and the source of the edge. We will also indicate that this edge has already been assigned an agent.<br>
In the *'moving'* function we basically schedule when the agents will perform 'movement'. We check if the agent's distance from the Pokemon is close enough for him to 'capture' him in the same 'movement', and we also inform the server what the next step the agent should do. At the end we make sure that the amount of 'moves' does not exceed the required limit of an average of 10 'moves' per second.<br>
The rest of the functions are used to get specific data from the server (like *'get_pokemons'*, *'get_time_to_end'* etc.)
Note that in order to create a graph and execute algorithms on it, we used the `networkx` library.<br><br>
* **`PokemonGame`**:<br>
In this class we implemented the graphical strcture of the game. We used `pygame` and `Numpy` libraries for that.
We initialized a `Controller` variable and from it we got the data of the graph. As long as the controller is connected to the server (ie the game is not over), we will get information about the locations of the agents and Pokemon, drew the nodes and edges and on them the Pokemon and agents (Pikachu if the src id of the edge is larger than the dest id, and otherwise 'Squirtle'. 'Pokeball' represents the agents.)
Also appear on the screen the time left for the game, the score and the sum of the 'move' commands sent to the server. There is also a 'stop' button where you can stop the game at any given moment.
In addition, we wrote functions for drawing a line and an arrow and performing a scale to position.<br>
Agent and Pokemon moves are not controlled by PokemonGame but are controlled by the controller. In PokemonGame we will only send a request to the controller to update the information in his possession.

<br><br>

### Performances
|**case**|**grade**|
| :-: | :-: |
|0|147|
|1|464|
|2|286|
|3|861|
|4|211|
|5|550|
|6|79|
|7|310|
|8|125|
|9|395|
|10|59|
|11|1679|
|12|40|
|13|369|
|14|226|
|15|310|
