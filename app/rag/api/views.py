from rest_framework import status, generics
from django.views.generic import TemplateView
from rest_framework.response import Response
import logging
from utilities.rag_handler import RAGHandler
from utilities.config import MODEL_RAG
from rag.api.serializers import FilePathModelSerializer, PromptModelSerializer
from django.core.files.storage import FileSystemStorage
import os
from django.shortcuts import render

class RAGAddView(generics.GenericAPIView):
    """Handle POST Adds a new source to the Embedchain app."""
    serializer_class = FilePathModelSerializer
    
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            path = serializer.validated_data['path']          
            
            rag_handler = RAGHandler(MODEL_RAG)
            source = rag_handler.add_source(path)
            return Response({'source': source, 'file_path': path}, status=status.HTTP_200_OK)   
        except Exception as e:            
            logging.exception("Unexpected error occurred when adding RAG resources.")
            return Response({"detail": " An unexpected error occurred, " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class RAGChatView(generics.GenericAPIView):
    """RAG Chat API view."""
    serializer_class = PromptModelSerializer

    def post(self, request, *args, **kwargs):
        """Function to handle POST requests."""
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            prompt = serializer.validated_data['prompt']

            rag_handler = RAGHandler(MODEL_RAG)
            response = rag_handler.get_rag_response(prompt)
            
            return Response({
                'response': response
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logging.exception("Unexpected error occurred when checking unseen emails.")
            return Response({"detail": " An unexpected error occurred, " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class RAGAddFileView(TemplateView):
    """RAG Add File API view."""
    template_name = 'rag_add.html'
    def post(self, request, *args, **kwargs):
        """Function to handle POST requests."""
        if request.method == 'POST' and request.FILES['file']:     
            file = request.FILES['file']
            file_type = file.content_type
            print("File type detected:", file_type)
            file_system = FileSystemStorage()
            file_path = file_system.save(file.name, file)
            file_name = os.path.basename(file_path)
            uploaded_file_url = f"media/{file_path}"
            print("File name: ", file_name)
            print("File path: ", file_path)
            print("File type: ", file_type)
            if uploaded_file_url:
                print("Adding data to the app")
                try:
                    data_type_mapping = {
                        'application/pdf': 'pdf_file',
                        'text/csv': 'csv',
                        'application/json': 'json',
                        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'docx'
                    }
                    data_type = data_type_mapping.get(file_type)
                    if not data_type:
                        raise ValueError('Unsupported file type')
                    RAGHandler(MODEL_RAG).add_rag_source(uploaded_file_url, data_type=data_type)
                    success_message = "File uploaded successfully!"
                    file_system.delete(file_path)
                    return render(request, 'rag_add.html', {'success_message': success_message})
                except Exception as e:
                    file_system.delete(file_path)
                    return render(request, 'rag_add.html', {
                        'error': 'Error occurred while adding file to the app. ' + str(e)
                    })
        return render(request, 'rag_add.html', {
            'error': 'Error occurred while uploading file.'
        })