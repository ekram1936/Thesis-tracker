// import { Component, OnInit } from '@angular/core';
// import { HttpClient } from '@angular/common/http';

// @Component({
//   selector: 'app-labs',
//   standalone: false,
//   templateUrl: './labs.component.html',
//   styleUrls: ['./labs.component.css'],
// })
// export class LabsComponent implements OnInit {
//   labs: any[] = [];
//   filteredLabs: any[] = [];
//   searchQuery: string = '';
//   selectedLab: string = '';
//   selectedStatus: string = '';

//   constructor(private http: HttpClient) {}

//   ngOnInit(): void {
//     this.fetchLabs();
//   }

//   fetchLabs(): void {
//     this.http.get<any[]>('http://0.0.0.0:8000/api/thesis_topics').subscribe({
//       next: (data) => {
//         this.labs = data;
//         this.filteredLabs = [...data];
//       },
//       error: (err) => console.error('Error fetching labs:', err),
//     });
//   }

//   filterLabs(): void {
//     this.filteredLabs = this.labs.filter((lab) => {
//       const matchesLab =
//         this.selectedLab === '' || lab.lab_name === this.selectedLab;

//       const matchesStatus =
//         this.selectedStatus === '' ||
//         lab.topics.some((topic: any) => topic.status === this.selectedStatus);

//       const matchesSearch =
//         this.searchQuery === '' ||
//         lab.lab_name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
//         lab.topics.some((topic: any) =>
//           topic.title.toLowerCase().includes(this.searchQuery.toLowerCase())
//         );

//       return matchesLab && matchesStatus && matchesSearch;
//     });
//   }
// }

import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';

@Component({
  selector: 'app-labs',
  standalone: false,
  templateUrl: './labs.component.html',
  styleUrls: ['./labs.component.css'],
})
export class LabsComponent implements OnInit {
  labs: any[] = [];
  filteredLabs: any[] = [];
  searchQuery: string = '';
  selectedLab: string = '';
  selectedStatus: string = '';

  private apiUrl: string = environment.apiUrl; // Dynamically set API URL based on environment

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.fetchLabs();
  }

  fetchLabs(): void {
    this.http.get<any[]>(`${this.apiUrl}/thesis_topics`).subscribe({
      next: (data) => {
        this.labs = data;
        this.filteredLabs = [...data];
      },
      error: (err) => console.error('Error fetching labs:', err),
    });
  }

  filterLabs(): void {
    this.filteredLabs = this.labs.filter((lab) => {
      const matchesLab =
        this.selectedLab === '' || lab.lab_name === this.selectedLab;

      const matchesStatus =
        this.selectedStatus === '' ||
        lab.topics.some((topic: any) => topic.status === this.selectedStatus);

      const matchesSearch =
        this.searchQuery === '' ||
        lab.lab_name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
        lab.topics.some((topic: any) =>
          topic.title.toLowerCase().includes(this.searchQuery.toLowerCase())
        );

      return matchesLab && matchesStatus && matchesSearch;
    });
  }
}
