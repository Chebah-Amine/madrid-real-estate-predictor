import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { RouterModule } from '@angular/router';
import { NavbarComponent } from './navbar/navbar.component';
import { MapComponent } from './map/map.component';
import { CommonModule } from '@angular/common';


@NgModule({
  declarations: [ NavbarComponent, MapComponent ],
  imports: [ CommonModule, HttpClientModule, RouterModule ],
  exports: [ NavbarComponent , MapComponent ]
})
export class ComponentsModule { }
