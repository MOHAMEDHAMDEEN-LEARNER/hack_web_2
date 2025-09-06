import { QueryClient, QueryFunction } from "@tanstack/react-query";

async function throwIfResNotOk(res: Response) {
  if (!res.ok) {
    let errorData;
    let errorMessage = res.statusText;
    
    try {
      // Clone the response so we can read it multiple ways if needed
      const responseClone = res.clone();
      const text = await responseClone.text();
      
      // Try to parse as JSON first
      try {
        errorData = JSON.parse(text);
        errorMessage = errorData.message || res.statusText;
      } catch {
        // If not JSON, use the text as the error message
        errorMessage = text || res.statusText;
      }
    } catch {
      // If all fails, use status text
      errorMessage = res.statusText;
    }
    
    const error = new Error(errorMessage);
    (error as any).fieldErrors = errorData?.fieldErrors;
    (error as any).status = res.status;
    throw error;
  }
}

export async function apiRequest(
  url: string,
  options?: {
    method?: string;
    body?: string;
    headers?: Record<string, string>;
  }
): Promise<any> {
  const method = options?.method || 'GET';
  const headers = {
    'Content-Type': 'application/json',
    ...options?.headers,
  };

  const res = await fetch(url, {
    method,
    headers,
    body: options?.body,
    credentials: "include",
  });

  await throwIfResNotOk(res);
  return await res.json();
}

type UnauthorizedBehavior = "returnNull" | "throw";
export const getQueryFn: <T>(options: {
  on401: UnauthorizedBehavior;
}) => QueryFunction<T> =
  ({ on401: unauthorizedBehavior }) =>
  async ({ queryKey }) => {
    const res = await fetch(queryKey.join("/") as string, {
      credentials: "include",
    });

    if (unauthorizedBehavior === "returnNull" && res.status === 401) {
      return null;
    }

    await throwIfResNotOk(res);
    return await res.json();
  };

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      queryFn: getQueryFn({ on401: "throw" }),
      refetchInterval: false,
      refetchOnWindowFocus: false,
      staleTime: Infinity,
      retry: false,
    },
    mutations: {
      retry: false,
    },
  },
});
