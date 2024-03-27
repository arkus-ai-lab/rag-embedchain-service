from rest_framework import status, generics
from rest_framework.response import Response
import logging
from utilities.rag_handler import RAGHandler
from utilities.config import MODEL_RAG
from rag.api.serializers import FilePathModelSerializer, PromptModelSerializer

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