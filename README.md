🧠 Gomoku AI – Human vs AI and AI vs AI (Minimax & Alpha-Beta)

This is a Gomoku game implemented in Python using Tkinter, featuring two AI strategies:

    Minimax Algorithm (Black)

    Alpha-Beta Pruning (Red)

Players can choose to either:

    Play as a human against the AI

    Watch an AI vs AI battle between two different algorithms.

🎮 Features:

    Intuitive GUI built with Tkinter

    Beautiful, customizable background (image loading optional)

    Human vs AI Mode: Play against a Minimax-powered AI

    AI vs AI Mode: Watch Minimax (Black) play against Alpha-Beta (Red)

    Custom evaluation functions and optimized move search using depth-limited algorithms

    Dynamic move generation and smart scoring heuristics

🤖 Algorithms Used:

    Minimax with depth-limited search and a basic evaluation function

    Alpha-Beta Pruning to optimize decision-making and reduce computation

    Both AIs assess board positions based on sequence patterns (2-in-a-row to 5-in-a-row)

🛠️ Requirements:

    Python 3.x

    Pillow for image handling (pip install Pillow)

    Tkinter (usually included with Python)

📷 Optional:

Add your own background image by replacing the file path in:

image_path = r"C:\Your\Path\To\bg.jpeg" 

    
