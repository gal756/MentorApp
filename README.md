## Mentor Web App

Welcome to the Code Mentor Web App, a platform designed to facilitate remote coding sessions between mentors and students.

## Introduction:
The Mentor Web App is a collaborative coding platform designed to facilitate remote coding sessions between mentors and students. The primary goal is to create an interactive and real-time coding environment that allows mentors to share code, observe students as they code, and provide guidance during coding sessions.

## Features:
1.Lobby for Code Block Selection: Users, both mentors, and students start on a lobby page where they can choose from a list of code blocks.each code block represent aproblem from the Database.  
2.Individual Code Block Pages: After selecting a code block, users are directed to an individual page dedicated to that specific code block.  
3.Real-Time Code Changes: The web app employs a Socket connection to enable real-time code changes. This feature ensures that both mentors and students can see code modifications instantly.  
4.Syntax Highlighting: The app supports syntax highlighting for JavaScript code, enhancing the readability and understanding of the code snippets.  
5.User Roles: Users are categorized into mentors and students. Mentors have a read-only view of the code block, while students can actively make changes. This distinction allows for a structured learning environment.

## How It Works:
1.Lobby Selection: Users recognize as student or mentor after the get into the lobby and choose a specific code block they want to work on or discuss.  
2.Individual Code Block Page: Upon selection, users are redirected to a dedicated page for the chosen code block. The mentor, who initiates the session, sees a read-only version, while the student sees an editable version.  
3.Real-Time Collaboration: As the student makes changes to the code, the mentor can observe these modifications in real-time. This allows for immediate feedback and guidance. 
 
 4.Enhanced Learning: The web app aims to create an immersive learning experience by combining real-time collaboration, syntax highlighting, and a structured workflow between mentors and students.

## Technologies Used:
Backend:  
1.Flask (Python web framework)  
2.Flask-SocketIO for WebSocket communication  
3.psycopg2 for PostgreSQL database interaction  
Frontend:  
1.HTML, CSS, and JavaScript  
2.Prism.js for syntax highlighting

## Contributing:
The project is open to contributions. If you'd like to contribute, please follow the guidelines outlined in the project repository.

## License
This project is licensed under the MIT License, providing flexibility for usage and contributions.

## Author

This web application was developed by Gal Evgi.

- gal756@gmail.com
- https://github.com/gal756

Feel free to reach out for questions, feedback, or collaboration!
