# To-Do List Application

A simple To-Do List application built using Flask for the web interface and MongoDB Atlas for data storage. Users can register, log in, manage tasks, and set reminders.

## Features

- **User Authentication**: Users can register and log in with their credentials.
- **Task Management**: Add, start, complete, and delete tasks.
- **Task Status**: Organize tasks into pending, ongoing, and completed categories.
- **Reminders**: Set reminders for tasks (optional).
- **User Interface**: Clean and responsive UI with Bootstrap.

## Technologies Used

- **Python**: Flask web framework.
- **MongoDB Atlas**: Cloud-based database for storing user and task data.
- **Bootstrap**: For styling and responsive design.

## Installation

### Prerequisites

- Python 3.6 or higher
- Flask
- pymongo
- Bootstrap (included via CDN)

### Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/nishantddubey/todo-list.git
   cd todo-list
    ```
2. **Create a Virtual Environment**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```
3. **Install Required Packages**

    ```bash
    pip install flask pymongo
    ```

4. **Configure MongoDB Atlas/Local**

    Ensure you have a MongoDB Atlas account or MongoDB on local.
    Create a new database and note the connection string.
    Replace the connection string in app.py with your MongoDB Atlas connection string.

5. **Run the Application**
    ```bash
    python app.py
    ```


## Usage

**Register:**
Go to the /register page to create a new account.

**Login:**
After registration, log in at the /login page.

**Manage Tasks:**

Add: Use the form on the home page to add a new task.
Start: Move tasks from pending to ongoing.
Complete: Mark tasks as completed.
Delete: Remove tasks from any status.