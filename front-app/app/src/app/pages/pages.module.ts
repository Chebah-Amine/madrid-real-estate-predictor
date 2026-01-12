import { NgModule } from '@angular/core';
import { HomePageComponent } from './home-page/home-page.component';
import { StatisticsComponent } from './statistics-page/statistics.component';
import { ComponentsModule } from '../components/components.module';
import { MapPageComponent } from './map-page/map-page.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { DynamicStatsPageComponent } from './dynamic-stats-page/dynamic-stats-page.component';
import { RouterModule } from '@angular/router';
import { PredictionsPageComponent } from './predictions-page/predictions-page.component';
import { PredictionFiltersComponent } from './predictions-page/inner/prediction-filters/prediction-filters.component';
import { PredictionFormComponent } from './predictions-page/inner/prediction-form/prediction-form.component';
import { PredictionResultsComponent } from './predictions-page/inner/prediction-results/prediction-results.component';
import { TranslocoModule } from '@ngneat/transloco';



@NgModule({
  declarations: [HomePageComponent, StatisticsComponent, MapPageComponent, DynamicStatsPageComponent, PredictionsPageComponent, PredictionFiltersComponent, PredictionFormComponent, PredictionResultsComponent],
  imports: [ CommonModule, ComponentsModule, FormsModule, RouterModule, ReactiveFormsModule, TranslocoModule
  ],
  exports: [HomePageComponent, StatisticsComponent, MapPageComponent, DynamicStatsPageComponent, PredictionsPageComponent],

})
export class PagesModule { }
