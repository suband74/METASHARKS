from rest_framework import serializers
from studies.models import Student, EducationGroups, Faculty, Subjects


class SubjectSrlz(serializers.ModelSerializer):
    class Meta:
        model = Subjects
        fields = ["id", "name"]


class StudentsListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        students = [Student(**item) for item in validated_data]
        return Student.objects.bulk_create(students)


class StudentSrlz(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"
        list_serializer_class = StudentsListSerializer

class EducationGroupsSrlz(serializers.ModelSerializer):
    class Meta:
        model = EducationGroups
        fields = "__all__"

class FacultySrlz(serializers.ModelSerializer):
    subjects_of_study = SubjectSrlz(many=True)
    class Meta:
        model = Faculty
        fields = ["id", "name", "subjects_of_study"]
