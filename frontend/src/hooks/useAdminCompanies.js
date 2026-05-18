import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import adminService from "../services/adminService";
import toast from "react-hot-toast";

export function useAdminCompanies(onFormSuccess) {
    const queryClient = useQueryClient();

    const companiesQuery = useQuery({
        queryKey: ["admin", "companies"],
        queryFn: adminService.getCompanies
    });

    const deleteMutation = useMutation({
        mutationFn: adminService.deleteCompany,
        onSuccess: () => {
            queryClient.invalidateQueries(["admin", "companies"]);
            toast.success("Perusahaan berhasil dihapus");
        }
    });

    const createMutation = useMutation({
        mutationFn: adminService.createCompany,
        onSuccess: () => {
            queryClient.invalidateQueries(["admin", "companies"]);
            if (onFormSuccess) onFormSuccess();
            toast.success("Perusahaan baru ditambahkan");
        }
    });

    const updateMutation = useMutation({
        mutationFn: ({ id, data }) => adminService.updateCompany(id, data),
        onSuccess: () => {
            queryClient.invalidateQueries(["admin", "companies"]);
            if (onFormSuccess) onFormSuccess();
            toast.success("Data perusahaan diperbarui");
        }
    });

    return {
        companies: companiesQuery.data || [],
        isLoadingCompanies: companiesQuery.isLoading,
        deleteMutation,
        createMutation,
        updateMutation
    };
}
