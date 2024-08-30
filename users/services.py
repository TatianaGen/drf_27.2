import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_API_KEY


def create_stripe_product(payment):
    """Создает новый продукт в stripe"""
    tmp_product = payment.course if payment.course else payment.lesson

    product = stripe.Product.create(name=tmp_product.title)

    return product.id


def create_stripe_price(product_id, payment):
    """Создает цену в stripe"""
    price = stripe.Price.create(
        product=product_id,
        currency="rub",
        unit_amount=payment.payment_amount * 100,
    )

    return price.id


def create_stripe_session(price_id):
    """Создает сессию в stripe"""
    session = stripe.checkout.Session.create(
        success_url="http://localhost:8000/",
        line_items=[{"price": price_id, "quantity": 1}],
        mode="payment",
    )

    return session.id, session.url
