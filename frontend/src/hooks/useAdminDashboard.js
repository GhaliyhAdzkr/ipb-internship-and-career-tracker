import { useQuery } from "@tanstack/react-query";
import adminService from "../services/adminService";

export function useAdminDashboard() {
    const pendingVerificationsQuery = useQuery({
        queryKey: ["admin", "pending-verifications"],
        queryFn: adminService.getPendingVerifications
    });

    const companiesQuery = useQuery({
        queryKey: ["admin", "companies"],
        queryFn: adminService.getCompanies
    });

    return {
        pendingApplications: pendingVerificationsQuery.data || [],
        loadingApps: pendingVerificationsQuery.isLoading,
        companies: companiesQuery.data || [],
        isLoadingCompanies: companiesQuery.isLoading
    };
}
