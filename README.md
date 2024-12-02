# Quiz App

A dynamic quiz application built with Django that allows users to test their knowledge across different programming languages and topics.

[View Repository](https://github.com/Gaganjeet15/Django_quiz.git)

## Features

- 🎯 Multiple programming categories (Python, Java, C, etc.)
- 🔄 Random questions for each attempt
- ✅ Immediate feedback on answers
- 📱 Responsive design with modern UI
- 🎨 Dark theme interface with gradient backgrounds
- 🔍 Category-specific quizzes
- 📊 Score tracking per session
- 🔄 Option to retry category-specific quizzes
- ⚡ Instant feedback with correct/incorrect indicators

## Live Demo

The application is live at: [https://gaganquiz.pythonanywhere.com/](https://gaganquiz.pythonanywhere.com/)

To access the application:
1. When prompted for login credentials:
   - Username: `user`
   - Password: `user12345`
2. After logging in, remove "admin" from the URL
3. Access the main application at: [https://gaganquiz.pythonanywhere.com/](https://gaganquiz.pythonanywhere.com/)

## Screenshots

### Dashboard
![Dashboard](https://raw.githubusercontent.com/Gaganjeet15/Django_quiz/main/screenshots/dashboard.png)
*Quiz Dashboard with category selection and progress tracking*

### Quiz Interface
![Quiz](https://raw.githubusercontent.com/Gaganjeet15/Django_quiz/main/screenshots/quiz.png)
*Interactive quiz interface with multiple choice questions*

### Results View
![Results](https://raw.githubusercontent.com/Gaganjeet15/Django_quiz/main/screenshots/results.png)
*Instant feedback with correct and incorrect answers highlighted*

## Technologies Used

- Django 5.1.3
- Python 3.x
- Tailwind CSS 2.0.0
- HTML5
- JavaScript
- SQLite3

## Installation

1. Clone the repository
   ```bash
   git clone https://github.com/Gaganjeet15/Django_quiz.git
   cd Django_quiz
   ```

2. Create a virtual environment and activate it
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations
   ```bash
   python manage.py migrate
   ```

5. Start the development server
   ```bash
   python manage.py runserver
   ```

## Usage

1. Access the application at `http://127.0.0.1:8000/`
2. For admin access (optional):
   - **Username**: user
   - **Password**: user12345
3. Select a programming category from the dropdown
4. Answer the 10 questions presented
5. Submit to see your results with instant feedback
6. Try another quiz in the same category or return to dashboard

## Project Structure

quiz_project/
├── quiz/
│   ├── models.py          # Database models (Question, Category)
│   ├── views.py           # View logic
│   ├── templates/         # HTML templates
│      ├── quiz/
│          ├── dashboard.html
│          ├── quiz.html
│   
└── requirements.txt      # Project dependencies

## Database Models

### Category
- name: Category name (e.g., Python, Java, C)
- parent_category: Optional parent category

### Question
- question: The question text
- option_1, option_2, option_3, option_4: Multiple choice options
- correct_answer: The correct option
- category: Related category
- difficulty: Question difficulty level (Easy, Medium, Hard)

## Key Features Explained

1. **Category Selection**
   - Clean dropdown interface
   - Persistent category selection during retries
   - Dark theme UI with gradient effects

2. **Quiz Interface**
   - 10 random questions per attempt
   - Interactive option selection
   - Real-time visual feedback
   - Responsive design for all devices

3. **Results Display**
   - Immediate feedback after submission
   - Correct answers highlighted in green
   - Incorrect answers marked in red
   - Option to try another quiz in same category

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

THANKYOU FOR READING THIS README FILE.
