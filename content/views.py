from django.forms.models import model_to_dict
from rest_framework.views import APIView, Response, status

from .models import Content


class ValidationFieldsError(Exception):
    pass


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
            "is_active": data["is_active"],
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


class ContentParamView(APIView):
    def get(self, request, content_id):
        try:
            content = Content.objects.get(pk=content_id)
        except Content.DoesNotExist:
            return Response({"Error": "Content not found"}, status.HTTP_404_NOT_FOUND)

        content_dict = model_to_dict(content)

        return Response(content_dict)

    def data_processing(self, data) -> dict:
        keys = data.keys()
        result = {}

        if "title" in keys:
            result["title"] = data["title"]

        if "module" in keys:
            result["module"] = data["module"]

        if "description" in keys:
            result["description"] = data["description"]

        if "students" in keys:
            result["students"] = data["students"]

        if "is_active" in keys:
            result["is_active"] = data["is_active"]

        return result

    def validation_update_data(self, data) -> dict or bool:
        keys = data.keys()
        result = {}

        if "title" in keys:
            if type(data["title"]) != str:
                result["title"] = "must be a str"

        if "module" in keys:
            if type(data["module"]) != str:
                result["module"] = "must be a str"

        if "description" in keys:
            if type(data["description"]) != str:
                result["description"] = "must be a str"

        if "students" in keys:
            if type(data["students"]) != int:
                result["students"] = "must be a int"

        if "is_active" in keys:
            if type(data["is_active"]) != bool:
                result["is_active"] = "must be a bool"

        return result

    def patch(self, request, content_id):
        try:
            strip_unknow_data = self.data_processing(request.data)
            no_validate_data = self.validation_update_data(strip_unknow_data)

            if no_validate_data:
                raise ValidationFieldsError(no_validate_data)

            content = Content.objects.get(id=content_id)

            for key, value in strip_unknow_data.items():
                setattr(content, key, value)

            content.save()

            return Response(model_to_dict(content))
        except Content.DoesNotExist:
            return Response({"Error": "Content not found"}, status.HTTP_404_NOT_FOUND)

        except ValidationFieldsError as err:
            return Response(err, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, content_id):
        try:
            content = Content.objects.get(id=content_id).delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Content.DoesNotExist:
            return Response({"Error": "Content not found"}, status.HTTP_404_NOT_FOUND)


class ContentFilterView(APIView):
    def get(self, request):
        title = request.query_params.get("title", None)

        contents = Content.objects.filter(title=title)
        contents_dict = [model_to_dict(content) for content in contents]

        return Response(contents_dict)
