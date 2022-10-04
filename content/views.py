from django.forms.models import model_to_dict
from rest_framework.views import APIView, Response, status

from .models import Content
from .utils import data_processing, validation_create_data, validation_update_data


class ValidationFieldsError(Exception):
    pass


class ContentView(APIView):
    def get(self, request):
        contents = Content.objects.all()
        contents_dict = [model_to_dict(content) for content in contents]

        return Response(contents_dict)

    def post(self, request):
        val_data = validation_create_data(request.data)

        if not val_data:
            data_proc = data_processing(request.data)
            new_content = Content.objects.create(**data_proc)
            return Response(model_to_dict(new_content), status.HTTP_201_CREATED)
        else:
            return Response(val_data, status.HTTP_400_BAD_REQUEST)


class ContentParamView(APIView):
    def get(self, request, content_id):
        try:
            content = Content.objects.get(id=content_id)
        except Content.DoesNotExist:
            return Response({"Error": "Content not found"}, status.HTTP_404_NOT_FOUND)

        content_dict = model_to_dict(content)

        return Response(content_dict)

    def patch(self, request, content_id):
        try:
            strip_unknow_data = data_processing(request.data)
            no_validate_data = validation_update_data(strip_unknow_data)

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
