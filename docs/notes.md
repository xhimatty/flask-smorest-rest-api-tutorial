# Flask-Smorest Product API Notes

## 1. Project Overview

This project is a Product REST API built with Flask, Flask-Smorest, Marshmallow, Flask-SQLAlchemy and SQLite.

Flask-Smorest handles API routes, request validation, response serialisation and API documentation. Marshmallow defines the structure of the data being sent and returned. Flask-SQLAlchemy handles database operations, while SQLite stores the products.

## 2. Project Structure

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

* [`app.py`](app.py) creates the Flask application, configures Flask-Smorest and SQLite, initialises the database and registers the blueprint.
* [`models.py`](models.py) contains the SQLAlchemy database model.
* [`views.py`](views.py) contains the Marshmallow schemas and API routes.
* [`api.http`](api.http) contains HTTP requests for testing the API using the REST Client extension in VS Code.
* [`products.db`](products.db) is the SQLite database where the products are stored.
* [`README.md`](README.md) contains the general project information.
* [`docs/notes.md`](docs/notes.md) contains my learning notes and explanations of the code.

## 3. [Flask-Smorest](https://flask-smorest.readthedocs.io/en/latest/quickstart.html)

Flask-Smorest integrates API routes with Flask and provides request validation, response serialisation and OpenAPI documentation.

The main components used in this project are:

* `Blueprint`: Groups related API routes.
* `Schema`: Defines the structure of the data using Marshmallow.
* `@blp.arguments()`: Validates incoming request data and passes the validated data to the route function.
* `@blp.response()`: Serialises the returned data and documents the response structure.
* `Api`: Integrates Flask-Smorest with the Flask application and registers the blueprints.

### Blueprint and URL Prefix

The blueprint is defined in [`views.py`](views.py):

```python
blp = Blueprint('products', __name__, url_prefix='/products')
```

The `url_prefix='/products'` means every route registered under this blueprint starts with `/products`.

For example:

```python
@blp.route('/', methods=['GET'])
```

The full endpoint is `/products/`.

Another example:

```python
@blp.route('/<int:product_id>', methods=['GET'])
```

The full endpoint is `/products/<int:product_id>`. When a request is sent to `/products/2`, Flask passes the integer `2` to the function as `product_id`.

The blueprint prefix is already `/products`, so adding `/products` again to the route would result in `/products/products`.

## 4. [Marshmallow Schema](https://marshmallow.readthedocs.io/en/latest/)

The product schema defines the fields returned by the API and the structure used to validate incoming product data.

```python
class ProductSchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True)
    description = fields.Str()
    price = fields.Float()
    qty = fields.Int()
```

* `fields.Int()` defines an integer field.
* `fields.Str()` defines a string field.
* `fields.Float()` defines a floating-point number field.
* `required=True` means the field must be present in the incoming data when Marshmallow validates it. Otherwise, validation fails with a 422 response.
* `id` is included in the schema so it can be returned in the response.

Defining a schema alone does not automatically validate incoming requests. It must be connected to a route using `@blp.arguments()`.

### Request Validation

```python
@blp.arguments(ProductSchema)
```

This validates incoming JSON against `ProductSchema` and passes the validated data to the function as `data`.

If a required field is missing or a field contains an invalid value, Marshmallow raises a validation error.

For example, `name` is required, so sending a request without it results in a `422 Unprocessable Entity response`.

## 5. Creating a Product Using `POST`

The `POST` endpoint creates a new product and saves it to the database.

```python
@blp.route('/', methods=['POST'])
@blp.arguments(ProductSchema)
@blp.response(201, ProductSchema)
def products(data):
    """Create a product and save it to the database."""
    product = Product(**data)
    db.session.add(product)
    db.session.commit()
    return product
```

### How it works

`Product(**data)` creates a Product object using the validated request data.

The `**data` syntax is Python dictionary unpacking. It passes the dictionary's keys and values to the Product constructor as keyword arguments.

For example, if `data` contains:

```python
{
    'name': 'Hisense TV 116UXS',
    'description': 'A massive 116-inch high-end model adding cyan backlight structure',
    'price': 720.50,
    'qty': 100
}
```

Python passes those values to the Product constructor as if I had written each argument separately.

`db.session.add(product)` adds the new product to the database session.

`db.session.commit()` commits the transaction and saves the product to the database.

`return product` returns the saved product. Flask-Smorest serialises it using `ProductSchema` and responds with HTTP 201 Created.

The `201` status code indicates that a resource has been created successfully.

## 6. Retrieving All Products Using `GET`

The `GET` endpoint retrieves all products stored in the database.

```python
@blp.route('/', methods=['GET'])
@blp.response(200, ProductSchema(many=True))
def see_products():
    """Retrieve all products from the database."""
    return Product.query.all()
```

`Product.query.all()` retrieves all product records from the database.

`ProductSchema(many=True)` tells Flask-Smorest that the response contains multiple products. Without `many=True`, the schema would be configured to serialise a single product rather than a collection.

The `200` status code indicates that the request was successful.

Unlike `POST`, this endpoint does not need `@blp.arguments(ProductSchema)` because it does not receive product data in the request body.

## 7. Retrieving a Single Product Using `GET`

The endpoint below retrieves one product using its ID.

```python
@blp.route('/<int:product_id>', methods=['GET'])
@blp.response(200, ProductSchema)
def get_product(product_id):
    """Retrieve a product by ID or return 404 if it doesn't exist."""
    product = Product.query.get_or_404(product_id)
    return product
```

The `<int:product_id>` part of the route tells Flask to accept an integer from the URL and pass it to the function as `product_id`.

`Product.query.get_or_404(product_id)` searches for a product using its primary key.

If the product exists, SQLAlchemy returns the Product object. If it does not exist, Flask returns a 404 Not Found response.

This saves me from writing an `if` statement to check whether the product exists.

Since this endpoint returns a single product, `ProductSchema` is used without `many=True`.

## 8. Updating a Product Using `PUT`

The `PUT` endpoint updates an existing product using its ID.

```python
@blp.route('/<int:product_id>', methods=['PUT'])
@blp.arguments(ProductSchema)
@blp.response(200, ProductSchema)
def update_product(data, product_id):
    """Update an existing product using its ID."""
    product = Product.query.get_or_404(product_id)
    product.name = data.get('name')
    product.description = data.get('description')
    product.price = data.get('price')
    product.qty = data.get('qty')
    db.session.commit()
    return product
```

`@blp.arguments(ProductSchema)` validates the incoming JSON data and passes it to the function as `data`.

`Product.query.get_or_404(product_id)` retrieves the product to update. If the product does not exist, Flask returns a 404 Not Found response.

The assignment statements update the product's existing attributes using the values supplied in the request.

For example:

```python
product.name = data.get('name')
```

This assigns the submitted name to the product's `name` attribute.

`db.session.commit()` saves the changes to the database.

`return product` returns the updated product, which Flask-Smorest serialises using `ProductSchema`. The response status is `200 OK`.

### Testing PUT Using REST Client

```http
PUT http://127.0.0.1:5000/products/2
Content-Type: application/json

{
    "name": "Updated Hisense TV",
    "description": "Updated product description",
    "price": 850.50,
    "qty": 45
}
```

This request updates the product with ID `2`.

Expected result: `200 OK`, followed by the updated product details.

If product ID `2` does not exist, the endpoint returns `404 Not Found`.

## 9. Deleting a Product Using `DELETE`

The `DELETE` endpoint removes an existing product from the database using its ID.

```python
@blp.route('/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Delete a product using its ID."""
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return {'message': 'Product deleted successfully'}, 200
```

`Product.query.get_or_404(product_id)` retrieves the product to delete. If the product does not exist, Flask returns a 404 Not Found response.

`db.session.delete(product)` marks the product for deletion from the database.

`db.session.commit()` commits the transaction and saves the deletion.

The function returns a JSON message confirming that the product was deleted, together with the `200 OK` status code.

### Testing DELETE Using REST Client

```http
DELETE http://127.0.0.1:5000/products/2
```

Expected result:

```json
{
    "message": "Product deleted successfully"
}
```

The response status is `200 OK`.

If I send the same DELETE request again, the endpoint returns `404 Not Found` because the product has already been deleted.

## 10. Testing the API Using REST Client

The [`test/api.http`](test/api.http) file contains the HTTP requests used to test the API.

The VS Code REST Client extension allows me to send HTTP requests directly from this file and inspect the responses.

### Complete `api.http` File

The following requests can be kept in the same file and sent individually using the `Send Request` link displayed above each request.

```http
POST http://127.0.0.1:5000/products/
Content-Type: application/json

{
    "name": "Hisense TV 116UXS",
    "description": "A massive 116-inch high-end model adding cyan backlight structure",
    "price": 720.50,
    "qty": 100
}

###

POST http://127.0.0.1:5000/products/
Content-Type: application/json

{
    "name": "Hisense TV 163MX",
    "description": "A massive 163-inch flagship feature a four-primary RGBY architecture",
    "price": 920.25,
    "qty": 60
}

###

GET http://127.0.0.1:5000/products/

###

GET http://127.0.0.1:5000/products/2

###

PUT http://127.0.0.1:5000/products/2
Content-Type: application/json

{
    "name": "Updated Hisense TV",
    "description": "Updated product description",
    "price": 850.50,
    "qty": 45
}

###

DELETE http://127.0.0.1:5000/products/2
```

## 11. Swagger UI and OpenAPI Documentation

Flask-Smorest can generate OpenAPI documentation for the API and provide an interactive Swagger UI page.

### OpenAPI Configuration in `app.py`

The relevant configuration is:

```python
app.config['API_TITLE'] = 'Product API'
app.config['API_VERSION'] = 'v1'
app.config['OPENAPI_VERSION'] = '3.0.2'
app.config['OPENAPI_URL_PREFIX'] = '/'
app.config['OPENAPI_SWAGGER_UI_PATH'] = '/swagger-ui'
app.config['OPENAPI_SWAGGER_UI_URL'] = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'
```

These settings configure the API's title, version, OpenAPI specification version and Swagger UI.

### Opening Swagger UI

Start the Flask application and visit:

`http://127.0.0.1:5000/swagger-ui`

Swagger UI displays the registered API endpoints and allows me to send requests through the browser.

The OpenAPI JSON specification is available at:

`http://127.0.0.1:5000/openapi.json`


## 12. Filtering Products by Minimum Price

Filtering allows us to retrieve products that match a condition. In this example, we retrieve products whose prices are greater than or equal to a specified minimum price.

### ProductQuerySchema

```python
class ProductQuerySchema(Schema):
    price_min = fields.Float(load_default=0)
```

* `price_min` is the query parameter used to set the minimum price.
* `load_default=0` means the minimum price defaults to `0` if the user does not provide one.

### GET Endpoint

```python
@blp.route('/', methods=['GET'])
@blp.arguments(ProductQuerySchema, location='query')
@blp.response(200, ProductSchema(many=True))
def see_products(args):
    """Filter products by minimum price."""
    return Product.query.filter(
        Product.price >= args['price_min']
    ).all()
```

`@blp.arguments(ProductQuerySchema, location='query')` reads and validates the query parameters and passes them to the function through `args`.

`Product.query.filter()` filters the products according to the condition provided.

`.all()` returns all products that match the condition.

### Testing with `api.http`

```http
### Filter products with a minimum price of 100
GET http://127.0.0.1:5000/products/?price_min=100
```

You can change `100` to another value to test different minimum prices.

## 13. Pagination

Pagination divides a large list of products into smaller pages. Instead of returning every product in one response, the API returns a specified number of products per page.

### ProductQuerySchema

```python
class ProductQuerySchema(Schema):
    page = fields.Int(load_default=1)
    per_page = fields.Int(load_default=2)
```

* `page` specifies which page to retrieve. It defaults to page `1`.
* `per_page` specifies how many products to return per page. It defaults to `2` in this example.

### GET Endpoint

```python
@blp.route('/', methods=['GET'])
@blp.arguments(ProductQuerySchema, location='query')
@blp.response(200, ProductSchema(many=True))
def see_products(args):
    """Paginate products."""
    return Product.query.paginate(
        page=args['page'],
        per_page=args['per_page']
    ).items
```

`Product.query.paginate()` handles pagination.

* `page` selects the requested page.
* `per_page` sets the number of products on each page.
* `.items` returns the products on that page.

### Testing with `api.http`

```http
### Retrieve the first page
GET http://127.0.0.1:5000/products/?page=1

### Retrieve the second page
GET http://127.0.0.1:5000/products/?page=2

### Retrieve the first page with three products
GET http://127.0.0.1:5000/products/?page=1&per_page=3
```

With four products in the database and `per_page=2`, page 1 returns the first two products, and page 2 returns the next two.

**Note:** This example demonstrates pagination only. It does not filter products by price.

## 14. Sorting Products

Sorting allows us to arrange products according to a field, such as price. In this example, we sort products by price in ascending or descending order.

### ProductQuerySchema

```python
class ProductQuerySchema(Schema):
    sort = fields.Str(load_default='price')
```

* `sort` specifies the sorting order.
* `load_default='price'` means products are sorted by price in ascending order when no sorting parameter is provided.
* `sort=-price` requests descending order.

### GET Endpoint

```python
@blp.route('/', methods=['GET'])
@blp.arguments(ProductQuerySchema, location='query')
@blp.response(200, ProductSchema(many=True))
def see_products(args):
    """Sort products by price."""
    if args['sort'] == '-price':
        return Product.query.order_by(Product.price.desc()).all()

    return Product.query.order_by(Product.price).all()
```

`Product.query.order_by(Product.price)` sorts products by price in ascending order.

`Product.price.desc()` sorts products by price in descending order.

The `if` statement checks whether the user requested descending order. If not, the endpoint returns products in ascending order.

**Note:** This example demonstrates sorting only. It does not filter or paginate the results.

### Testing with `api.http`

```http
### Sort products by price in ascending order
GET http://127.0.0.1:5000/products/?sort=price

### Sort products by price in descending order
GET http://127.0.0.1:5000/products/?sort=-price
```

Compare the responses to see how the product order changes.

## 15. HTTP Status Codes Learned So Far

| Status Code       | Meaning                                      | Example                                                                           |
| ----------------- | -------------------------------------------- | --------------------------------------------------------------------------------- |
| `200 OK`          | Request succeeded                            | Retrieving, updating, or deleting a product, depending on the endpoint's response |
| `201 Created`     | A resource was created successfully          | Creating a product using POST                                                     |
| `400 Bad Request` | The request contains invalid or missing data | A required field is missing or has an invalid value                               |
| `404 Not Found`   | The requested resource does not exist        | Retrieving, updating, or deleting a product ID that does not exist                |
| `422 Unprocessable Entity` | The request data fails validation | A required field is missing or a field contains an invalid value                |
