import { Injectable, inject, signal, computed } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { Observable, tap, catchError, throwError, BehaviorSubject } from 'rxjs';
import { environment } from '../../environments/environment';
import {
  User,
  RegisterRequest,
  LoginRequest,
  AuthResponse
} from '../models/models';

const TOKEN_KEY = 'hobby_connect_token';
const USER_KEY = 'hobby_connect_user';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private readonly apiUrl = environment.apiUrl;
  private http = inject(HttpClient);
  private router = inject(Router);

  private currentUserSubject = new BehaviorSubject<User | null>(this.getStoredUser());
  currentUser$ = this.currentUserSubject.asObservable();

  private isAuthenticatedSignal = signal<boolean>(this.hasValidToken());
  isAuthenticated = computed(() => this.isAuthenticatedSignal());

  constructor() {
    // Check token validity on service initialization
    if (this.hasValidToken()) {
      this.loadCurrentUser();
    }
  }

  /**
   * Register a new user
   */
  register(userData: RegisterRequest): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(`${this.apiUrl}/auth/register`, userData)
      .pipe(
        tap((response: AuthResponse) => this.handleAuthResponse(response)),
        catchError(this.handleError)
      );
  }

  /**
   * Login user
   */
  login(credentials: LoginRequest): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(`${this.apiUrl}/auth/login`, credentials)
      .pipe(
        tap((response: AuthResponse) => this.handleAuthResponse(response)),
        catchError(this.handleError)
      );
  }

  /**
   * Logout user
   */
  logout(): void {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
    this.currentUserSubject.next(null);
    this.isAuthenticatedSignal.set(false);
    this.router.navigate(['/']);
  }

  /**
   * Get current user profile
   */
  getCurrentUser(): Observable<User> {
    return this.http.get<User>(`${this.apiUrl}/auth/me`)
      .pipe(
        tap((user: User) => {
          this.storeUser(user);
          this.currentUserSubject.next(user);
        }),
        catchError(this.handleError)
      );
  }

  /**
   * Refresh token
   */
  refreshToken(): Observable<{ access_token: string; token_type: string }> {
    return this.http.post<{ access_token: string; token_type: string }>(
      `${this.apiUrl}/auth/refresh`,
      {}
    ).pipe(
      tap((response: { access_token: string; token_type: string }) => {
        this.storeToken(response.access_token);
      }),
      catchError(this.handleError)
    );
  }

  /**
   * Get stored token
   */
  getToken(): string | null {
    return localStorage.getItem(TOKEN_KEY);
  }

  /**
   * Check if user is authenticated
   */
  hasValidToken(): boolean {
    const token = this.getToken();
    if (!token) return false;

    // Check if token is expired (basic check)
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      const expiry = payload.exp * 1000;
      return Date.now() < expiry;
    } catch {
      return false;
    }
  }

  /**
   * Get current user value
   */
  getCurrentUserValue(): User | null {
    return this.currentUserSubject.value;
  }

  /**
   * Update current user in state
   */
  updateCurrentUser(user: User): void {
    this.storeUser(user);
    this.currentUserSubject.next(user);
  }

  private handleAuthResponse(response: AuthResponse): void {
    this.storeToken(response.access_token);
    this.isAuthenticatedSignal.set(true);
    this.loadCurrentUser();
  }

  private storeToken(token: string): void {
    localStorage.setItem(TOKEN_KEY, token);
  }

  private storeUser(user: User): void {
    localStorage.setItem(USER_KEY, JSON.stringify(user));
  }

  private getStoredUser(): User | null {
    const userStr = localStorage.getItem(USER_KEY);
    if (userStr) {
      try {
        return JSON.parse(userStr);
      } catch {
        return null;
      }
    }
    return null;
  }

  private loadCurrentUser(): void {
    this.getCurrentUser().subscribe({
      error: () => this.logout()
    });
  }

  private handleError(error: any): Observable<never> {
    let errorMessage = 'An unknown error occurred';

    if (error.error?.detail) {
      errorMessage = error.error.detail;
    } else if (error.message) {
      errorMessage = error.message;
    }

    return throwError(() => new Error(errorMessage));
  }
}
