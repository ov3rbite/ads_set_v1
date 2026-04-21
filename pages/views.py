import hashlib
import json
import uuid

from django.conf import settings
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import Conversion, PRODUCT_CHOICES

VALID_PRODUCTS = {slug for slug, _ in PRODUCT_CHOICES}


def landing(request, product):
    if product not in VALID_PRODUCTS:
        return JsonResponse({"error": "not found"}, status=404)
    if "sid" not in request.session:
        request.session["sid"] = uuid.uuid4().hex
    return render(request, f"{product}/landing.html", {"product": product})


@csrf_exempt
@require_POST
def convert(request, product):
    if product not in VALID_PRODUCTS:
        return JsonResponse({"error": "not found"}, status=404)

    try:
        body = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        body = {}

    ip = request.META.get("HTTP_X_FORWARDED_FOR", request.META.get("REMOTE_ADDR", ""))
    if "," in ip:
        ip = ip.split(",")[0].strip()
    ip_hash = hashlib.sha256(ip.encode()).hexdigest()

    Conversion.objects.create(
        product=product,
        user_agent=request.META.get("HTTP_USER_AGENT", ""),
        referrer=request.META.get("HTTP_REFERER", ""),
        session_id=request.session.get("sid", ""),
        ip_hash=ip_hash,
        button_label=body.get("button_label", ""),
    )
    return JsonResponse({"ok": True})


def maintenance(request, product):
    if product not in VALID_PRODUCTS:
        return JsonResponse({"error": "not found"}, status=404)
    return render(request, "maintenance.html", {"product": product})


def dashboard(request):
    key = request.GET.get("key", "")
    if key != settings.DASHBOARD_KEY:
        return JsonResponse({"error": "forbidden"}, status=403)

    totals = (
        Conversion.objects.values("product")
        .annotate(count=Count("id"))
        .order_by("-count")
    )

    by_button = (
        Conversion.objects.values("product", "button_label")
        .annotate(count=Count("id"))
        .order_by("product", "-count")
    )

    by_day = (
        Conversion.objects.annotate(day=TruncDate("timestamp"))
        .values("product", "day")
        .annotate(count=Count("id"))
        .order_by("day")
    )

    unique_visitors = (
        Conversion.objects.values("product")
        .annotate(unique=Count("ip_hash", distinct=True))
        .order_by("-unique")
    )

    return render(request, "dashboard.html", {
        "totals": totals,
        "by_button": by_button,
        "by_day": by_day,
        "unique_visitors": unique_visitors,
    })
