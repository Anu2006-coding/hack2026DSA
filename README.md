Problem 1: Maze Solver Using Shortest Path Algorithm

📌 Problem Statement

Design and implement a maze-solving program that finds the shortest path from the starting point to the destination while avoiding walls and obstacles. The maze contains open paths, blocked cells, and special doors and keys. The algorithm must determine a valid shortest route based on the movement rules and key-door constraints.

🎯 Objectives

- Represent the maze using a grid.
- Identify the starting point and destination.
- Find the shortest valid path through the maze.
- Avoid walls and blocked cells.
- Handle keys and doors according to the problem rules.
- Display the shortest path length and path coordinates.
- Save the maze and path output in CSV files.

⚙️ Features

- Generate or load a maze from a CSV file.
- Support different maze configurations.
- Find a shortest valid path to the destination.
- Consider keys and doors when exploring possible routes.
- Display the generated maze and shortest path information.
- Export maze data and path results to CSV files.

🛠️ Technologies Used

- Programming Language: Python
- Data Storage: CSV files
- Development Environment: Visual Studio Code
- Algorithm: Shortest-path search with key-and-door state handling, as implemented in the program.

📂 Project Structure

problem1_Maze/
├── main.py
├── maze.csv
├── path_output.csv
├── output1.png
├── output2.png
└── README.md

The screenshot files are optional. Include them only if you have saved valid images.

▶️ How to Run

1. Install Python 3 on your system.

2. Open the project folder in VS Code.

3. Open the integrated terminal.

4. Run the following command:
   
   python main.py

5. Follow the displayed instructions to select a maze option and provide any requested parameters.

6. View the generated maze, shortest path length, and path coordinates in the terminal.

📊 Output

The program displays:

- The generated or loaded maze.
- The shortest path length.
- The coordinates of the path from the starting point to the destination.
- The saved maze file and path output file.

The output files "maze.csv" and "path_output.csv" store the maze representation and path-related results, respectively.

⏱️ Algorithm Analysis

The algorithm explores reachable maze states to find the shortest valid route. If keys and doors are present, the search must track the keys collected along each route so that a door is traversed only when its required key is available.

For an ordinary unweighted grid, Breadth-First Search (BFS) finds a shortest path. When key collection affects which moves are valid, the search state must include both the current position and the keys collected. The exact time and space complexity depend on the implemented search algorithm and number of key states.

✅ Validation

The program can be tested using:

- A maze with a direct path to the destination.
- A maze containing walls and dead ends.
- A maze with multiple possible routes.
- A maze with keys and locked doors.
- A maze where no valid path exists.

The result should be a shortest valid path that follows all movement and key-door constraints.

🚀 Future Enhancements

- Add a graphical user interface for maze visualization.
- Highlight the shortest path directly on the maze.
- Compare BFS with other search algorithms.
- Display execution time and memory usage.
- Provide interactive maze generation and testing.

🏁 Conclusion

The Maze Solver project demonstrates how graph-search algorithms can solve pathfinding problems. By representing the maze as a grid and accounting for obstacles and key-door constraints, the program identifies a shortest valid route and saves relevant results for analysis.