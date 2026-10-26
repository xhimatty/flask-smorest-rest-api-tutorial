from flask_smorest import Blueprint, abort
from marshmallow import Schema, fields
from models import db, Product

blp = Blueprint('products', __name__, url_prefix='/products')


# Marshmallow Schema

class ProductSchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True)
    description = fields.Str()
    price = fields.Float()
    qty = fields.Int()


# Filtering products
class ProductQuerySchema(Schema):
    price_min = fields.Float(load_default=0)
    page = fields.Int(load_default=1)
    per_page = fields.Int(load_default=2)
    sort = fields.Str(load_default='price')


# Add product with POST 

@blp.route('/', methods=['POST'])
@blp.arguments(ProductSchema)
@blp.response(201, ProductSchema)
def products(data):
    """Create a product and save it to the database."""
    product = Product(**data) 
    db.session.add(product)
    db.session.commit()
    return product 


# Retrieve product with GET

# @blp.route('/', methods=['GET'])
# @blp.arguments(ProductQuerySchema, location='query')
# @blp.response(200, ProductSchema(many=True))
# def see_products(args):
#     """Filter products based on price"""
#     return Product.query.filter(Product.price >= args['price_min']).all()

# @blp.route('/', methods=['GET'])
# @blp.arguments(ProductQuerySchema, location='query')
# @blp.response(200, ProductSchema(many=True))
# def see_products(args):
#     """Pagination of products"""
#     return Product.query.paginate(
#         page=args['page'],
#         per_page=args['per_page']
#     ).items


@blp.route('/', methods=['GET'])
@blp.arguments(ProductQuerySchema, location='query')
@blp.response(200, ProductSchema(many=True))
def see_products(args):
    """Retrieve product with sorting"""
    if args['sort'] == '-price':
        return Product.query.order_by(Product.price.desc()).all()
    return Product.query.order_by(Product.price).all()


@blp.route('/<int:product_id>', methods=['GET'])
@blp.response(200, ProductSchema)
def get_product(product_id):
    """Retrieve a product by ID or return 404 if it doesn't exist.""" 
    product = Product.query.get_or_404(product_id)
    return product


# Update product with PUT

@blp.route('/<int:product_id>', methods=['PUT'])
@blp.arguments(ProductSchema)
@blp.response(200, ProductSchema)
def update_product(data, product_id):
    """Update an existing product using its id"""
    product = Product.query.get_or_404(product_id)
    product.name = data.get('name')
    product.description = data.get('description')
    product.price = data.get('price')
    product.qty = data.get('qty')
    db.session.commit()
    return product


# Delete product with Delete

@blp.route('/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Delete a product using its id"""
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return {'message': 'Product deleted successfully'}, 200