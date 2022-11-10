from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import mixins
from rest_framework import status
from rest_framework.response import Response
from rest_framework.settings import api_settings
from studies.serializers import StudentSrlz, StudentsListSerializer
from studies.models import User, EducationGroups, Faculty, Student
from ..serializers import EducationGroupsSrlz, FacultySrlz, StudentSrlz
from studies.permissions_user import IsCurator, IsAdmin
from studies.tasks import report, report_2


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
        possible_number = 20 - Student.objects.filter(group=data["group"]).count()
        print(possible_number)
        print(type(possible_number))
        delta = possible_number - len(data)
        if delta >= 0:
            req_data = [{'group': data["group"], 'student_user': i} for i in data['students']]
            serializer = StudentSrlz(data=req_data, many=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"Add": serializer.data})
        else:
            return Response({"Ошибка": f"В эту группу можно добавить только на {abs(delta)} студентов меньше"})


class CustomCreateModelMixin:
    """
    Create a model instance.
    """
    def create(self, request, *args, **kwargs):
        free_place = Student.objects.filter(group=request.data["group"]).count()
        if  free_place < 20:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return "В группе нет свободных мест"

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
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


class StudentViewSet(CustomCreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
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

