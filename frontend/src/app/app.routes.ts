import { Routes } from '@angular/router';
import { authGuard, guestGuard } from './guards/auth.guard';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () => import('./pages/landing/landing.component').then(m => m.LandingComponent),
    title: 'Welcome - Hobby Connect'
  },
  {
    path: 'login',
    loadComponent: () => import('./pages/login/login.component').then(m => m.LoginComponent),
    canActivate: [guestGuard],
    title: 'Login - Hobby Connect'
  },
  {
    path: 'register',
    loadComponent: () => import('./pages/register/register.component').then(m => m.RegisterComponent),
    canActivate: [guestGuard],
    title: 'Register - Hobby Connect'
  },
  {
    path: 'dashboard',
    loadComponent: () => import('./pages/dashboard/dashboard.component').then(m => m.DashboardComponent),
    canActivate: [authGuard],
    title: 'Dashboard - Hobby Connect'
  },
  {
    path: 'matches',
    loadComponent: () => import('./pages/matches/matches.component').then(m => m.MatchesComponent),
    canActivate: [authGuard],
    title: 'Find Matches - Hobby Connect'
  },
  {
    path: '**',
    redirectTo: ''
  }
];
