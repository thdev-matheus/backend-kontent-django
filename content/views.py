from django.forms.models import model_to_dict
from rest_framework.views import APIView, Response, status

from .models import Content


class ContentView(APIView):
    def get(self, request):
        contents = Content.objects.all()
        contents_dict = [model_to_dict(content) for content in contents]

        return Response(contents_dict)

    def validation_create_data(self, data) -> dict or bool:
        keys = data.keys()
        result = {}

        if "title" not in keys:
            result["title"] = "missing key"
        elif type(data["title"]) != str:
            result["title"] = "must be a str"

        if "module" not in keys:
            result["module"] = "missing key"
        elif type(data["module"]) != str:
            result["module"] = "must be a str"

        if "description" not in keys:
            result["description"] = "missing key"
        elif type(data["description"]) != str:
            result["description"] = "must be a str"

        if "students" not in keys:
            result["students"] = "missing key"
        elif type(data["students"]) != int:
            result["students"] = "must be a int"

        if "is_active" not in keys:
            result["is_active"] = "missing key"
        elif type(data["is_active"]) != bool:
            result["is_active"] = "must be a bool"

        return result

    def data_processing(self, data) -> dict:
        result = {
            "title": data["title"],
            "module": data["module"],
            "description": data["description"],
            "students": data["students"],
            "is_active": data["is_active"]
        }

        return result

    def post(self, request):
        val_data = self.validation_create_data(request.data)

        if not val_data:
            data_proc = self.data_processing(request.data)
            new_content = Content.objects.create(**data_proc)
            return Response(model_to_dict(new_content), status.HTTP_201_CREATED)
        else:
            return Response(val_data, status.HTTP_400_BAD_REQUEST)
