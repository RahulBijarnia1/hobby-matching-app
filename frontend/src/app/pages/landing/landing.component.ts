import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-landing',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './landing.component.html',
  styleUrl: './landing.component.css'
})
export class LandingComponent {
  currentYear = new Date().getFullYear();
  
  features = [
    {
      icon: 'M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z',
      title: 'Smart Matching',
      description: 'Our advanced algorithm connects you with people who share your passions and interests.'
    },
    {
      icon: 'M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z',
      title: 'Real Connections',
      description: 'Meet genuine people who enjoy the same hobbies and activities as you do.'
    },
    {
      icon: 'M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z',
      title: 'Discover New Hobbies',
      description: 'Explore new interests through connections with people who can introduce you to their world.'
    },
    {
      icon: 'M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z',
      title: 'Safe & Secure',
      description: 'Your data is protected with industry-standard security measures and encryption.'
    }
  ];

  steps = [
    {
      number: '01',
      title: 'Create Your Profile',
      description: 'Sign up and tell us about yourself and your interests.'
    },
    {
      number: '02',
      title: 'Select Your Hobbies',
      description: 'Choose from our extensive list of hobbies and activities.'
    },
    {
      number: '03',
      title: 'Find Your Matches',
      description: 'Discover people who share your passions and connect with them.'
    }
  ];
}
