// import { Component, OnInit } from '@angular/core';
// import { HttpClient } from '@angular/common/http';
// import Chart from 'chart.js/auto';

// @Component({
//   selector: 'app-insights',
//   standalone: false,
//   templateUrl: './insights.component.html',
//   styleUrls: ['./insights.component.css'],
// })
// export class InsightsComponent implements OnInit {
//   totalLabs: number | null = null;
//   totalOpenThesis: number | null = null;
//   totalClosedThesis: number | null = null;
//   thesisPerLab: { [key: string]: number } | null = null;

//   constructor(private http: HttpClient) {}

//   ngOnInit(): void {
//     this.fetchTotalLabs();
//     this.fetchTotalOpenThesis();
//     this.fetchTotalClosedThesis();
//     this.fetchThesisPerLab();
//   }

//   fetchTotalLabs(): void {
//     this.http
//       .get<number>('http://0.0.0.0:8000/api/insights/total_labs')
//       .subscribe({
//         next: (data) => (this.totalLabs = data),
//         error: (err) => console.error('Error fetching total labs:', err),
//       });
//   }

//   fetchTotalOpenThesis(): void {
//     this.http
//       .get<number>('http://0.0.0.0:8000/api/insights/total_open_thesis')
//       .subscribe({
//         next: (data) => (this.totalOpenThesis = data),
//         error: (err) => console.error('Error fetching total open thesis:', err),
//       });
//   }

//   fetchTotalClosedThesis(): void {
//     this.http
//       .get<number>('http://0.0.0.0:8000/api/insights/total_closed_thesis')
//       .subscribe({
//         next: (data) => (this.totalClosedThesis = data),
//         error: (err) =>
//           console.error('Error fetching total closed thesis:', err),
//       });
//   }

//   fetchThesisPerLab(): void {
//     this.http
//       .get<{ [key: string]: number }>(
//         'http://0.0.0.0:8000/api/insights/thesis_per_lab'
//       )
//       .subscribe({
//         next: (data) => {
//           this.thesisPerLab = data;
//           this.initializeChart(data);
//         },
//         error: (err) => console.error('Error fetching thesis per lab:', err),
//       });
//   }

import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import Chart from 'chart.js/auto';
import { environment } from '../../environments/environment';

@Component({
  selector: 'app-insights',
  standalone: false,
  templateUrl: './insights.component.html',
  styleUrls: ['./insights.component.css'],
})
export class InsightsComponent implements OnInit {
  totalLabs: number | null = null;
  totalOpenThesis: number | null = null;
  totalClosedThesis: number | null = null;
  thesisPerLab: { [key: string]: number } | null = null;

  private apiUrl: string = environment.apiUrl; // Dynamically set API URL based on environment

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.fetchTotalLabs();
    this.fetchTotalOpenThesis();
    this.fetchTotalClosedThesis();
    this.fetchThesisPerLab();
  }

  fetchTotalLabs(): void {
    this.http.get<number>(`${this.apiUrl}/insights/total_labs`).subscribe({
      next: (data) => (this.totalLabs = data),
      error: (err) => console.error('Error fetching total labs:', err),
    });
  }

  fetchTotalOpenThesis(): void {
    this.http
      .get<number>(`${this.apiUrl}/insights/total_open_thesis`)
      .subscribe({
        next: (data) => (this.totalOpenThesis = data),
        error: (err) => console.error('Error fetching total open thesis:', err),
      });
  }

  fetchTotalClosedThesis(): void {
    this.http
      .get<number>(`${this.apiUrl}/insights/total_closed_thesis`)
      .subscribe({
        next: (data) => (this.totalClosedThesis = data),
        error: (err) =>
          console.error('Error fetching total closed thesis:', err),
      });
  }

  fetchThesisPerLab(): void {
    this.http
      .get<{ [key: string]: number }>(`${this.apiUrl}/insights/thesis_per_lab`)
      .subscribe({
        next: (data) => {
          this.thesisPerLab = data;
          this.initializeChart(data);
        },
        error: (err) => console.error('Error fetching thesis per lab:', err),
      });
  }

  initializeChart(thesisPerLab: { [key: string]: number }): void {
    if (typeof document !== 'undefined') {
      const labels = Object.keys(thesisPerLab);
      const data = Object.values(thesisPerLab);

      const modernColors = [
        '#4CAF50',
        '#2196F3',
        '#FFC107',
        '#FF5722',
        '#673AB7',
        '#00BCD4',
        '#E91E63',
        '#9C27B0',
        '#FF9800',
        '#03A9F4',
      ];

      const generateModernColors = (count: number): string[] => {
        const colors: string[] = [];
        for (let i = 0; i < count; i++) {
          colors.push(modernColors[i % modernColors.length]);
        }
        return colors;
      };

      const backgroundColors = generateModernColors(labels.length);

      const canvas = document.getElementById(
        'thesisChart'
      ) as HTMLCanvasElement;
      if (canvas) {
        const ctx = canvas.getContext('2d');
        if (ctx) {
          new Chart(ctx, {
            type: 'bar',
            data: {
              labels,
              datasets: [
                {
                  data,
                  backgroundColor: backgroundColors,
                  borderColor: backgroundColors,
                  borderWidth: 2,
                },
              ],
            },
            options: {
              responsive: true,
              maintainAspectRatio: false, // Allows the chart to adjust height
              plugins: {
                legend: {
                  display: false,
                },
                title: {
                  display: true,
                  text: 'Number of Thesis Topics per Lab',
                  font: {
                    size: 18,
                    family: 'Roboto, sans-serif',
                  },
                  color: '#333',
                },
              },
              scales: {
                x: {
                  grid: {
                    drawOnChartArea: false,
                    color: '#ddd',
                  },
                  ticks: {
                    font: {
                      size: 12,
                      family: 'Roboto, sans-serif',
                    },
                    color: '#555',
                  },
                },
                y: {
                  grid: {
                    color: '#f0f0f0',
                  },
                  ticks: {
                    font: {
                      size: 12,
                      family: 'Roboto, sans-serif',
                    },
                    color: '#555',
                  },
                },
              },
            },
          });
        } else {
          console.error('Failed to acquire canvas context.');
        }
      } else {
        console.error('Canvas element not found.');
      }
    }
  }
}
