from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.conf import settings

from .models import customer, Order

from rest_framework.views import APIView

import razorpay


class LoginView(APIView):
    def get(self, request):
        if request.session.get("customer_id"):
            return redirect("home")
        return render(request, "login.html")


class IndexView(APIView):
    def get(self, request):
        return render(request, "index.html")


class CollectionView(APIView):
    def get(self, request):
        return render(request, "collection.html")


class AboutView(APIView):
    def get(self, request):
        return render(request, "about.html")


class ServiceView(APIView):
    def get(self, request):
        return render(request, "service.html")


class ContactView(APIView):
    def get(self, request):
        return render(request, "contact.html")

class RegisterView(APIView):
    def get(self, request):
        return render(request, "register.html")

class BynowView(APIView):
    def get(self, request):
        return render(request, "bynow.html")
class CheckoutView(APIView):
    def get(self, request):
        return render(request, "checkout.html",
        {"booking_amount": f"{settings.BOOKING_AMOUNT_INR:,}"})
class CreateOrderView(APIView):
    def post(self, request):
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        car_brand = request.POST.get("car_brand")
        car_name = request.POST.get("car_name")
        car_color = request.POST.get("car_color")
        car_price = request.POST.get("car_price")

        amount_inr = settings.BOOKING_AMOUNT_INR
        amount_paise = amount_inr * 100

        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )

        razorpay_order = client.order.create(
            dict(amount=amount_paise, currency="INR", payment_capture=1)
        )

        order = Order(
            name=name,
            phone=phone,
            address=address,
            car_brand=car_brand,
            car_name=car_name,
            car_color=car_color,
            car_price=car_price,
            amount_paise=amount_paise,
            razorpay_order_id=razorpay_order["id"],
        )
        order.save()

        return JsonResponse(
            {
                "order_id": razorpay_order["id"],
                "amount_inr": f"{amount_inr:,}",
                "razorpay_key_id": settings.RAZORPAY_KEY_ID,
            }
        )

from django.conf import settings

client = razorpay.Client(
    auth=(
        settings.RAZORPAY_KEY_ID,
        settings.RAZORPAY_KEY_SECRET
    )
)

class CustomerSaveView(APIView):
    def post(self, request):

        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        place = request.POST.get("place")
        password = request.POST.get("password")

        o = customer(
            customer_name=name,
            customer_phone=phone,
            customer_email=email,
            customer_place=place,
            customer_password=password
        )

        o.save()

        return redirect("login")

def check_login_details(request):

    if request.method == "POST":

        email = (request.POST.get("email") or "").strip()
        password = request.POST.get("password")

        people = customer.objects.filter(customer_email=email).first()

        if people is None:
            return render(request, "login.html", {"error": "Email not found"})

        if people.customer_password != password:
            return render(request, "login.html", {"error": "Wrong password"})

        # login success -> remember the user, go to home page
        request.session["customer_id"] = people.id
        request.session["customer_name"] = people.customer_name
        return redirect("home")

    return render(request, "login.html")


def logout_view(request):
    request.session.flush()
    return redirect("login")
# ── RAZORPAY PAYMENT ────────────────────────────────────────
def _razorpay_client():
    return razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


class CreateOrderView(APIView):
    def post(self, request):
        d = request.data
        name = (d.get("name") or "").strip()
        phone = (d.get("phone") or "").strip()
        address = (d.get("address") or "").strip()
        if not (name and phone and address):
            return JsonResponse({"error": "Name, phone and address are required"}, status=400)

        amount_paise = settings.BOOKING_AMOUNT_INR * 100

        try:
            rp_order = _razorpay_client().order.create({
                "amount": amount_paise,
                "currency": "INR",
                "payment_capture": 1,
            })
        except Exception as e:
            return JsonResponse({"error": "Could not start payment: %s" % e}, status=502)

        Order.objects.create(
            name=name, phone=phone, address=address,
            car_brand=d.get("brand", ""), car_name=d.get("car", ""),
            car_color=d.get("color", ""), car_price=d.get("price", ""),
            amount_paise=amount_paise,
            razorpay_order_id=rp_order["id"],
        )
        return JsonResponse({
            "key": settings.RAZORPAY_KEY_ID,
            "order_id": rp_order["id"],
            "amount": amount_paise,
            "name": name, "phone": phone,
        })


class VerifyPaymentView(APIView):
    def post(self, request):
        d = request.data
        order_id = d.get("razorpay_order_id", "")
        payment_id = d.get("razorpay_payment_id", "")
        signature = d.get("razorpay_signature", "")

        order = Order.objects.filter(razorpay_order_id=order_id).first()
        if order is None:
            return JsonResponse({"ok": False, "error": "Order not found"}, status=404)

        try:
            _razorpay_client().utility.verify_payment_signature({
                "razorpay_order_id": order_id,
                "razorpay_payment_id": payment_id,
                "razorpay_signature": signature,
            })
        except Exception:
            order.status = "failed"
            order.save()
            return JsonResponse({"ok": False, "error": "Signature verification failed"}, status=400)

        order.status = "paid"
        order.razorpay_payment_id = payment_id
        order.save()
        return JsonResponse({"ok": True, "order_id": order_id})


class PaymentSuccessView(APIView):
    def get(self, request):
        order = Order.objects.filter(
            razorpay_order_id=request.GET.get("order_id", ""), status="paid").first()
        return render(request, "payment_success.html", {"order": order})