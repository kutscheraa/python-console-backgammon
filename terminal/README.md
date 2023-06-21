# Backgammon
Minimal implementation of backgammon in Python.

Run the game in console using `python main.py`. The program automatically determines legal moves and allows players to choose among them. The interface is pretty ugly, but it gets the job done.

A few quirks:
- To play a move, you enter the corresponding start and end indices from the list shown. Some of the indices are a bit cryptic, such as for the bars and for bearing off.
- You can't currently move one checker more than one die at a time, so you will have to play each die separately.

Other than that, anything unexpected is probably a bug. Feel free to report it in an issue or submit a pull request if you so desire.

Enjoy!
