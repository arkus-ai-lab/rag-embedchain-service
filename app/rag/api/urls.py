"""URLs for RAG API"""
from django.urls import path
from rag.api.views import RAGAddView, RAGChatView

urlpatterns = [
    path('rag-add/', RAGAddView.as_view(), name='rag'),
    path('rag-chat/', RAGChatView.as_view(), name='rag-chat'),
]