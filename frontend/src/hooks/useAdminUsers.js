import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import adminService from "../services/adminService";
import toast from "react-hot-toast";

export function useAdminUsers() {
    const queryClient = useQueryClient();

    const studentsQuery = useQuery({
        queryKey: ["admin", "students"],
        queryFn: adminService.getStudents
    });

    const departmentsQuery = useQuery({
        queryKey: ["admin", "departments"],
        queryFn: adminService.getDepartments
    });

    const toggleActiveMutation = useMutation({
        mutationFn: adminService.toggleUserActive,
        onSuccess: () => {
            queryClient.invalidateQueries(["admin", "students"]);
            toast.success("Status akun berhasil diperbarui");
        }
    });

    return {
        students: studentsQuery.data || [],
        isLoadingStudents: studentsQuery.isLoading,
        departments: departmentsQuery.data || [],
        isLoadingDepartments: departmentsQuery.isLoading,
        toggleActiveMutation
    };
}
