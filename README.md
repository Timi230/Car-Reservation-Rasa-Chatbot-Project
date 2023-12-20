# Car-Reservation-Rasa-Chatbot-Project

Welcome to the repository for my car reservation chatbot project, completed during my international semester where I took a course on databases and deep learning. This project allowed me to deepen my knowledge of databases and explore the TensorFlow library. The creation of the chatbot was done using the Rasa tool, enabling the development of assistants with artificial intelligence.

## Context

During the course, I had the opportunity to delve into databases and explore TensorFlow, a powerful library for deep learning. The final project for the course involved developing a chatbot connected to a database.

## The Chatbot

For this project, I chose to create a car reservation chatbot. Two tables were at my disposal, one containing the list of cars and the other the list of agencies. I used the Rasa tool to implement this chatbot, adding a layer of artificial intelligence to my interactions.

## Repository Structure

- **`data/` :** Contains all YAML files used for training the chatbot.

- **`actions/` :** Contains Python source files used to create custom actions for the chatbot.

- **`models/` :** Contains the chatbot models.

## Installation

To install the project, follow these steps:

1. Create a Python virtual environment with the command:
    ```bash
    python3 -m venv .venv
    ```

2. Clone the Git repository:
    ```bash
    git clone https://github.com/Timi230/Car-Reservation-Rasa-Chatbot-Project
    ```

3. Install the necessary libraries:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the actions server and launch the chatbot shell:
    ```bash
    rasa run actions
    rasa shell
    ```

## Contributions

Contributions are welcome! If you have ideas for improvement, report issues, or submit pull requests.
