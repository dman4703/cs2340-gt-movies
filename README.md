# GT Movies Store

A Django-based web application for browsing and purchasing movies online.

## Course Information

**Institution:** Georgia Institute of Technology  
**Course:** CS 2340 – Objects and Design  
**Instructor:** Pedro Guillermo Feijóo-García, Ph.D.  
**Project Coordination:** 
- Lucas Zangari (Head TA)
- Emilio Aponte (Head TA)
- Aidan Pietruszka (Client & Mentor TA)

## Team

- **Patrick:** Scrum Master, Front-end Developer
- **Syed:** Product Owner, Full-stack Developer
- **Haley:** Front-end Developer
- **Chris:** Full-stack Developer
- **Devon:** Back-end Developer

## Features

- **User Authentication**
  - User registration and login
  - Password reset functionality
  - Order history tracking

- **Movie Management**
  - Browse movie catalog
  - Search movies by title
  - Filter movies by genre
  - View detailed movie information
  - Rate and review movies

- **Shopping Experience**
  - Add movies to cart
  - Adjust item quantities
  - Clear shopping cart
  - Complete purchases
  - View order history

- **Admin Dashboard**
  - Manage users, movies, reviews, and orders
  - Upload movie images
  - Track user activity

## Technology Stack

- **Backend**: Django 5.1.5
- **Frontend**: Bootstrap 5.3.3
- **Database**: SQLite3
- **Email**: SMTP (Gmail)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/dman4703/cs2340-gt-movies.git
cd cs2340-gt-movies-store
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the project root with:
```
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Start the development server:
```bash
python manage.py runserver
```

Visit `http://localhost:8000` to access the application.

## Project Structure

```
gt-movies-store/
├── accounts/        # User authentication and management
├── cart/           # Shopping cart functionality
├── home/           # Landing page and about
├── movies/         # Movie catalog and reviews
├── moviesstore/    # Project settings and configuration
├── media/          # User-uploaded content
└── templates/      # Base templates
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request