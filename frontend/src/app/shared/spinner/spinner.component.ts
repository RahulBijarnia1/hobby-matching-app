import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-spinner',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './spinner.component.html',
  styleUrl: './spinner.component.css'
})
export class SpinnerComponent {
  @Input() size: 'sm' | 'md' | 'lg' = 'md';
  @Input() color: 'primary' | 'white' | 'gray' = 'primary';
  @Input() fullScreen = false;

  get sizeClasses(): string {
    const sizes = {
      sm: 'w-5 h-5',
      md: 'w-8 h-8',
      lg: 'w-12 h-12'
    };
    return sizes[this.size];
  }

  get colorClasses(): string {
    const colors = {
      primary: 'text-indigo-600',
      white: 'text-white',
      gray: 'text-gray-400'
    };
    return colors[this.color];
  }
}
