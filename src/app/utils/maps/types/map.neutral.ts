import { DataProviderService } from '../../../services/data-provider.service';
import * as L from 'leaflet';
import { MapTypes } from '../map.types';
import { GeoData } from '../map.visualization';

/***| BLANK |***/

export class NeutralGeoData extends GeoData {

    constructor(private _provider:DataProviderService) { super();
    }
    public title() { return MapTypes.Neutral }
    public display() { 
        this.styleRegion.fillOpacity = 0;
        this.styleRegion.fillColor = '#fff';
        this.styleRegion.dashArray = '1 1'
        this.styleRegion.color = '#00000025'
        this.styleOuterBorders.color = '#00000050'
        this.styleOuterBorders.className = 'map-shadow'

        this._provider.getBordersRaw().subscribe( d => { this.borders(d) }); this.data()
    }

    private data() {
        this._provider.getDistrictsRaw().subscribe( d => {
            d.features.forEach((district:any) => {
                L.geoJSON(district, { style: this.styleRegion
                })
                .addTo(this.map)
            })
        });
    }

}