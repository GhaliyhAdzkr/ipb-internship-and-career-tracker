import { useQuery } from '@tanstack/react-query';
import adminService from '../services/adminService';

export function useAdminPlacements() {
  const placementsQuery = useQuery({
    queryKey: ['admin', 'placements'],
    queryFn: adminService.getPlacements,
  });

  return {
    placements: placementsQuery.data || [],
    isLoadingPlacements: placementsQuery.isLoading,
    isErrorPlacements: placementsQuery.isError,
    placementsQuery
  };
}
