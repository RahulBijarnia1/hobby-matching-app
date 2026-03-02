/**
 * Hobby interface representing a hobby entity
 */
export interface Hobby {
  id: number;
  name: string;
  category: string | null;
}

/**
 * User interface representing a user entity
 */
export interface User {
  id: number;
  name: string;
  age: number;
  email: string;
  bio: string | null;
  created_at: string;
  hobbies: Hobby[];
}

/**
 * Request payload for user registration
 */
export interface RegisterRequest {
  name: string;
  age: number;
  email: string;
  password: string;
  bio?: string;
}

/**
 * Request payload for user login
 */
export interface LoginRequest {
  email: string;
  password: string;
}

/**
 * Authentication response with token
 */
export interface AuthResponse {
  id: number;
  name: string;
  email: string;
  access_token: string;
  token_type: string;
}

/**
 * Request payload for updating user profile
 */
export interface UpdateProfileRequest {
  name?: string;
  age?: number;
  bio?: string;
  hobby_ids?: number[];
}

/**
 * User match response with match percentage
 */
export interface UserMatch {
  id: number;
  name: string;
  age: number;
  email: string;
  bio: string | null;
  match_percentage: number;
  common_hobbies: Hobby[];
}

/**
 * Paginated response structure
 */
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  pages: number;
  page_size: number;
  total_pages?: number;
  has_next: boolean;
  has_prev: boolean;
}

/**
 * Query parameters for filtering matches
 */
export interface MatchQueryParams {
  min_age?: number;
  max_age?: number;
  min_match_percentage?: number;
  page?: number;
  limit?: number;
  page_size?: number;
}

/**
 * User update request
 */
export interface UserUpdate {
  name?: string;
  age?: number;
  bio?: string;
}

/**
 * API error response structure
 */
export interface ApiError {
  detail: string;
}

/**
 * Toast notification type
 */
export type ToastType = 'success' | 'error' | 'warning' | 'info';

/**
 * Toast notification interface
 */
export interface Toast {
  id: number;
  message: string;
  type: ToastType;
  duration?: number;
}
