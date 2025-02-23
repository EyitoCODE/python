# Ayo Game

Ayo is a traditional mancala game played in West Africa. This project is a Python implementation of the game with a graphical user interface (GUI) built using tkinter. The game supports both Player vs Player (PvP) and Player vs AI (PvAI) modes, with adjustable difficulty settings for the AI. A restart button allows users to start a new game at any time.


## Features

- **Player vs Player (PvP):** Two human players can play against each other.
- **Player vs AI (PvAI):** Play against an AI with two difficulty settings: Easy and Hard.
- **Restart Button:** Quickly restart the game at any time.
- **Tutorial Prompt:** A built-in tutorial explains the game rules and how to play.
- **GUI:** A visual representation of the game board using tkinter.
- **Modular Code:** Organized into multiple files and classes for clarity and maintainability.

## How to Play

- **Game Board:**  
  The board consists of 12 pits. Pits 0 to 5 belong to Player 1, and pits 6 to 11 belong to Player 2. Each pit starts with 4 seeds.

- **Game Rules:**  
  1. On your turn, click one of your pits to sow the seeds counterclockwise around the board.
  2. If the last seed lands in an opponent's pit that has exactly 2 or 3 seeds, those seeds are captured.
  3. The game ends when one player's side is empty. The winner is the player with the most captured seeds.

- **Controls:**  
  - **Mode Selection:** Use the radio buttons to select between Player vs Player and Player vs AI.
  - **AI Difficulty:** Choose the desired difficulty level for the AI (Easy or Hard) when in PvAI mode.
  - **Restart:** Click the "Restart Game" button to start a new match.
  - **Tutorial:** Click the "Tutorial" button at any time to view game instructions.

## Thought Process & Development Journey

Growing up, I spent many afternoons playing Ayo with my sibling. Those moments of strategizing, laughter, and healthy competition inspired me to recreate the game in a digital format. While building this project, I encountered challenges in translating the traditional game rules into code, especially when implementing the capture mechanism. This project is not only a tribute to my childhood memories but also a learning experience in structuring a project with clean, modular code.

## Challenges

- **Implementing Game Rules:** Translating the complex traditional rules of Ayo into a programmatic format required careful consideration and testing.
- **AI Development:** Creating an AI that provided a challenging yet fair experience in both easy and hard modes.
- **GUI Design:** Balancing simplicity with functionality in the tkinter-based GUI to ensure a smooth user experience.

## Future Improvements & Roadmap

### Short-Term Enhancements

- **Sound Effects & Music:** Add background music and sound effects for moves, captures, and game over.
- **Better Animations:** Implement smooth animations for seed distribution and captures to enhance visual appeal.
- **Enhanced AI:** Develop a more sophisticated AI using algorithms like Minimax for a more challenging gameplay experience.

### Long-Term Roadmap

1. **Online Browser Game:**
   - **Backend Development:** Use frameworks like Django or Flask to create server-side game logic.
   - **Frontend Development:** Develop a responsive web interface using React or Vue.js.
   - **Real-Time Multiplayer:** Implement WebSocket support (e.g., using Socket.IO) to allow real-time online multiplayer games.

2. **Mobile App (iOS and Android):**
   - **Cross-Platform Framework:** Use frameworks like Flutter or React Native to create a mobile version.
   - **Touch Controls & Gestures:** Adapt the game controls to be intuitive for touch interfaces.
   - **In-App Purchases & Ads:** Integrate monetization strategies while ensuring a fun user experience.

3. **Cloud Integration:**
   - **Online Leaderboards:** Introduce online leaderboards to track high scores and competitive play.
   - **User Accounts:** Allow users to save progress, customize themes, and challenge friends.

# Author
- Oritse-tsegbemi Eyito
