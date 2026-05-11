import React from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import vacancyService from '../services/vacancyService';
import { PiTrash } from 'react-icons/pi';

export default function Wishlist() {
  const queryClient = useQueryClient();

  const { data, isLoading, isError } = useQuery({
    queryKey: ['wishlist'],
    queryFn: () => vacancyService.getWishlist({ page: 1, perPage: 50 }),
  });

  const deleteMutation = useMutation({
    mutationFn: (id) => vacancyService.deleteWishlist(id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['wishlist'] }),
  });

  if (isLoading) return <div>Memuat wishlist...</div>;
  if (isError) return <div>Gagal memuat wishlist.</div>;

  const items = data?.items || [];

  return (
    <div className="font-jakarta">
      <div className="mb-6 flex items-center justify-between">
        <h2 className="text-xl font-bold">Wishlist Saya</h2>
      </div>

      {items.length === 0 ? (
        <div className="p-8 bg-white rounded-xl">Belum ada wishlist.</div>
      ) : (
        <div className="grid grid-cols-1 gap-4">
          {items.map((w) => (
            <div key={w.id} className="p-4 bg-white rounded-xl flex items-center justify-between">
              <div>
                <div className="font-bold">{w.vacancy.title}</div>
                <div className="text-sm text-zinc-500">{w.vacancy.company?.name || '-'}</div>
              </div>
              <div className="flex items-center gap-2">
                <button onClick={() => deleteMutation.mutate(w.id)} className="text-red-600 hover:text-red-800">
                  <PiTrash size={18} />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
