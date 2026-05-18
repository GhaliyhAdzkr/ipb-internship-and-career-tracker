import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import applicationService from '../services/applicationService';

/**
 * Custom Hook for job application queries and mutations using TanStack Query.
 */
export const useApplications = () => {
  const queryClient = useQueryClient();

  // 1. Query to fetch the current student's own applications list
  const { 
    data: applications = [], 
    isLoading, 
    isError, 
    error,
    refetch 
  } = useQuery({
    queryKey: ['applications', 'my'],
    queryFn: applicationService.getMyApplications,
    staleTime: 5 * 60 * 1000, // 5 minutes stale time
    refetchOnWindowFocus: true,
  });

  // 2. Mutation to update an application status (e.g. withdraw or accept offer)
  const updateStatusMutation = useMutation({
    mutationFn: ({ id, data }) => applicationService.updateStatus(id, data),
    onSuccess: (updatedApp) => {
      // Invalidate the application list to trigger automatic refresh
      queryClient.invalidateQueries({ queryKey: ['applications', 'my'] });
      // Invalidate the specific application's audit history
      queryClient.invalidateQueries({ queryKey: ['applications', updatedApp.id, 'history'] });
    },
  });

  // 3. Mutation to upload acceptance proof (Letter of Acceptance LoA)
  const uploadProofMutation = useMutation({
    mutationFn: ({ id, file }) => applicationService.uploadProof(id, file),
    onSuccess: (data, variables) => {
      queryClient.invalidateQueries({ queryKey: ['applications', 'my'] });
      queryClient.invalidateQueries({ queryKey: ['applications', variables.id, 'history'] });
    },
  });

  return {
    applications,
    isLoading,
    isError,
    error,
    refetch,
    updateStatus: updateStatusMutation.mutateAsync,
    isUpdatingStatus: updateStatusMutation.isPending,
    uploadProof: uploadProofMutation.mutateAsync,
    isUploadingProof: uploadProofMutation.isPending,
  };
};

/**
 * Custom Hook to fetch history/audit trail of a specific application.
 * @param {string} applicationId - The application ID to fetch history for.
 */
export const useApplicationHistory = (applicationId) => {
  return useQuery({
    queryKey: ['applications', applicationId, 'history'],
    queryFn: () => applicationService.getHistory(applicationId),
    enabled: !!applicationId,
    staleTime: 60 * 1000, // 1 minute stale time
    refetchOnWindowFocus: false,
  });
};
