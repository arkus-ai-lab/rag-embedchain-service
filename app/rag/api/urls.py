"""URLs for RAG API"""
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from rag.api.views import RAGAddView, RAGChatView, RAGAddFileView

urlpatterns = [
    path('rag-add/', RAGAddView.as_view(), name='rag'),
    path('rag-chat/', RAGChatView.as_view(), name='rag-chat'),
    path('rag-add/file/', RAGAddFileView.as_view(), name='rag-add-file'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )