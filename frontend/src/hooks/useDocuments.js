import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import documentService from '../services/documentService';

export const useDocuments = () => {
  const queryClient = useQueryClient();

  const documentsQuery = useQuery({
    queryKey: ['documents'],
    queryFn: documentService.listDocuments,
    // Lakukan polling setiap 30 detik selama status dokumen masih pending atau processing
    refetchInterval: (query) => {
      const docs = query.state.data;
      if (!docs) return false;
      const hasPending = docs.some((d) => d.status === 'PENDING' || d.status === 'PROCESSING');
      return hasPending ? 30000 : false;
    },
  });

  const requestMutation = useMutation({
    mutationFn: documentService.requestDocument,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['documents'] });
    },
  });

  return {
    documents: documentsQuery.data || [],
    isLoading: documentsQuery.isLoading,
    requestDocument: requestMutation.mutateAsync,
    isRequesting: requestMutation.isPending,
    requestError: requestMutation.error,
  };
};
