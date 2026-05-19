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

    const studentsQuery = useQuery({
        queryKey: ["admin", "students"],
        queryFn: adminService.getStudents
    });

    const vacancyStatsQuery = useQuery({
        queryKey: ["admin", "vacancy-stats"],
        queryFn: adminService.getVacancyStats
    });

    return {
        pendingApplications: pendingVerificationsQuery.data || [],
        loadingApps: pendingVerificationsQuery.isLoading,
        companies: companiesQuery.data || [],
        isLoadingCompanies: companiesQuery.isLoading,
        students: studentsQuery.data || [],
        isLoadingStudents: studentsQuery.isLoading,
        vacancyStats: vacancyStatsQuery.data,
        isLoadingVacancyStats: vacancyStatsQuery.isLoading
    };
}
