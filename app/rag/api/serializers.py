"""Serializers for RAG API"""
from rest_framework import serializers
from core.models import FilePathModel, PromptModel

class FilePathModelSerializer(serializers.ModelSerializer):
    """Serializer for FilePathModel"""
    class Meta:
        model = FilePathModel
        fields = '__all__'


class PromptModelSerializer(serializers.ModelSerializer):
    """Serializer for PromptModel"""
    class Meta:
        model = PromptModel
        fields = '__all__'