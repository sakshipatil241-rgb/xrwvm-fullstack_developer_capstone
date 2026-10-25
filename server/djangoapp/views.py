
import json
import logging
from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import CarModel, Dealer, Review
from .populate import initiate
from .restapis import analyze_review_sentiments

logger = logging.getLogger(__name__)


def _dealer_payload(dealer):
    return {
        "id": dealer.id,
        "city": dealer.city,
        "state": dealer.state,
        "st": dealer.st,
        "address": dealer.address,
        "zip": dealer.zip_code,
        "lat": dealer.lat,
        "long": dealer.long,
        "short_name": dealer.short_name,
        "full_name": dealer.full_name,
    }


def _review_payload(review):
    return {
        "id": review.id,
        "name": review.name,
        "dealership": review.dealership_id,
        "review": review.review,
        "purchase": review.purchase,
        "purchase_date": review.purchase_date.strftime("%Y-%m-%d") if review.purchase_date else "",
        "car_make": review.car_make,
        "car_model": review.car_model,
        "car_year": review.car_year,
        "sentiment": review.sentiment,
    }


@csrf_exempt
def login_user(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body)
    except (TypeError, ValueError):
        return JsonResponse({"error": "Invalid JSON payload"}, status=400)

    username = (data.get("userName") or data.get("username") or "").strip()
    password = data.get("password", "")

    if not username or not password:
        return JsonResponse({"error": "Username and password are required"}, status=400)

    user = authenticate(request, username=username, password=password)
    if user is None:
        return JsonResponse({"userName": username, "status": "Authentication failed"}, status=401)

    login(request, user)
    return JsonResponse({"userName": username, "status": "Authenticated"})


@csrf_exempt
def logout_request(request):
    if request.user.is_authenticated:
        logout(request)
    return JsonResponse({"status": "Logged out", "success": True})


@csrf_exempt
def registration(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body)
    except (TypeError, ValueError):
        return JsonResponse({"error": "Invalid JSON payload"}, status=400)

    username = (data.get("username") or data.get("userName") or "").strip()
    first_name = (data.get("first_name") or data.get("firstName") or "").strip()
    last_name = (data.get("last_name") or data.get("lastName") or "").strip()
    email = (data.get("email") or "").strip()
    password = data.get("password", "")

    if not username or not email or not password:
        return JsonResponse({"error": "Username, email, and password are required"}, status=400)

    if User.objects.filter(username=username).exists():
        return JsonResponse({"error": "Username already exists"}, status=409)

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
    )
    user.save()
    login(request, user)
    return JsonResponse({"status": "success", "userName": username}, status=201)


def get_dealers(request):
    initiate()
    dealers = Dealer.objects.all().order_by("id")
    payload = {"status": 200, "dealers": [_dealer_payload(item) for item in dealers]}
    return JsonResponse(payload)


def get_dealers_by_state(request, state):
    initiate()
    if state.lower() == "all":
        dealers = Dealer.objects.all().order_by("id")
    else:
        dealers = Dealer.objects.filter(state__iexact=state).order_by("id")

    return JsonResponse({"status": 200, "dealers": [_dealer_payload(item) for item in dealers]})


def get_dealer_details(request, dealer_id):
    initiate()
    dealer = Dealer.objects.filter(id=dealer_id).first()
    if dealer is None:
        return JsonResponse({"status": 404, "error": "Dealer not found"}, status=404)
    return JsonResponse({"status": 200, "dealer": [_dealer_payload(dealer)]})


def get_dealer_reviews(request, dealer_id):
    initiate()
    reviews = Review.objects.filter(dealership_id=dealer_id).order_by("id")
    return JsonResponse({"status": 200, "reviews": [_review_payload(item) for item in reviews]})


@csrf_exempt
def add_review(request):
    if not request.user.is_authenticated:
        return JsonResponse({"status": 401, "error": "Authentication required"}, status=401)

    if request.method != "POST":
        return JsonResponse({"status": 405, "error": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body)
    except (TypeError, ValueError):
        return JsonResponse({"status": 400, "error": "Invalid JSON payload"}, status=400)

    required_fields = ["dealership", "review", "purchase_date", "car_make", "car_model", "car_year"]
    missing = [field for field in required_fields if data.get(field) in (None, "")]
    if missing:
        return JsonResponse({"status": 400, "error": f"Missing required fields: {missing}"}, status=400)

    dealer = Dealer.objects.filter(id=data["dealership"]).first()
    if dealer is None:
        return JsonResponse({"status": 404, "error": "Dealer not found"}, status=404)

    name = (data.get("name") or request.user.get_full_name() or request.user.username).strip() or request.user.username
    review_text = data["review"].strip()

    try:
        purchase_date = datetime.strptime(data["purchase_date"], "%Y-%m-%d").date()
    except ValueError:
        try:
            purchase_date = datetime.strptime(data["purchase_date"], "%m/%d/%Y").date()
        except ValueError:
            return JsonResponse({"status": 400, "error": "Date format invalid"}, status=400)

    review = Review.objects.create(
        name=name,
        dealership=dealer,
        review=review_text,
        purchase=bool(data.get("purchase", False)),
        purchase_date=purchase_date,
        car_make=data["car_make"],
        car_model=data["car_model"],
        car_year=int(data["car_year"]),
        sentiment=analyze_review_sentiments(review_text),
    )

    return JsonResponse({"status": 200, "message": "Review added successfully", "review": _review_payload(review)})


def get_car_models(request):
    initiate()
    models = CarModel.objects.select_related("make")
    payload = {
        "status": 200,
        "CarModels": [{
            "CarMake": item.make.name,
            "CarModel": item.name,
            "CarType": item.type,
            "CarYear": item.year,
        } for item in models],
    }
    return JsonResponse(payload)


@csrf_exempt
def analyze_review(request, text=None):
    if request.method not in {"GET", "POST"}:
        return JsonResponse({"error": "Method not allowed"}, status=405)

    if text is None:
        try:
            data = json.loads(request.body)
        except (TypeError, ValueError):
            return JsonResponse({"error": "Review text required"}, status=400)
        text = data.get("text") or data.get("review") or ""

    if not text:
        return JsonResponse({"error": "Review text required"}, status=400)

    sentiment = analyze_review_sentiments(text)
    return JsonResponse({"sentiment": sentiment})
