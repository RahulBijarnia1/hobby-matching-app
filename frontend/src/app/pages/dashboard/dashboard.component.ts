import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { ApiService } from '../../services/api.service';
import { ToastService } from '../../shared/toast/toast.service';
import { SpinnerComponent } from '../../shared/spinner/spinner.component';
import { User, Hobby, UpdateProfileRequest } from '../../models/models';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, FormsModule, SpinnerComponent],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css'
})
export class DashboardComponent implements OnInit {
  private authService = inject(AuthService);
  private apiService = inject(ApiService);
  private toastService = inject(ToastService);
  private router = inject(Router);

  user: User | null = null;
  allHobbies: Hobby[] = [];
  selectedHobbyIds: Set<number> = new Set();
  categories: string[] = [];
  selectedCategory = '';
  
  isLoading = true;
  isSaving = false;
  showEditModal = false;
  
  editForm: UpdateProfileRequest = {
    name: '',
    age: 0,
    bio: ''
  };

  // Group hobbies by category
  get groupedHobbies(): { [key: string]: Hobby[] } {
    const filtered = this.selectedCategory 
      ? this.allHobbies.filter(h => h.category === this.selectedCategory)
      : this.allHobbies;
    
    return filtered.reduce((groups, hobby) => {
      const category = hobby.category || 'Other';
      if (!groups[category]) {
        groups[category] = [];
      }
      groups[category].push(hobby);
      return groups;
    }, {} as { [key: string]: Hobby[] });
  }

  get selectedHobbies(): Hobby[] {
    return this.allHobbies.filter(h => this.selectedHobbyIds.has(h.id));
  }

  ngOnInit(): void {
    this.loadData();
  }

  async loadData(): Promise<void> {
    this.isLoading = true;
    try {
      // Load current user
      const userResponse = await this.authService.getCurrentUser().toPromise();
      this.user = userResponse!;
      
      // Initialize selected hobbies
      if (this.user?.hobbies) {
        this.selectedHobbyIds = new Set(this.user.hobbies.map(h => h.id));
      }
      
      // Initialize edit form
      this.editForm = {
        name: this.user?.name || '',
        age: this.user?.age || 0,
        bio: this.user?.bio || ''
      };
      
      // Load all hobbies
      const hobbiesResponse = await this.apiService.getHobbies().toPromise();
      this.allHobbies = hobbiesResponse!;
      
      // Extract categories
      this.categories = [...new Set(this.allHobbies.map(h => h.category).filter(Boolean))] as string[];
    } catch (error) {
      this.toastService.error('Failed to load data');
      console.error(error);
    } finally {
      this.isLoading = false;
    }
  }

  toggleHobby(hobby: Hobby): void {
    if (this.selectedHobbyIds.has(hobby.id)) {
      this.selectedHobbyIds.delete(hobby.id);
    } else {
      this.selectedHobbyIds.add(hobby.id);
    }
  }

  isHobbySelected(hobby: Hobby): boolean {
    return this.selectedHobbyIds.has(hobby.id);
  }

  async saveHobbies(): Promise<void> {
    if (!this.user) return;
    
    this.isSaving = true;
    try {
      await this.apiService.updateProfileWithHobbies({ hobby_ids: Array.from(this.selectedHobbyIds) }).toPromise();
      this.toastService.success('Hobbies updated successfully');
      await this.loadData();
    } catch (error) {
      this.toastService.error('Failed to update hobbies');
      console.error(error);
    } finally {
      this.isSaving = false;
    }
  }

  openEditModal(): void {
    this.editForm = {
      name: this.user?.name || '',
      age: this.user?.age || 0,
      bio: this.user?.bio || ''
    };
    this.showEditModal = true;
  }

  closeEditModal(): void {
    this.showEditModal = false;
  }

  async saveProfile(): Promise<void> {
    if (!this.user) return;
    
    this.isSaving = true;
    try {
      await this.apiService.updateProfile(this.editForm).toPromise();
      this.toastService.success('Profile updated successfully');
      this.showEditModal = false;
      await this.loadData();
    } catch (error) {
      this.toastService.error('Failed to update profile');
      console.error(error);
    } finally {
      this.isSaving = false;
    }
  }

  filterByCategory(category: string): void {
    this.selectedCategory = this.selectedCategory === category ? '' : category;
  }

  navigateToMatches(): void {
    this.router.navigate(['/matches']);
  }
}
