# Flask-Smorest REST API

A beginner-friendly REST API built with Flask-Smorest, Flask-SQLAlchemy, Marshmallow, and SQLite.

This project demonstrates how to build a REST API for managing products, from basic CRUD operations to filtering, pagination, and sorting.

The goal is to understand how the different parts of a Flask REST API work together through practical examples.

## Technologies Used

* Python
* Flask
* Flask-Smorest
* Flask-SQLAlchemy
* SQLAlchemy
* Marshmallow
* SQLite
* REST Client for VS Code

## Features

### Product Management (CRUD)

The API supports the four basic CRUD operations:

* **Create:** Add a new product.
* **Read:** Retrieve all products or a single product by ID.
* **Update:** Modify an existing product.
* **Delete:** Remove a product.

Each product contains the following fields:

| Field         | Description               |
| ------------- | ------------------------- |
| `id`          | Unique product identifier |
| `name`        | Product name              |
| `description` | Product description       |
| `price`       | Product price             |
| `qty`         | Product quantity          |

### Data Validation

Marshmallow schemas validate incoming request data and define the structure of API responses.

The API can reject invalid requests, including requests with missing required fields.

### Filtering

Retrieve products that meet a specified minimum price.

Example:

`GET /products/?price_min=500`

### Pagination

Retrieve products in smaller groups by specifying a page number and the number of products per page.

Example:

`GET /products/?page=1&per_page=2`

### Sorting

Sort products by price in ascending or descending order.

Examples:

* `GET /products/?sort=price`
* `GET /products/?sort=-price`

Filtering, pagination, and sorting are demonstrated as separate concepts. See [`docs/notes.md`](docs/notes.md) for code examples and explanations, and [`test/api.http`](test/api.http) to test the endpoints.

### API Documentation

Flask-Smorest generates OpenAPI documentation from the API configuration, routes, and schemas.

The interactive Swagger UI allows you to inspect endpoints and send requests.

## Project Structure

```text
flask-smorest-rest-api-tutorial/
├── docs/
│   └── notes.md
├── test/
│   └── api.http
├── .gitignore
├── app.py
├── models.py
├── views.py
├── requirements.txt
└── README.md
```

* [`app.py`](app.py): Creates and configures the Flask application and registers the blueprint.
* [`models.py`](models.py): Defines the database and Product model using modern SQLAlchemy 2.1.
* [`views.py`](views.py): Defines the API endpoints, schemas, and request handling.
* [`test/api.http`](test/api.http): Contains example HTTP requests for testing the API in VS Code.
* [`docs/notes.md`](docs/notes.md): Contains learning notes and code examples.
* `.env`: Stores local environment variables.
* `.gitignore`: Specifies files Git should ignore.
* `requirements.txt`: Lists the Python dependencies required by the project.

The SQLite database is created locally when the application is configured to create it. The database file should not be committed to the repository.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/xhimatty/flask-smorest-rest-api-tutorial.git
```

Navigate into the project directory:

```bash
cd flask-smorest-rest-api-tutorial
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it in PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python app.py
```

The API should now be available at:

`http://127.0.0.1:5000`

## API Documentation

Once the application is running, open Swagger UI:

`http://127.0.0.1:5000/swagger-ui`

The OpenAPI specification is available at:

`http://127.0.0.1:5000/openapi.json`

## Testing the API

This project uses the REST Client extension in Visual Studio Code.

Instead of switching between your code editor and external tools like Postman or Thunder Client, this project includes a pre-configured .http file in the tests/ directory (e.g., requests.http).

### Why REST Client?

* Keep your test cases version-controlled alongside your code.
* No need to manage heavy desktop application workspaces.
* Quick execution directly inside VS Code.

### How to Use

Open [`test/api.http`](test/api.http) 
Ensure you have the REST Client extension enabled and send the requests to create, retrieve, update, and delete products, as well as test filtering, pagination, and sorting.

### Example

```http
POST http://127.0.0.1:5000/products/
Content-Type: application/json

{
    "name": "Hisense TV 116UXS",
    "description": "A massive 116-inch high-end model adding cyan backlight structure",
    "price": 720.50,
    "qty": 100
}
```

## Learning Notes

The [`docs/notes.md`](docs/notes.md) file documents the concepts covered during development, including CRUD operations, Marshmallow schemas, request validation, filtering, pagination, and sorting.

The project is intended as a learning resource for beginners who want to understand how to build REST APIs using Flask-Smorest.

## Who Is This For?

This is a beginner-friendly tutorial for those who are new to:

* [Flask-SQLAlchemy](https://docs.sqlalchemy.org/en/21/orm/quickstart.html)
* [Flask-Smorest](https://flask-smorest.readthedocs.io/en/latest/quickstart.html)
* [Marshmallow](https://marshmallow.readthedocs.io/en/latest/)
