import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { environment } from '../../environments/environment';
import {
  Hobby,
  User,
  UserMatch,
  MatchQueryParams,
  UpdateProfileRequest,
  PaginatedResponse,
  UserUpdate
} from '../models/models';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private readonly apiUrl = environment.apiUrl;
  private http = inject(HttpClient);

  // ==================== Hobbies ====================

  /**
   * Get all available hobbies
   */
  getHobbies(category?: string): Observable<Hobby[]> {
    let params = new HttpParams();
    if (category) {
      params = params.set('category', category);
    }
    return this.http.get<Hobby[]>(`${this.apiUrl}/hobbies`, { params })
      .pipe(catchError(this.handleError));
  }

  /**
   * Get all hobby categories
   */
  getHobbyCategories(): Observable<string[]> {
    return this.http.get<string[]>(`${this.apiUrl}/hobbies/categories`)
      .pipe(catchError(this.handleError));
  }

  /**
   * Get a specific hobby by ID
   */
  getHobby(id: number): Observable<Hobby> {
    return this.http.get<Hobby>(`${this.apiUrl}/hobbies/${id}`)
      .pipe(catchError(this.handleError));
  }

  // ==================== Users ====================

  /**
   * Get current user profile (protected)
   */
  getProfile(): Observable<User> {
    return this.http.get<User>(`${this.apiUrl}/users/profile`)
      .pipe(catchError(this.handleError));
  }

  /**
   * Update current user profile (protected)
   */
  updateProfile(data: UpdateProfileRequest): Observable<User> {
    return this.http.put<User>(`${this.apiUrl}/users/profile`, data)
      .pipe(catchError(this.handleError));
  }

  /**
   * Add hobbies to current user (protected)
   */
  addHobbies(hobbyIds: number[]): Observable<User> {
    return this.http.post<User>(`${this.apiUrl}/users/profile/hobbies`, hobbyIds)
      .pipe(catchError(this.handleError));
  }

  /**
   * Remove hobbies from current user (protected)
   */
  removeHobbies(hobbyIds: number[]): Observable<User> {
    return this.http.delete<User>(`${this.apiUrl}/users/profile/hobbies`, {
      body: hobbyIds
    }).pipe(catchError(this.handleError));
  }

  /**
   * Get all users
   */
  getUsers(): Observable<User[]> {
    return this.http.get<User[]>(`${this.apiUrl}/users`)
      .pipe(catchError(this.handleError));
  }

  /**
   * Get a specific user by ID
   */
  getUser(id: number): Observable<User> {
    return this.http.get<User>(`${this.apiUrl}/users/${id}`)
      .pipe(catchError(this.handleError));
  }

  /**
   * Update user profile with hobbies
   */
  updateProfileWithHobbies(data: UpdateProfileRequest): Observable<User> {
    return this.http.put<User>(`${this.apiUrl}/users/profile`, data)
      .pipe(catchError(this.handleError));
  }

  /**
   * Delete current user account
   */
  deleteAccount(): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/users/account`)
      .pipe(catchError(this.handleError));
  }

  // ==================== Matches ====================

  /**
   * Get matches for current user (protected)
   */
  getMatches(params?: MatchQueryParams): Observable<PaginatedResponse<UserMatch>> {
    let httpParams = new HttpParams();

    if (params?.min_age) {
      httpParams = httpParams.set('min_age', params.min_age.toString());
    }
    if (params?.max_age) {
      httpParams = httpParams.set('max_age', params.max_age.toString());
    }
    if (params?.min_match_percentage) {
      httpParams = httpParams.set('min_match_percentage', params.min_match_percentage.toString());
    }
    if (params?.page) {
      httpParams = httpParams.set('page', params.page.toString());
    }
    if (params?.page_size) {
      httpParams = httpParams.set('page_size', params.page_size.toString());
    }

    return this.http.get<PaginatedResponse<UserMatch>>(
      `${this.apiUrl}/users/matches`,
      { params: httpParams }
    ).pipe(catchError(this.handleError));
  }

  // ==================== Error Handler ====================

  /**
   * Handle HTTP errors
   */
  private handleError(error: HttpErrorResponse): Observable<never> {
    let errorMessage = 'An unknown error occurred';

    if (error.error instanceof ErrorEvent) {
      // Client-side error
      errorMessage = error.error.message;
    } else {
      // Server-side error
      if (error.error?.detail) {
        errorMessage = error.error.detail;
      } else if (error.status === 0) {
        errorMessage = 'Unable to connect to server. Please check your connection.';
      } else if (error.status === 401) {
        errorMessage = 'Unauthorized. Please login again.';
      } else if (error.status === 403) {
        errorMessage = 'Access denied.';
      } else if (error.status === 404) {
        errorMessage = 'Resource not found.';
      } else {
        errorMessage = `Server error: ${error.status}`;
      }
    }

    console.error('API Error:', errorMessage);
    return throwError(() => new Error(errorMessage));
  }
}
