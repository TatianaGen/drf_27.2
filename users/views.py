from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from users.models import User, Payments
from users.serializer import UserSerializer, PaymentsSerializer
from users.services import create_stripe_product, create_stripe_price, create_stripe_session
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class PaymentsListAPIView(ListAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = [
        "course",
        "lesson",
    ]
    ordering_fields = ("date",)
    search_fields = ("payment_method",)

    class PaymentsCreateAPIView(CreateAPIView):
        serializer_class = PaymentsSerializer
        queryset = Payments.objects.all()

        def perform_create(self, serializer):
            payment = serializer.save(user=self.request.user)
            product_id = create_stripe_product(payment)
            price_id = create_stripe_price(product_id, payment)
            session_id, session_url = create_stripe_session(price_id)
            payment.session_id = session_id
            payment.link = session_url
            payment.save()
