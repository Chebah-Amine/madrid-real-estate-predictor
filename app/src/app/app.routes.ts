import { RouterModule, Routes } from '@angular/router';
import { HomePageComponent } from './pages/home-page/home-page.component';
import { StatisticsComponent } from './pages/statistics-page/statistics.component';
import { NgModule } from '@angular/core';
import { MapPageComponent } from './pages/map-page/map-page.component';
import { DynamicStatsPageComponent } from './pages/dynamic-stats-page/dynamic-stats-page.component';
import { PredictionsPageComponent } from './pages/predictions-page/predictions-page.component';

export const routes: Routes = [
    { path:'', component: HomePageComponent },
    { path:'stats', component: StatisticsComponent },
    { path:'map', component: MapPageComponent },
    { path:'dynamic', component: DynamicStatsPageComponent },
    { path:'predictions', component: PredictionsPageComponent },
];

@NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule]
})
export class AppRoutingModule { }