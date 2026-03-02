import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, FormArray, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { ApiService } from '../../services/api.service';
import { Hobby } from '../../models/models';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent implements OnInit {
  private fb = inject(FormBuilder);
  private apiService = inject(ApiService);
  private router = inject(Router);

  userForm!: FormGroup;
  hobbies: Hobby[] = [];
  loading = false;
  loadingHobbies = true;
  submitting = false;
  errorMessage = '';
  successMessage = '';

  ngOnInit(): void {
    this.initForm();
    this.loadHobbies();
  }

  private initForm(): void {
    this.userForm = this.fb.group({
      name: ['', [Validators.required, Validators.minLength(1), Validators.maxLength(100)]],
      age: ['', [Validators.required, Validators.min(1), Validators.max(150)]],
      email: ['', [Validators.required, Validators.email]],
      hobbies: this.fb.array([], [Validators.required, Validators.minLength(1)])
    });
  }

  private loadHobbies(): void {
    this.loadingHobbies = true;
    this.apiService.getHobbies().subscribe({
      next: (hobbies) => {
        this.hobbies = hobbies;
        this.initHobbiesArray();
        this.loadingHobbies = false;
      },
      error: (error) => {
        this.errorMessage = 'Failed to load hobbies. Please refresh the page.';
        this.loadingHobbies = false;
      }
    });
  }

  private initHobbiesArray(): void {
    const hobbiesArray = this.userForm.get('hobbies') as FormArray;
    this.hobbies.forEach(() => hobbiesArray.push(this.fb.control(false)));
  }

  get hobbiesArray(): FormArray {
    return this.userForm.get('hobbies') as FormArray;
  }

  get selectedHobbiesCount(): number {
    return this.hobbiesArray.controls.filter(control => control.value).length;
  }

  get isHobbySelectionValid(): boolean {
    return this.selectedHobbiesCount > 0;
  }

  getSelectedHobbyIds(): number[] {
    return this.hobbies
      .filter((_, index) => this.hobbiesArray.at(index).value)
      .map(hobby => hobby.id);
  }

  onSubmit(): void {
    if (this.userForm.invalid || !this.isHobbySelectionValid) {
      this.markFormGroupTouched(this.userForm);
      if (!this.isHobbySelectionValid) {
        this.errorMessage = 'Please select at least one hobby.';
      }
      return;
    }

    this.submitting = true;
    this.errorMessage = '';
    this.successMessage = '';

    const userData = {
      name: this.userForm.get('name')!.value.trim(),
      age: this.userForm.get('age')!.value,
      email: this.userForm.get('email')!.value.trim().toLowerCase(),
      hobby_ids: this.getSelectedHobbyIds()
    };

    this.apiService.createUser(userData).subscribe({
      next: (user) => {
        this.successMessage = `Welcome, ${user.name}! Your profile has been created successfully.`;
        this.submitting = false;
        
        // Store user ID for matches page
        localStorage.setItem('currentUserId', user.id.toString());
        localStorage.setItem('currentUserName', user.name);
        
        // Reset form
        this.userForm.reset();
        this.hobbiesArray.controls.forEach(control => control.setValue(false));
        
        // Navigate to matches after 2 seconds
        setTimeout(() => {
          this.router.navigate(['/matches']);
        }, 2000);
      },
      error: (error) => {
        this.errorMessage = error.message || 'Failed to create user. Please try again.';
        this.submitting = false;
      }
    });
  }

  private markFormGroupTouched(formGroup: FormGroup): void {
    Object.values(formGroup.controls).forEach(control => {
      control.markAsTouched();
      if (control instanceof FormGroup) {
        this.markFormGroupTouched(control);
      }
    });
  }

  // Form validation helpers
  isFieldInvalid(fieldName: string): boolean {
    const field = this.userForm.get(fieldName);
    return field ? field.invalid && field.touched : false;
  }

  getFieldError(fieldName: string): string {
    const field = this.userForm.get(fieldName);
    if (!field || !field.errors || !field.touched) return '';

    if (field.errors['required']) return `${this.capitalizeFirst(fieldName)} is required`;
    if (field.errors['email']) return 'Please enter a valid email address';
    if (field.errors['min']) return `${this.capitalizeFirst(fieldName)} must be at least ${field.errors['min'].min}`;
    if (field.errors['max']) return `${this.capitalizeFirst(fieldName)} cannot exceed ${field.errors['max'].max}`;
    if (field.errors['minlength']) return `${this.capitalizeFirst(fieldName)} must be at least ${field.errors['minlength'].requiredLength} characters`;
    if (field.errors['maxlength']) return `${this.capitalizeFirst(fieldName)} cannot exceed ${field.errors['maxlength'].requiredLength} characters`;
    
    return '';
  }

  private capitalizeFirst(str: string): string {
    return str.charAt(0).toUpperCase() + str.slice(1);
  }
}
