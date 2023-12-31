from django.contrib.auth.mixins import LoginRequiredMixin
from iiol.authentication import JWTCookieAuthentication
from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import render
from .models import MybookWishlist, MybookWishlistGroup
from .serializers import MybookWishlistSerializer, MybookWishlistGroupSerializer
from rest_framework.response import Response
from django.conf import settings
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import filters
from rest_framework import viewsets
from django.db.models import Q
import datetime
from django.contrib.auth import get_user_model
from django.contrib import messages
from iiol.authentication import JWTLoginRequiredMixin
from rest_framework.decorators import action

User = get_user_model()


class MybookWishListViewSet(JWTLoginRequiredMixin, viewsets.ViewSet):
    basename = "mylist"

    permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ["bookname", "isbn13"]

    redirect_filed_name = "redirect_to"
    queryset = MybookWishlist.objects.all()
    serializer_class = MybookWishlistSerializer
    return_json = None
    response_type = "render"
    request = None

    def response_with_type(self, code, msg, RESTCode=200):
        self.set_JSON_header(code, msg)
        self.response_type = self.request.query_params.get("format")
        if self.response_type == "json":
            return JsonResponse(
                data=self.return_json,
                status=RESTCode,
                json_dumps_params={"ensure_ascii": False},
            )
        else:
            return render(
                self.request,
                "mybookwishlist/mylist.html",
                {
                    **self.return_json,
                },
            )

    def set_JSON_header(self, code, msg):
        self.return_json["status"]["code"] = code
        self.return_json["status"]["msg"] = msg

    def list(self, request):
        self.request = request
        self.return_json = {"status": {"code": "", "msg": ""}, "result_data": {}}

        qs = (
            MybookWishlist.objects.all()
            .filter(user=request.user.pk, DELETED=False)
            .order_by("-updated_at")
            .select_related("isbn13")
        )

        groupPk = self.request.query_params.get("groupPk")
        if groupPk is not None:
            if str(groupPk).lower() in ("none", "null"):
                groupPk = None
            qs = qs.filter(groupname=groupPk)

        if not qs.exists():
            return self.response_with_type(
                "S", "Nothing...", RESTCode=status.HTTP_204_NO_CONTENT
            )
        serializer = MybookWishlistSerializer(qs, many=True)
        self.return_json["result_data"]["data"] = serializer.data

        qs_group_dict = {}
        group_qs = (
            MybookWishlistGroup.objects.all()
            .filter(user=request.user.pk, DELETED=False)
            .values("pk", "name")
        )
        if group_qs.exists():
            qs_group_dict = MybookWishlistGroupSerializer(group_qs, many=True).data

        self.return_json["result_data"]["groupname"] = qs_group_dict
        return self.response_with_type("S", "")

    def create(self, request):
        self.request = request
        self.return_json = {"status": {"code": "", "msg": ""}, "result_data": {}}
        self.response_type = "json"

        qs = MybookWishlist.objects.all().filter(
            user=request.user.pk, isbn13=request.data["isbn13"]
        )
        if qs.exists():
            if qs[0].DELETED == True:
                serializer = MybookWishlistSerializer(
                    qs[0], data={"DELETED": False}, partial=True
                )
                if serializer.is_valid():
                    serializer.save()
                    self.return_json[
                        "result_data"
                    ] = MybookWishlistSerializer().to_representation(qs[0])
                    return self.response_with_type(
                        "S", "삭제되어있던 Mywishlist에서 복원했습니다.", RESTCode=status.HTTP_200_OK
                    )
                else:
                    return self.response_with_type(
                        "E",
                        str(serializer.errors),
                        RESTCode=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )
            else:
                self.return_json[
                    "result_data"
                ] = MybookWishlistSerializer().to_representation(qs[0])
                return self.response_with_type(
                    "E", "이미 저장되었습니다.", RESTCode=status.HTTP_409_CONFLICT
                )
        else:
            serializer = MybookWishlistSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                self.return_json["result_data"] = serializer.data
                return self.response_with_type(
                    "S",
                    "성공적으로 MyBookwishlist에 추가했습니다!",
                    RESTCode=status.HTTP_201_CREATED,
                )
            else:
                return self.response_with_type(
                    "E", str(serializer.errors), RESTCode=status.HTTP_400_BAD_REQUEST
                )

    def partial_update(self, request, pk):
        self.request = request
        self.return_json = {"status": {"code": "", "msg": ""}, "result_data": {}}
        self.response_type = "json"
        try:
            item = MybookWishlist.objects.get(
                isbn13=pk, user=request.user.pk, DELETED=False
            )
        except MybookWishlist.DoesNotExist:
            return self.response_with_type(
                "E",
                "내 mybookwishlist에서 해당 도서를 찾을 수 없었습니다. ",
                RESTCode=status.HTTP_404_NOT_FOUND,
            )

        if "readYn" in request.data.keys():
            request.data["readDate"] = datetime.date.today()

        print(request.data)
        serializer = MybookWishlistSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            print(serializer.validated_data)
            serializer.save()
            self.return_json["result_data"] = serializer.data
            return self.response_with_type(
                "S", "정보 수정에 성공했습니다.", RESTCode=status.HTTP_200_OK
            )
        else:
            print(serializer.errors)
        return self.response_with_type(
            "E", serializer.errors, RESTCodㅍe=status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request, pk):
        self.request = request
        self.return_json = {"status": {"code": "", "msg": ""}, "result_data": {}}
        self.response_type = "json"
        try:
            item = MybookWishlist.objects.get(
                isbn13=pk, user=request.user.pk, DELETED=False
            )
        except MybookWishlist.DoesNotExist:
            return self.response_with_type(
                "E",
                "해당 도서를 찾을 수 없었습니다. \n 이미 삭제되었는지 확인하십시오. ",
                RESTCode=status.HTTP_404_NOT_FOUND,
            )
        serializer = MybookWishlistSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            self.return_json["result_data"] = serializer.data
            return self.response_with_type(
                "S", "삭제에 성공하였습니다.", RESTCode=status.HTTP_202_ACCEPTED
            )
        return self.response_with_type(
            "E", "삭제에 실패하였습니다.", RESTCode=status.HTTP_406_NOT_ACCEPTABLE
        )

    @action(detail=False, methods=["post"])
    def create_group(self, request):
        self.request = request
        self.return_json = {"status": {"code": "", "msg": ""}, "result_data": {}}
        self.response_type = "json"

        qs = MybookWishlistGroup.objects.filter(user=request.user.pk, DELETED=False)
        if qs.count() > 10:
            return self.response_with_type(
                "E", "분류는 10개까지만 만들 수 있습니다.", RESTCode=status.HTTP_400_BAD_REQUEST
            )

        if request.data["name"] == "":
            return self.response_with_type(
                "E", "새 분류 이름은 공란일 수 없습니다.", RESTCode=status.HTTP_400_BAD_REQUEST
            )

        qs = qs.filter(name=request.data["name"])

        if qs.exists():
            return self.response_with_type(
                "E", "이미 존재하는 분류입니다.", RESTCode=status.HTTP_409_CONFLICT
            )

        serializer = MybookWishlistGroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            self.return_json["result_data"] = serializer.data
            return self.response_with_type(
                "S", "새로운 분류를 추가했습니다.", RESTCode=status.HTTP_201_CREATED
            )
        else:
            return self.response_with_type(
                "E", str(serializer.errors), RESTCode=status.HTTP_400_CREATED
            )

    @action(detail=True, methods=["patch"])
    def update_group(self, request, groupPk=None):
        self.request = request
        self.return_json = {"status": {"code": "", "msg": ""}, "result_data": {}}
        self.response_type = "json"
        if groupPk == None:
            return self.response_with_type(
                "E", "수정할 분류가 지정되지 않았습니다.", RESTCode=status.HTTP_400_BAD_REQUEST
            )

        try:
            item = MybookWishlistGroup.objects.get(
                user=request.user.pk, pk=groupPk, DELETED=False
            )
        except MybookWishlistGroup.DoesNotExist:
            return self.response_with_type(
                "E", "수정하려는 분류가 존재하지 않습니다.", RESTCode=status.HTTP_404_NOT_FOUND
            )

        request.data["name"] = request.data["groupname"]
        serializer = MybookWishlistGroupSerializer(
            item, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            self.return_json["result_data"] = serializer.data

        return self.response_with_type("S", "변경했습니다 !", RESTCode=status.HTTP_200_OK)

    @action(detail=True, methods=["delete"])
    def delete_group(self, request, groupPk=None):
        self.request = request
        self.return_json = {"status": {"code": "", "msg": ""}, "result_data": {}}
        self.response_type = "json"
        if groupPk == None:
            return self.response_with_type(
                "E", "삭제할 분류가 지정되지 않았습니다.", RESTCode=status.HTTP_400_BAD_REQUEST
            )
        try:
            item = MybookWishlistGroup.objects.get(
                user=request.user.pk, pk=groupPk, DELETED=False
            )
        except MybookWishlistGroup.DoesNotExist:
            return self.response_with_type(
                "E", "삭제하려는 분류가 존재하지 않습니다.", RESTCode=status.HTTP_404_NOT_FOUND
            )
        serializer = MybookWishlistGroupSerializer(
            item, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()

        return self.response_with_type("S", "분류를 삭제했습니다.", RESTCode=status.HTTP_200_OK)
