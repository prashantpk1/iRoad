# iRoad

## Project Overview

iRoad is a Django-based web application designed to manage and process road-related data and workflows. The project is structured for modularity, maintainability, and ease of use.

## Features
- User authentication and OTP verification
- Entity and account management
- Document handling and templates
- Modular app structure for scalability

## Project Structure
```
iRoad/
  Project/
	 manage.py
	 App/
	 core/
	 documents/
	 templates/
```

## Getting Started

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Django (recommended version: 4.x)

### Setup Instructions
1. Clone the repository:
	```bash
	git clone <repo-url>
	cd iRoad/Project
	```
2. Install dependencies:
	```bash
	pip install -r requirements.txt
	```
	*(Create `requirements.txt` if not present: `pip freeze > requirements.txt`)*
3. Apply migrations:
	```bash
	python manage.py migrate
	```
4. Create a superuser (admin):
	```bash
	python manage.py createsuperuser
	```
5. Run the development server:
	```bash
	python manage.py runserver
	```

## Usage
- Access the app at `http://127.0.0.1:8000/`
- Admin panel at `http://127.0.0.1:8000/admin/`

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
This project is licensed under the MIT License.