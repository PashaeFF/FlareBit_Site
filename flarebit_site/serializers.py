# serializers.py
from rest_framework import serializers
from project_request.models import ProjectRequest, ProjectFiles
from datetime import date
import re

from rest_framework import serializers
import mimetypes

class ProjectFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectFiles
        fields = '__all__'

    def validate(self, data):
        file = data.get('file')

        if file:
            allowed_mime_types = [
                'application/pdf',
                'application/msword',                      # .doc
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document',  # .docx
                'application/vnd.ms-excel',                # .xls
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',  # .xlsx
                'text/csv',
                'image/jpeg',
                'image/png',
                'image/gif',
                'image/webp',
                'video/mp4',
                'video/quicktime',
                'video/x-msvideo',    # avi
                'video/x-matroska',   # mkv
            ]

            file_mime_type, _ = mimetypes.guess_type(file.name)

            if file_mime_type not in allowed_mime_types:
                raise serializers.ValidationError(f"{file.name} file type is not supported.")
        
        return data


class ProjectRequestSerializer(serializers.ModelSerializer):
    project_files = ProjectFilesSerializer(many=True, read_only=True)

    class Meta:
        model = ProjectRequest
        fields = (
            'description', 'service', 'request_date', 'contact_name', 'organization',
            'job_title', 'email', 'phone_number', 'how_did_you_hear_about_us', 'project_files'
        )

    def validate_request_date(self, value):
        if value and value < date.today():
            raise serializers.ValidationError("Request date cannot be in the past.")
        return value

    def validate_phone_number(self, value):
        # Yalnız icazə verilən simvollar: rəqəmlər, +, -, (, )
        if not re.fullmatch(r'^[\d\+\-\(\)\s]+$', value):
            raise serializers.ValidationError("Phone number only digits, +, -, ( and ) are allowed.")
        
        # Ən azı bir rəqəm olmalıdır
        if not re.search(r'\d', value):
            raise serializers.ValidationError("Phone number must contain at least one digit.")
        
        return value
