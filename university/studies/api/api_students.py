from django.conf import settings
from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from studies.models import EducationGroups, Faculty, Student, User
from studies.permissions_user import IsAdmin, IsCurator
from studies.serializers import StudentSrlz
from studies.tasks import report, report_2, send_email_students_created

from ..serializers import EducationGroupsSrlz, FacultySrlz, StudentSrlz

EMAIL_STUDENT_CREATED = """Вы зачислены в группу {} на направление {}"""


class StudentsApiView(APIView):
    """
    Получить список всех студентов
    """

    def get(self, request):
        qs = User.objects.filter(roles__icontains="STUDENT").values()
        return Response({"students": StudentSrlz(qs, many=True).data})


class MassComplectationGroup(APIView):
    """
    Зачислить сразу несколько студентов в группу
    """

    def post(self, request):
        data = request.data
        lst_id = [i["student_user"] for i in data["students"]]
        qs = Student.objects.filter(group=data["group"]).filter(student_user_id__in=lst_id).values()
        possible_number = 20 - qs.count()
        delta = possible_number - len(data)
        if delta >= 0:

            req_data = [i for i in data["students"]]
            for j in req_data:
                j.update({"group": data["group"]})

            serializer = StudentSrlz(data=req_data, many=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            emails = [item["email"] for item in qs]
            query = EducationGroups.objects.filter(pk=data["group"]).first()
            gr = query.name
            fac = query.faculty.name

            send_email_students_created.delay(
                subject="Зачисление в университет",
                from_email=settings.EMAIL_HOST_USER,
                to=emails,
                body=EMAIL_STUDENT_CREATED.format(gr, fac),
            )
            return Response({"Add": serializer.data})
        else:
            return Response(
                {
                    "Ошибка": f"В эту группу можно добавить только на {abs(delta)} студентов меньше"
                }
            )


class CustomCreateModelMixin:
    """
    Create a model instance.
    """

    def create(self, request, *args, **kwargs):
        free_place = Student.objects.filter(group=request.data["group"]).count()
        if free_place < 20:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            query = EducationGroups.objects.filter(pk=request.data["group"]).first()
            gr = query.name
            fac = query.faculty.name

            if serializer.data["email"]:
                send_email_students_created.delay(
                    subject="Зачисление в университет",
                    from_email=settings.EMAIL_HOST_USER,
                    to=[serializer.data["email"]],
                    body=EMAIL_STUDENT_CREATED.format(gr, fac),
                )

            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )
        return "В группе нет свободных мест"

    def get_success_headers(self, data):
        try:
            return {"Location": str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class GroupOperationsViewSet(ModelViewSet):
    """
    CRUD студенческой группы
    """

    queryset = EducationGroups.objects.all()
    serializer_class = EducationGroupsSrlz
    permission_classes = [IsCurator]


class FacultyApiView(APIView):
    """
    Получить список факультетов
    """

    def get(self, request):
        qs = Faculty.objects.all()
        return Response({"faculty": FacultySrlz(qs, many=True).data})


class StudentViewSet(
    CustomCreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    """
    CRUD студентов
    """

    queryset = Student.objects.all()
    serializer_class = StudentSrlz
    permission_classes = [IsCurator]


class Report(APIView):
    """
    Генерация отчета
    """

    permission_classes = [IsAdmin]

    def get(self, request):
        report.delay()
        return Response({"res": "OK"})


class ReportGroups(APIView):
    """
    Генерация отчета
    """

    permission_classes = [IsAdmin]

    def get(self, request):
        report_2.delay()
        return Response({"res": "OK"})
