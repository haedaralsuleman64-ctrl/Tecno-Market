#### TEcNO Market #### 

Welcome to TEcNO Market! 🛍️

TEcNO Market is a modern and comprehensive e-commerce platform for selling electronic products at competitive prices. The store offers a wide range of products, including laptops, complete computer systems, headphones, smartwatches, and mobile devices. It is built with a simple and eye-friendly user interface to provide the best possible shopping experience.

Prerequisites

To run this project, you must have the following software installed on your system:

    Python 3.10 or a later version.

    Git to handle the project repository.

## Setup Guide

Follow these steps to set up and run the TEcNO Market web application on your local machine.

# 1. Clone the Repository

 - Open your terminal or command prompt and clone the project using the following command:
  $ git clone [Your Repository URL]
  $ cd TEcNO-Market

# 2. Create and Activate a Virtual Environment

 It is highly recommended to use a virtual environment to manage the project dependencies.
 - Create the virtual environment
  $ python -m venv venv

 - Activate the environment (on Linux and macOS)
  $ source venv/bin/activate

 - Activate the environment (on Windows)
  $ venv\Scripts\activate

# 3. Install Required Libraries

 - With the virtual environment activated, install all the dependencies listed in the requirements.txt file.
  $ pip install -r requirements.txt

# 4. Configure Project Settings

 - For security and proper functionality, you need to configure some settings. The project uses python-decouple to manage sensitive information, so you must create a .env file.
   Create a file named .env in the project's root directory (next to manage.py).

 - Add the following lines to the file, replacing the placeholder values:
// Django Secret Key
$ SECRET_KEY=YourSuperSecretAndUniqueKeyHere

$ Google Social Login Settings (Optional but required for the project structure)
$ GOOGLE_CLIENT_ID=Your_Google_Client_ID
$ GOOGLE_CLIENT_SECRET=Your_Google_Client_Secret

# 5. Apply Database Migrations

 - This project uses SQLite3 as its default database. Run the following Django commands to create the necessary database tables:

  $ python manage.py makemigrations
  $ python manage.py migrate

# 6. Load Initial Data

 - To populate the store with initial product data, run the loaddata command:

  $ python manage.py loaddata products/fixtures/products.json

# 7. Collect Static Files

 - To properly serve CSS, JavaScript, and image files, you need to run the collectstatic command:

  $ python manage.py collectstatic

# 8. Create a Superuser

 - To access the Django Admin Panel, you must create a superuser account:

  $ python manage.py createsuperuser

Follow the on-screen prompts to enter your desired username, email, and password.

# 9. Run the Development Server

 - Finally, start the development server to view the store in your browser:

  $ python manage.py runserver

# The TEcNO Market website will now be accessible at: http://127.0.0.1:8000/

# To log in to the admin panel, visit:
$ http://127.0.0.1:8000/admin

Enjoy your experience with TEcNO Market! 😊