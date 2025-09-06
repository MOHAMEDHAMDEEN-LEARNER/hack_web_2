import { useQuery } from "@tanstack/react-query";

export function useAuth() {
  const { data: user, isLoading } = useQuery({
    queryKey: ["/api/auth/user"],
    retry: false,
    staleTime: 0, // Allow refetching when invalidated
  });

  return {
    user,
    isLoading,
    isAuthenticated: !!user,
  };
}
