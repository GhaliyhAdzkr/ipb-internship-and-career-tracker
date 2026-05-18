import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { notificationService } from '../services/notificationService';

export const useNotifications = () => {
  const queryClient = useQueryClient();

  const { data: notifications, isLoading } = useQuery({
    queryKey: ['notifications'],
    queryFn: notificationService.getNotifications,
    refetchInterval: 1000 * 60, // Ambil ulang data setiap menit
  });

  const { data: unreadCount } = useQuery({
    queryKey: ['notifications', 'unread-count'],
    queryFn: notificationService.getUnreadCount,
    refetchInterval: 1000 * 30, // Ambil ulang data setiap 30 detik
  });

  const markAsReadMutation = useMutation({
    mutationFn: notificationService.markAsRead,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['notifications'] });
    },
  });

  const deleteMutation = useMutation({
    mutationFn: notificationService.deleteNotification,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['notifications'] });
    },
  });

  return {
    notifications: Array.isArray(notifications) ? notifications : (notifications?.notifications || []),
    unreadCount: unreadCount?.unread_count ?? unreadCount?.count ?? 0,
    isLoading,
    markAsRead: markAsReadMutation.mutate,
    deleteNotification: deleteMutation.mutate,
  };
};
