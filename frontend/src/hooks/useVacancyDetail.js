import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { vacancyService } from "../services/vacancyService";
import toast from "react-hot-toast";

export function useVacancyDetail(vacancyId, token) {
    const queryClient = useQueryClient();

    const vacancyQuery = useQuery({
        queryKey: ["vacancy", vacancyId],
        queryFn: () => vacancyService.getVacancy(vacancyId),
        enabled: !!vacancyId,
    });

    const wishlistQuery = useQuery({
        queryKey: ["wishlist"],
        queryFn: () => vacancyService.getWishlist({ page: 1, perPage: 100 }),
        enabled: !!token,
    });

    const isWishlisted = wishlistQuery.data?.items?.some(w => w.vacancy.id === vacancyId) || false;
    const wishlistId = wishlistQuery.data?.items?.find(w => w.vacancy.id === vacancyId)?.id;

    const toggleWishlistMutation = useMutation({
        mutationFn: async () => {
            if (isWishlisted) {
                if (wishlistId) {
                    return await vacancyService.deleteWishlist(wishlistId);
                }
            } else {
                return await vacancyService.addToWishlist(vacancyId);
            }
        },
        onMutate: async () => {
            await queryClient.cancelQueries({ queryKey: ["wishlist"] });
            const previousWishlist = queryClient.getQueryData(["wishlist"]);
            return { previousWishlist };
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["vacancy", vacancyId] });
            queryClient.invalidateQueries({ queryKey: ["wishlist"] });
            if (isWishlisted) {
                toast.success("Berhasil dihapus dari wishlist!");
            } else {
                toast.success("Lowongan berhasil disimpan ke wishlist!");
            }
        },
        onError: (error, variables, context) => {
            if (context?.previousWishlist) {
                queryClient.setQueryData(["wishlist"], context.previousWishlist);
            }
            toast.error(error.response?.data?.detail || "Gagal memperbarui wishlist.");
        },
    });

    return {
        vacancy: vacancyQuery.data,
        isLoadingVacancy: vacancyQuery.isLoading,
        isErrorVacancy: vacancyQuery.isError,
        vacancyQuery,
        
        wishlistData: wishlistQuery.data,
        isWishlisted,
        wishlistId,
        toggleWishlistMutation
    };
}
