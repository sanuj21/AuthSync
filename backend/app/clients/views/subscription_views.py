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
from rest_framework.views import APIView


from ..serializers import SubscriptionSerializer, PaymentSerializer
from ..models import Subscription, Payment, ClientApp, ApiPlan
from ..permissions import isOwner

def generate_api_key():
    return uuid.uuid4().hex



env = environ.Env()
environ.Env.read_env()

# For Owner to manage Subscriptions

class SubscriptionListCreateView(APIView):
    permission_classes = [IsAuthenticated, isOwner]

    def post(self, request, *args, **kwargs):
        plan = request.data['plan']

        if plan == 'Free':
            no_of_days = 365
        else:
            no_of_days = request.data['no_of_days']

        # Get the client id from app_pk url
        client_app = ClientApp.objects.get(id=self.kwargs['app_pk'])

        # Get this info from plan selected by user i.e(Free, Basic, Premium), i.e in request.data
        api_plan = ApiPlan.objects.get(name = plan)

        subs_end_date = now() + timedelta(days= no_of_days)

        subscription = Subscription.objects.create(
            end_date = subs_end_date,
            client_app = client_app,
            plan = api_plan,
            api_key = generate_api_key(),
            api_key_expires = subs_end_date
        )

        amount = request.data['amount']

        # If plan is free then no need to create payment
        if plan == 'Free':
            return Response(SubscriptionSerializer(subscription).data)


        # setup razorpay client this is the client to whome user is paying money that's you
        client = razorpay.Client(auth=(env('PUBLIC_KEY'), env('SECRET_KEY')))

        # create razorpay order
        payment = client.order.create({"amount": int(amount) * 100,
                                        "currency": "INR",
                                        "payment_capture": "1"})

        payment = Payment.objects.create(
            amount=amount,
            subscription=subscription,
            order_id=payment['id']
        )

        paymentSerializer = PaymentSerializer(payment)
        subscriptionSerializer = SubscriptionSerializer(subscription)

        response_data = {
            "subscription": subscriptionSerializer.data,
            "payment": paymentSerializer.data
        }

        return Response(response_data)


    def get(self, request, *args, **kwargs):
        subscriptions = Subscription.objects.filter(client_app=self.kwargs['app_pk'])
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data)



class SubscriptionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, isOwner]

    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer


#* --------------------------------------------- *#


"""
@api_view(['POST'])
def start_payment(request):
    # request.data is coming from frontend
    amount = request.data['amount']
    no_of_days = request.data['no_of_days']
    logged_in_user = request.user


    # setup razorpay client this is the client to whome user is paying money that's you
    client = razorpay.Client(auth=(env('PUBLIC_KEY'), env('SECRET_KEY')))

    # create razorpay order
    payment = client.order.create({"amount": int(amount),
                                   "currency": "INR",
                                   "payment_capture": "1"})

    # Get this info from login user, he will be owner
    client_app = ClientApp.objects.get(owner = logged_in_user)

    # Get this info from plan selected by user i.e(Free, Basic, Premium), i.e in request.data
    api_plan = ApiPlan.objects.get(name = request.data['plan'])

    subs_end_date = now() + timedelta(days=no_of_days)

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
"""

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

    subscription = payment.subscription
    subscription.is_Active = True
    subscription.save()


    res_data = {
        'message': 'payment successfully received!'
    }

    return Response(res_data)




