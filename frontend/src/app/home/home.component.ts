import { Component, HostListener } from '@angular/core';

@Component({
  selector: 'app-home',
  standalone: false,

  templateUrl: './home.component.html',
  styleUrl: './home.component.css',
})
export class HomeComponent {
  menuOpen: boolean = false;
  showModal: boolean = false;

  toggleMenu(): void {
    this.menuOpen = !this.menuOpen;
  }

  closeMenu(): void {
    this.menuOpen = false;
  }

  openModal(event: Event): void {
    event.preventDefault(); // Prevent default link behavior
    this.showModal = true; // Show the modal
  }

  closeModal(): void {
    this.showModal = false; // Hide the modal
  }

  // Close modal when clicking outside of the modal-content
  closeOnBackdropClick(event: MouseEvent): void {
    const target = event.target as HTMLElement;
    if (target.classList.contains('modal')) {
      this.closeModal();
    }
  }

  // Close modal when pressing the ESC key
  @HostListener('document:keydown.escape', ['$event'])
  handleEscapeKey(event: KeyboardEvent): void {
    this.closeModal(); // Hide the modal on pressing ESC key
  }
  // Method to scroll to a specific section
  scrollToSection(sectionId: string): void {
    const section = document.getElementById(sectionId);
    if (section) {
      section.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }
}
