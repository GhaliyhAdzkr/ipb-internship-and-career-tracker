import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { vacancyService } from "../services/vacancyService";
import toast from "react-hot-toast";

export const useVacancies = (params) => {
  return useQuery({
    queryKey: ["vacancies", params],
    queryFn: () => vacancyService.getVacancies(params),
    staleTime: 5 * 60 * 1000, // 5 menit cache
  });
};

export const useJobMatches = (params, enabled = true) => {
  return useQuery({
    queryKey: ["job-matches", params],
    queryFn: () => vacancyService.getJobMatches(params),
    enabled,
    staleTime: 5 * 60 * 1000,
    retry: false,
  });
};

export const useLandingVacancies = () => {
  return useQuery({
    queryKey: ["landing-vacancies"],
    queryFn: async () => {
      const data = await vacancyService.getVacancies({ page: 1, perPage: 3 });
      return { items: data.items || [] };
    },
    staleTime: 5 * 60 * 1000,
  });
};

export const useIndustries = () => {
  return useQuery({
    queryKey: ["industries"],
    queryFn: () => vacancyService.getIndustries(),
    staleTime: 60 * 60 * 1000, // 1 jam cache
  });
};

export const useWishlist = (enabled = true) => {
  return useQuery({
    queryKey: ["wishlist"],
    queryFn: () => vacancyService.getWishlist({ page: 1, perPage: 100 }),
    enabled: enabled,
    staleTime: 5 * 60 * 1000,
  });
};

export const useWishlistMutations = (wishlistMap = new Map()) => {
  const queryClient = useQueryClient();

  const toggleWishlist = useMutation({
    mutationFn: async ({ vacancyId, isWishlisted }) => {
      if (isWishlisted) {
        const wishlistId = wishlistMap.get(vacancyId);
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
    onSuccess: (data, variables) => {
      queryClient.invalidateQueries({ queryKey: ["wishlist"] });
      queryClient.invalidateQueries({ queryKey: ["vacancies"] });
      if (variables.isWishlisted) {
        toast.success("Berhasil dihapus dari wishlist!");
      } else {
        toast.success("Berhasil ditambahkan ke wishlist!");
      }
    },
    onError: (err, variables, context) => {
      if (context?.previousWishlist) {
        queryClient.setQueryData(["wishlist"], context.previousWishlist);
      }
      toast.error(err.response?.data?.detail || "Gagal memperbarui wishlist.");
    },
  });

  const removeWishlist = useMutation({
    mutationFn: (wishlistId) => vacancyService.deleteWishlist(wishlistId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["wishlist"] });
      toast.success("Lowongan dihapus dari wishlist");
    },
    onError: () => {
      toast.error("Gagal menghapus wishlist");
    },
  });

  return {
    toggleWishlist: toggleWishlist.mutate,
    isToggling: toggleWishlist.isPending,
    removeWishlist: removeWishlist.mutate,
    isRemoving: removeWishlist.isPending,
  };
};
