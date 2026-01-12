import { AfterViewInit, Component, Input, OnChanges, OnInit, SimpleChanges } from '@angular/core';
import { MapDimensions, MapView } from '../../interfaces/MapInterfaces';
import { GeoData } from '../../utils/maps/map.visualization';
import * as L from 'leaflet';


@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrl: './map.component.scss'
})
export class MapComponent implements OnInit, AfterViewInit, OnChanges {


  /***| ATTRIBUTES |***/
  
  @Input() private view:MapView = { lat:40.50710222091962, lon:-3.5340053809203122, zoom:11};
  @Input() public  dimensions:MapDimensions = { height:"800px", width:"100%" }
  @Input() public  hasLegend:boolean = false;
  @Input() public  geo!:GeoData;
  
  private map!:L.Map;


  /***| HOOKS |***/

  ngOnInit() {
  }
  ngOnChanges(changes: SimpleChanges): void { if(changes['geo']) { this.display() }
  }
  ngAfterViewInit() { this.init(); this.display();
  }
  

  /***| FUNCTIONS |***/

  private init():void {
    
    this.map = L.map('map').setView( [ this.view.lat, this.view.lon ], this.view.zoom )

    L.tileLayer( 'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', { maxZoom: 20, minZoom: 10,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
   
    }) .addTo(this.map);

  }

  private display() { 
    if (this.geo) { this.geo.defineMap(this.map); this.geo.clear(); this.geo.display()
    }
  }


}