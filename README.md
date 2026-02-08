# CineBook
CineBook is a web-based movie ticket booking system developed using Python (Flask) that allows users to browse movies, view show timings, select seats, and book tickets online. The system supports both normal movies and kids movies, with dynamic seat selection, multiple screens, and real-time booking management.

The project is designed with a strong focus on Data Structures and Algorithms, where core functionalities such as movie search, seat management, undo operations, show handling, and booking history are implemented using Binary Search Tree (BST), Linked List, Stack, Queue, and Graphs. Online payments are integrated using Stripe, making the booking process secure and user-friendly.

Backend & Frontend Technologies :-

 Backend :-

Python – Core programming language used for backend logic
Flask – Lightweight web framework for handling routes, requests, and responses
Data Structures (In-Memory Storage)
Binary Search Tree (BST) – Efficient movie search
Linked List – Dynamic seat selection handling
Stack – Undo functionality for seat selection
Queue – Booking history management
Graph – Movie show scheduling and relationships
Stripe API – Online payment integration for secure transactions

 Frontend :-

HTML5 – Structure of the web pages
CSS3 – Styling and layout
Jinja2 – Template engine for rendering dynamic content
JavaScript – Client-side interactions and form handling

 Note on Data Persistence:-
 Install Flask and Stripe using pip, then start the application by running python app.py to launch the CineBook movie ticket booking system.
This application uses in-memory data storage implemented through Python data structures. All booking details, seat availability, and history are stored temporarily during runtime and are cleared when the server is stopped or restarted. This design choice was made intentionally to demonstrate the practical use of Data Structures and Algorithms rather than focusing on database integration.
