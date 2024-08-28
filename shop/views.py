import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .models import Product, Category

@csrf_exempt
def handle_post_request(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST requests are allowed"})

    custom_header = request.headers.get('Custom-Header')
    content_type = request.headers.get('Content-Type')

    if content_type == 'application/json':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON data")

        product_name = data.get('name')
        product_price = data.get('price')
        product_description = data.get('description', '')
        category_slug = data.get('category_slug')

        if not product_name or not product_price or not category_slug:
            return JsonResponse({"error": "Missing name, price, or category"})

        try:
            category = Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            return JsonResponse({"error": "Category not found"})

        product = Product.objects.create(
            name=product_name,
            price=product_price,
            description=product_description,
            category=category,
            stock=data.get('stock', 1),  # default stock to 1 if not provided
            available=data.get('available', True)
        )

        return JsonResponse({
            "message": "Product created successfully",
            "product_name": product.name,
            "product_price": product.price,
            "category": category.name,
            "custom_header": custom_header
        })

    else:
        return JsonResponse({"error": "Unsupported Content-Type"})


def product_list(request):
    products = Product.objects.all()
    product_data = [{
        "name": product.name,
        "price": product.price,
        "description": product.description,
        "category": product.category.name,
        "stock": product.stock,
        "available": product.available
    } for product in products]
    return JsonResponse({"products": product_data})


def product_detail(request, slug):
    try:
        product = Product.objects.get(slug=slug)
        product_data = {
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "category": product.category.name,
            "stock": product.stock,
            "available": product.available
        }
        return JsonResponse({"product": product_data})
    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found"})
