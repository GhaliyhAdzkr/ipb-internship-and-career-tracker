import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import adminService from "../services/adminService";
import toast from "react-hot-toast";

export function useAdminMasterData(onFormSuccess) {
    const queryClient = useQueryClient();

    // Queries
    const departmentsQuery = useQuery({
        queryKey: ["admin", "departments"],
        queryFn: adminService.getDepartments
    });

    // Mutations
    const deleteDeptMutation = useMutation({
        mutationFn: adminService.deleteDepartment,
        onSuccess: () => {
            queryClient.invalidateQueries(["admin", "departments"]);
            toast.success("Departemen berhasil dihapus");
        }
    });

    const createDeptMutation = useMutation({
        mutationFn: adminService.createDepartment,
        onSuccess: () => {
            queryClient.invalidateQueries(["admin", "departments"]);
            if (onFormSuccess) onFormSuccess();
            toast.success("Departemen baru ditambahkan");
        }
    });

    const updateDeptMutation = useMutation({
        mutationFn: ({ id, data }) => adminService.updateDepartment(id, data),
        onSuccess: () => {
            queryClient.invalidateQueries(["admin", "departments"]);
            if (onFormSuccess) onFormSuccess();
            toast.success("Data departemen diperbarui");
        }
    });

    return {
        departments: departmentsQuery.data || [],
        isLoadingDepartments: departmentsQuery.isLoading,
        
        deleteDepartment: deleteDeptMutation.mutate,
        isDeletingDepartment: deleteDeptMutation.isPending,
        
        createDepartment: createDeptMutation.mutate,
        isCreatingDepartment: createDeptMutation.isPending,
        
        updateDepartment: updateDeptMutation.mutate,
        isUpdatingDepartment: updateDeptMutation.isPending
    };
}
