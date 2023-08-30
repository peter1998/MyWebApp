# My Web Application

## Getting Started

### Backend Setup

1. **Database Setup:**

   - Install MySQL and create a database named `your_database_name`.
   - Set up a `.env` file in the `backend` folder with the following environment variables:

     ```
     DB_USER=your_database_username
     DB_PASSWORD=your_database_password
     DB_HOST=your_database_host (e.g., localhost)
     DB_DATABASE=your_database_name
     ```

   - Run the `init_db()` function in `backend/database.py` to initialize the database schema.

2. **Starting the Backend:**

   - Open a terminal in the `backend` directory.
   - Install the required Python packages using: `pip install -r requirements.txt`
   - Run the backend server using: `python main.py`

### Frontend Setup

1. **Starting the Frontend:**

   - Open a terminal in the `frontend` directory.
   - Start a local server using: `python -m http.server 8080`

   Access the frontend by opening your web browser and navigating to `http://localhost:8080`.

## Usage

1. **User Registration:**

   - Fill in the registration form with a valid email, name, and password.
   - Solve the CAPTCHA to verify you're a human.
   - Click "Register" to create a new user account.

2. **User Login:**

   - Fill in the login form with your registered email and password.
   - Click "Login" to access your user profile.

3. **User Profile:**

   - View your profile information after successful login.
   - Click "Edit Profile" to update your name and password.
   - Click "Delete Profile" to remove your user account.

4. **Logout:**

   - Click the "Logout" button to log out of your account.
