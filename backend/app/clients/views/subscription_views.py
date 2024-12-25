import uuid
import razorpay
import environ
import json
from datetime import timedelta
from django.utils.timezone import now

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


from ..serializers import SubscriptionSerializer, PaymentSerializer
from ..models import Subscription, Payment, ClientApp, ApiPlan
from ..permissions import isOwner

def generate_api_key():
    return uuid.uuid4().hex


# For Owner to manage Subscriptions
class SubscriptionListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, isOwner]

    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer


class SubscriptionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, isOwner]

    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer


#* --------------------------------------------- *#


env = environ.Env()

# you have to create .env file in same folder where you are using environ.Env()
# reading .env file which located in api folder
environ.Env.read_env()


@api_view(['POST'])
def start_payment(request):
    # request.data is coming from frontend
    amount = request.data['amount']

    # setup razorpay client this is the client to whome user is paying money that's you
    client = razorpay.Client(auth=(env('PUBLIC_KEY'), env('SECRET_KEY')))

    # create razorpay order
    payment = client.order.create({"amount": int(amount),
                                   "currency": "INR",
                                   "payment_capture": "1"})

    client_app = ClientApp.objects.get(owner = "123")
    api_plan = ApiPlan.objects.get(id = "123e4567-e89b-12d3-a456-426614174001")

    subs_end_date = now() + timedelta(days=30)

    subscription = Subscription.objects.create(
        end_date = subs_end_date,
        client_app = client_app,
        plan = api_plan,
    )

    payment = Payment.objects.create(
                                amount=amount,
                                subscription=subscription,
                                order_id=payment['id'])


    serializer = PaymentSerializer(payment)


    return Response(serializer.data)


@api_view(['POST'])
def handle_payment_success(request):
    # request.data is coming from frontend
    res = json.loads(request.data["response"])

    """res will be:
    {'razorpay_payment_id': 'pay_G3NivgSZLx7I9e',
    'razorpay_order_id': 'order_G3NhfSWWh5UfjQ',
    'razorpay_signature': '76b2accbefde6cd2392b5fbf098ebcbd4cb4ef8b78d62aa5cce553b2014993c0'}
    this will come from frontend which we will use to validate and confirm the payment
    """

    ord_id = ""
    raz_pay_id = ""
    raz_signature = ""

    # res.keys() will give us list of keys in res
    for key in res.keys():
        if key == 'razorpay_order_id':
            ord_id = res[key]
        elif key == 'razorpay_payment_id':
            raz_pay_id = res[key]
        elif key == 'razorpay_signature':
            raz_signature = res[key]

    # get order by payment_id which we've created earlier with isPaid=False
    payment = Payment.objects.get(order_id=ord_id)

    # we will pass this whole data in razorpay client to verify the payment
    data = {
        'razorpay_order_id': ord_id,
        'razorpay_payment_id': raz_pay_id,
        'razorpay_signature': raz_signature
    }

    client = razorpay.Client(auth=(env('PUBLIC_KEY'), env('SECRET_KEY')))

    # checking if the transaction is valid or not by passing above data dictionary in
    # razorpay client if it is "valid" then check will return None
    check = client.utility.verify_payment_signature(data)

    print(check)
    if check is not True:
        print("Redirect to error url or error page")
        return Response({'error': 'Something went wrong'})

    # if payment is successful that means check is None then we will turn isPaid=True
    payment.status = 'COMPLETED'
    payment.provider_payment_id = raz_pay_id
    payment.provider_order_id = ord_id
    payment.provider_signature = raz_signature
    payment.save()

    res_data = {
        'message': 'payment successfully received!'
    }

    return Response(res_data)
