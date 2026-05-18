import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import adminService from "../services/adminService";
import vacancyService from "../services/vacancyService";
import toast from "react-hot-toast";

export function useAdminVacancies(onFormSuccess) {
    const queryClient = useQueryClient();

    // Data Fetching
    const vacanciesQuery = useQuery({
        queryKey: ["admin", "vacancies"],
        queryFn: () => vacancyService.getVacancies(1, 200)
    });

    const companiesQuery = useQuery({
        queryKey: ["admin", "companies"],
        queryFn: adminService.getCompanies
    });

    const masterSkillsQuery = useQuery({
        queryKey: ["admin", "skills"],
        queryFn: adminService.getSkills
    });

    const industriesQuery = useQuery({
        queryKey: ["industries"],
        queryFn: () => vacancyService.getIndustries(),
        staleTime: 60 * 60 * 1000,
    });

    // Mutations
    const deleteMutation = useMutation({
        mutationFn: adminService.deleteVacancy,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["admin", "vacancies"] });
            toast.success("Lowongan berhasil dihapus");
        }
    });

    const createSkillMutation = useMutation({
        mutationFn: adminService.createSkill,
        onSuccess: (newSkill) => {
            queryClient.setQueryData(["admin", "skills"], (old) => {
                return [...(old || []), newSkill];
            });
            toast.success(`Keahlian "${newSkill.name}" berhasil ditambahkan secara dinamis!`);
        },
        onError: (err) => {
            console.error("Failed to create skill:", err);
            toast.error(err.response?.data?.detail || "Gagal membuat keahlian baru");
        }
    });

    const createMutation = useMutation({
        mutationFn: adminService.createVacancy,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["admin", "vacancies"] });
            if (onFormSuccess) onFormSuccess();
            toast.success("Lowongan baru berhasil ditambahkan");
        }
    });

    const updateMutation = useMutation({
        mutationFn: ({ id, data }) => adminService.updateVacancy(id, data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["admin", "vacancies"] });
            if (onFormSuccess) onFormSuccess();
            toast.success("Lowongan berhasil diperbarui");
        }
    });

    const scrapeMutation = useMutation({
        mutationFn: async () => {
            return new Promise(resolve => setTimeout(resolve, 2000));
        },
        onSuccess: () => {
            toast.success("Sinkronisasi scraping selesai!");
            queryClient.invalidateQueries({ queryKey: ["admin", "vacancies"] });
        }
    });

    return {
        vacancies: vacanciesQuery.data || [],
        isLoadingVacancies: vacanciesQuery.isLoading,
        companies: companiesQuery.data || [],
        masterSkills: masterSkillsQuery.data || [],
        industries: industriesQuery.data || [],
        
        deleteMutation,
        createSkillMutation,
        createMutation,
        updateMutation,
        scrapeMutation
    };
}
