"""Django Models"""
from django.db import models

class FilePathModel(models.Model):
    """Model for storing file paths"""
    path = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.path
    
class PromptModel(models.Model):
    """Model for storing prompts"""
    prompt = models.TextField()

    def __str__(self):
        return self.prompt