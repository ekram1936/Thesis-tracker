import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { InsightsComponent } from './insights/insights.component';
import { LabsComponent } from './labs/labs.component';

const routes: Routes = [
  { path: '', component: HomeComponent }, // Default to home
  { path: '**', redirectTo: '' }, // Redirect unknown paths to home
];

@NgModule({
  imports: [
    RouterModule.forRoot(routes, {
      anchorScrolling: 'enabled', // Enables scrolling to anchors like #home
      scrollPositionRestoration: 'enabled', // Restores scroll position when navigating
    }),
  ],
  exports: [RouterModule],
})
export class AppRoutingModule {}
