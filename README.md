# artificial-incompetence-project-1

Github Repository URL: https://github.com/TheGreatMarkus/artificial-incompetence-project-1.git

Project 1 for Team Artificial Incompetence for the COMP472 class

# Instructions

1. Clone the project:
    * `git clone https://github.com/TheGreatMarkus/artificial-incompetence-project-1.git`

2. Change directory to the project folder:
    * `cd artificial-incompetence-project-1`
    
3. Make sure that numpy for python3 is installed:
    * If not, install it using pip: `pip3 install numpy`

4. Create an `input.txt` file in the root directory of the project with the input boards

5. Run the project:
    * DFS: `python3 dfs.py`
    * BFS: `python3 bfs.py "heuristic"`
    * A*: `python3 a_star.py "heuristic"`
    * Possible values for `"heuristic"` are `zero-h`, `count-h`, `div-5-h` or `no-dbl-press-h`

6. Generated data about the runs will be found in the folder `output/`