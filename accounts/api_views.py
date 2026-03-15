from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import AccountSerializer
from .services import AccountService


class MeApi(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = AccountService.get_account(request.user)
        return Response(AccountSerializer(user).data)
