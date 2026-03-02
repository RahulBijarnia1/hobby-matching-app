import { Injectable, signal, computed } from '@angular/core';
import { Toast, ToastType } from '../../models/models';

@Injectable({
  providedIn: 'root'
})
export class ToastService {
  private toastsSignal = signal<Toast[]>([]);
  private idCounter = 0;

  toasts = computed(() => this.toastsSignal());

  /**
   * Show a toast notification
   */
  show(message: string, type: ToastType = 'info', duration: number = 5000): void {
    const toast: Toast = {
      id: ++this.idCounter,
      message,
      type,
      duration
    };

    this.toastsSignal.update(toasts => [...toasts, toast]);

    if (duration > 0) {
      setTimeout(() => this.remove(toast.id), duration);
    }
  }

  /**
   * Show a success toast
   */
  success(message: string, duration?: number): void {
    this.show(message, 'success', duration);
  }

  /**
   * Show an error toast
   */
  error(message: string, duration?: number): void {
    this.show(message, 'error', duration);
  }

  /**
   * Show a warning toast
   */
  warning(message: string, duration?: number): void {
    this.show(message, 'warning', duration);
  }

  /**
   * Show an info toast
   */
  info(message: string, duration?: number): void {
    this.show(message, 'info', duration);
  }

  /**
   * Remove a toast by ID
   */
  remove(id: number): void {
    this.toastsSignal.update(toasts => toasts.filter(t => t.id !== id));
  }

  /**
   * Clear all toasts
   */
  clear(): void {
    this.toastsSignal.set([]);
  }
}
