import stripe
from config import settings

stripe.api_key = settings.STRIPE_API_KEY


def create_stripe_product(name):
    return stripe.Product.create(name=name)


def create_stripe_price(product, price):
    return stripe.Price.create(
        currency="rub",
        unit_amount=price * 100,
        product_data={"name": product.get("name")},
    )


def create_stripe_session(price):
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price.get('id'), "quantity": 1}],
        mode="payment",
    )

    return session.get('id'), session.get('url')


def perform_create_payment(payment, price, name):
    payment.sum = price

    if payment.way == 'bank':
        payment_product = create_stripe_product(name)
        payment_price = create_stripe_price(payment_product, payment.sum)
        payment_session_id, payment_link = create_stripe_session(payment_price)
        payment.session_id = payment_session_id
        payment.link = payment_link

    payment.save()
