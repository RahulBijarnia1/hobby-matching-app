import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { ApiService } from '../../services/api.service';
import { AuthService } from '../../services/auth.service';
import { ToastService } from '../../shared/toast/toast.service';
import { SpinnerComponent } from '../../shared/spinner/spinner.component';
import { UserMatch, PaginatedResponse, MatchQueryParams } from '../../models/models';

@Component({
  selector: 'app-matches',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink, SpinnerComponent],
  templateUrl: './matches.component.html',
  styleUrl: './matches.component.css'
})
export class MatchesComponent implements OnInit {
  private apiService = inject(ApiService);
  private authService = inject(AuthService);
  private toastService = inject(ToastService);

  matches: UserMatch[] = [];
  isLoading = true;
  connectedIds: Set<number> = new Set();
  
  // Pagination
  currentPage = 1;
  pageSize = 12;
  totalMatches = 0;
  totalPages = 0;
  
  // Filters
  minAge = 13;
  maxAge = 100;
  minMatchPercentage = 0;
  showSidebar = false;
  
  // Sort
  sortBy: 'match_percentage' | 'age' | 'name' = 'match_percentage';
  sortOrder: 'asc' | 'desc' = 'desc';

  get hasNextPage(): boolean {
    return this.currentPage < this.totalPages;
  }

  get hasPrevPage(): boolean {
    return this.currentPage > 1;
  }

  get pageNumbers(): number[] {
    const pages: number[] = [];
    const start = Math.max(1, this.currentPage - 2);
    const end = Math.min(this.totalPages, this.currentPage + 2);
    
    for (let i = start; i <= end; i++) {
      pages.push(i);
    }
    return pages;
  }

  ngOnInit(): void {
    this.loadMatches();
  }

  async loadMatches(): Promise<void> {
    if (!this.authService.hasValidToken()) {
      this.toastService.error('Please log in to find matches');
      return;
    }

    this.isLoading = true;
    try {
      const params: MatchQueryParams = {
        page: this.currentPage,
        page_size: this.pageSize,
        min_age: this.minAge,
        max_age: this.maxAge,
        min_match_percentage: this.minMatchPercentage
      };

      const response = await this.apiService.getMatches(params).toPromise();

      if (response) {
        const paginatedResponse = response as PaginatedResponse<UserMatch>;
        this.matches = paginatedResponse.items;
        this.totalMatches = paginatedResponse.total;
        this.totalPages = paginatedResponse.total_pages || Math.ceil(paginatedResponse.total / this.pageSize);
        this.currentPage = paginatedResponse.page;
      }
    } catch (error) {
      this.toastService.error('Failed to load matches');
      console.error(error);
    } finally {
      this.isLoading = false;
    }
  }

  applyFilters(): void {
    this.currentPage = 1;
    this.loadMatches();
    this.showSidebar = false;
  }

  resetFilters(): void {
    this.minAge = 13;
    this.maxAge = 100;
    this.minMatchPercentage = 0;
    this.applyFilters();
  }

  goToPage(page: number): void {
    if (page >= 1 && page <= this.totalPages) {
      this.currentPage = page;
      this.loadMatches();
    }
  }

  nextPage(): void {
    if (this.hasNextPage) {
      this.currentPage++;
      this.loadMatches();
    }
  }

  prevPage(): void {
    if (this.hasPrevPage) {
      this.currentPage--;
      this.loadMatches();
    }
  }

  sortMatches(field: 'match_percentage' | 'age' | 'name'): void {
    if (this.sortBy === field) {
      this.sortOrder = this.sortOrder === 'asc' ? 'desc' : 'asc';
    } else {
      this.sortBy = field;
      this.sortOrder = field === 'match_percentage' ? 'desc' : 'asc';
    }
    
    this.matches.sort((a, b) => {
      let comparison = 0;
      if (field === 'match_percentage') {
        comparison = a.match_percentage - b.match_percentage;
      } else if (field === 'age') {
        comparison = a.age - b.age;
      } else {
        comparison = a.name.localeCompare(b.name);
      }
      return this.sortOrder === 'asc' ? comparison : -comparison;
    });
  }

  getMatchColor(percentage: number): string {
    if (percentage >= 80) return 'text-green-600 dark:text-green-400';
    if (percentage >= 60) return 'text-indigo-600 dark:text-indigo-400';
    if (percentage >= 40) return 'text-yellow-600 dark:text-yellow-400';
    return 'text-gray-600 dark:text-gray-400';
  }

  getMatchBgColor(percentage: number): string {
    if (percentage >= 80) return 'bg-green-100 dark:bg-green-900/30';
    if (percentage >= 60) return 'bg-indigo-100 dark:bg-indigo-900/30';
    if (percentage >= 40) return 'bg-yellow-100 dark:bg-yellow-900/30';
    return 'bg-gray-100 dark:bg-gray-700';
  }

  getProgressBarColor(percentage: number): string {
    if (percentage >= 80) return 'bg-gradient-to-r from-green-400 to-green-600';
    if (percentage >= 60) return 'bg-gradient-to-r from-indigo-400 to-indigo-600';
    if (percentage >= 40) return 'bg-gradient-to-r from-yellow-400 to-yellow-600';
    return 'bg-gradient-to-r from-gray-400 to-gray-600';
  }

  toggleSidebar(): void {
    this.showSidebar = !this.showSidebar;
  }

  connectWith(match: UserMatch): void {
    this.connectedIds.add(match.id);
    this.toastService.success(`Connected with ${match.name}! Their email is shown below.`);
  }

  isConnected(matchId: number): boolean {
    return this.connectedIds.has(matchId);
  }
}
