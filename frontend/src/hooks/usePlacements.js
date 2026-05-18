import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import placementService from '../services/placementService';

// Query:

export const usePlacements = () => {
  return useQuery({
    queryKey: ['placements', 'my'],
    queryFn: placementService.getMyPlacements,
    staleTime: 5 * 60 * 1000,
  });
};

export const useActivityLogs = (placementId) => {
  return useQuery({
    queryKey: ['placements', placementId, 'logs'],
    queryFn: () => placementService.getLogs(placementId),
    enabled: !!placementId,
    staleTime: 2 * 60 * 1000,
  });
};

export const useReportStatus = (placementId) => {
  return useQuery({
    queryKey: ['placements', placementId, 'report'],
    queryFn: () => placementService.getReport(placementId),
    enabled: !!placementId,
    refetchInterval: (query) => {
      const data = query.state.data;
      if (data?.status === 'generated') return false;
      return 30000;
    },
  });
};

// Mutasi:

export const useActivityLogMutations = (placementId) => {
  const queryClient = useQueryClient();

  const createLog = useMutation({
    mutationFn: (data) => placementService.createLog(placementId, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['placements', placementId, 'logs'] });
    },
  });

  const updateLog = useMutation({
    mutationFn: ({ logId, data }) => placementService.updateLog(placementId, logId, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['placements', placementId, 'logs'] });
    },
  });

  const deleteLog = useMutation({
    mutationFn: (logId) => placementService.deleteLog(placementId, logId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['placements', placementId, 'logs'] });
    },
  });

  const uploadAttachment = useMutation({
    mutationFn: ({ logId, file }) => placementService.uploadLogAttachment(placementId, logId, file),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['placements', placementId, 'logs'] });
    },
  });

  return {
    createLog: createLog.mutateAsync,
    isCreating: createLog.isPending,
    updateLog: updateLog.mutateAsync,
    isUpdating: updateLog.isPending,
    deleteLog: deleteLog.mutateAsync,
    isDeleting: deleteLog.isPending,
    uploadAttachment: uploadAttachment.mutateAsync,
    isUploading: uploadAttachment.isPending,
  };
};

export const useReportMutations = (placementId) => {
  const queryClient = useQueryClient();

  const generateReport = useMutation({
    mutationFn: () => placementService.generateReport(placementId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['placements', placementId, 'report'] });
    },
  });

  return {
    generateReport: generateReport.mutateAsync,
    isGenerating: generateReport.isPending,
    generateError: generateReport.error,
  };
};

/**
 * Hook gabungan untuk memantau status laporan dan melakukan mutasi generate
 * @param {string} placementId: ID penempatan
 */
export const useReport = (placementId) => {
  const statusQuery = useReportStatus(placementId);
  const mutations = useReportMutations(placementId);
  return {
    report: statusQuery.data,
    isLoadingReport: statusQuery.isLoading,
    ...mutations,
  };
};
