import json
from pathlib import Path

from django.db import transaction

from .models import CarMake, CarModel, Dealer, Review


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / 'database' / 'data'


def _load_json(name):
    path = DATA_DIR / name
    with path.open('r', encoding='utf-8') as handle:
        return json.load(handle)


@transaction.atomic
def populate_database():
    if Dealer.objects.exists() and Review.objects.exists():
        return

    dealers_data = _load_json('dealerships.json').get('dealerships', [])
    reviews_data = _load_json('reviews.json').get('reviews', [])
    cars_data = _load_json('car_records.json').get('cars', [])

    for dealer_data in dealers_data:
        Dealer.objects.update_or_create(
            id=dealer_data['id'],
            defaults={
                'city': dealer_data.get('city', ''),
                'state': dealer_data.get('state', ''),
                'st': dealer_data.get('st', ''),
                'address': dealer_data.get('address', ''),
                'zip_code': dealer_data.get('zip', ''),
                'lat': dealer_data.get('lat'),
                'long': dealer_data.get('long'),
                'short_name': dealer_data.get('short_name', ''),
                'full_name': dealer_data.get('full_name', ''),
            },
        )

    for car_data in cars_data:
        make_name = car_data.get('make', '').strip()
        if not make_name:
            continue
        make_obj, _ = CarMake.objects.get_or_create(name=make_name, defaults={'description': f'Inventory for {make_name}'})
        model_name = car_data.get('model', '').strip()
        body_type = car_data.get('bodyType', 'Other')
        year = int(car_data.get('year', 2023))
        CarModel.objects.get_or_create(
            make=make_obj,
            name=model_name,
            year=year,
            defaults={'type': body_type, 'description': f'{make_name} {model_name} inventory'}
        )

    for review_data in reviews_data:
        dealer_id = review_data.get('dealership')
        dealer = Dealer.objects.filter(id=dealer_id).first()
        if dealer is None:
            continue
        Review.objects.update_or_create(
            id=review_data['id'],
            defaults={
                'name': review_data.get('name', 'Anonymous'),
                'dealership': dealer,
                'review': review_data.get('review', ''),
                'purchase': bool(review_data.get('purchase', False)),
                'purchase_date': None,
                'car_make': review_data.get('car_make', ''),
                'car_model': review_data.get('car_model', ''),
                'car_year': int(review_data.get('car_year', 2023)),
                'sentiment': review_data.get('sentiment', 'neutral'),
            },
        )


def initiate():
    populate_database()
    return {'status': 'ok'}
