# My_Blogs

My_Blogs is a Django-based web application that allows users to create, manage, and interact with blog posts. Users can register, log in, update their profiles, create posts, edit posts, delete posts, like posts, and comment on posts. Additionally, the application supports filtering, sorting, and searching for posts.

## Features

- **User Authentication**:
  - User registration and login.
  - Profile update functionality.
  
- **Blog Post Management**:
  - Create, edit, and delete blog posts.
  - Like and comment on posts.
  
- **Search and Filter**:
  - Filter posts by categories, tags, or authors.
  - Sort posts by date, popularity, or title.
  - Search for posts using keywords.

## Technologies Used

- **Backend**: Django 5.1.6
- **Database**: SQLite (default)
- **Frontend**: HTML, CSS, JavaScript (optional)
- **Additional Packages**:
  - `Pillow` for image handling.
  - `sqlparse` for SQL parsing.
  - `tzdata` for timezone support.

## Installation

Follow these steps to set up the project locally:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/My_Blogs.git
   cd My_Blogs
Create a Virtual Environment:

bash
Copy
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install Dependencies:

bash
Copy
pip install -r requirements.txt
Apply Migrations:

bash
Copy
python manage.py migrate
Create a Superuser:

bash
Copy
python manage.py createsuperuser
Run the Development Server:

bash
Copy
python manage.py runserver
Access the Application:
Open your browser and go to http://127.0.0.1:8000/.

Project Structure
Copy
My_Blogs/
├── blog/                   # Main app for blog functionality
│   ├── migrations/         # Database migrations
│   ├── templates/          # HTML templates
│   ├── admin.py            # Admin configuration
│   ├── apps.py             # App configuration
│   ├── models.py           # Database models
│   ├── views.py            # View functions
│   ├── urls.py             # App-specific URLs
│   └── ...
├── My_Blogs/               # Project settings and configurations
│   ├── settings.py         # Django settings
│   ├── urls.py             # Main URLs
│   ├── wsgi.py             # WSGI configuration
│   └── ...
├── manage.py               # Django management script
├── requirements.txt        # List of dependencies
└── README.md               # Project documentation
Usage
User Registration and Login
Visit the registration page to create a new account.

Log in using your credentials to access the dashboard.

Create a Blog Post
Navigate to the "Create Post" page.

Fill in the title, content, and optional image.

Submit the form to publish the post.

Edit or Delete a Post
Go to the "My Posts" section.

Click on the post you want to edit or delete.

Make changes or delete the post.

Like and Comment on Posts
View any post on the homepage or detail page.

Click the "Like" button to like the post.

Add a comment using the comment form.

Search, Filter, and Sort Posts
Use the search bar to find posts by keywords.

Apply filters to narrow down posts by category, author, or tags.

Sort posts by date, popularity, or title.

Contributing
Contributions are welcome! Please follow these steps:

Fork the repository.
