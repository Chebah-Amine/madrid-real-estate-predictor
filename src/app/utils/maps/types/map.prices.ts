import { DataProviderService } from '../../../services/data-provider.service';
import * as L from 'leaflet';
import * as T from '@turf/turf';
import { MapTypes } from '../map.types';
import { GeoData } from '../map.visualization';

/***| PRICES |***/

export class PricesGeoData extends GeoData {


    /***| INIT |***/

    private dataDistrictsLight:any;
    constructor(private _provider:DataProviderService) { super(); this._provider.getDistrictEstatePrices().subscribe( ds => this.dataDistrictsLight = ds );
    }


    /***| METHODS |***/

    public title() { return MapTypes.Prices }

    public display() { 
        this.styleOuterBorders.color = '#000000A0'
        this.styleRegion.color = '#00000070'
        this.styleRegionHover.color = '#000000A0'
        this._provider.getBordersRaw().subscribe( d => { this.borders(d) }); this.data(); 
    }

    private data() {
        this._provider.getDistrictsRaw().subscribe( d => {
            
            if (!d) return;

            const districtLayers: L.GeoJSON<any>[] = [];
            const prices = this.dataDistrictsLight.map((e:any) => e.mean_price);
            const min = Math.min(...prices);
            const max = Math.max(...prices);
            console.log(min, max)

            d.features.forEach((district:any) => {
                
                let polygon = T.polygon(district.coordinates)
                let current = this.dataDistrictsLight.find((k:any) => T.booleanPointInPolygon([k.longitude, k.latitude] , polygon))

                let color   = (current) ? "#EE0000" : 'gold';
                let opacity = (current) ? this.normalize(current.mean_price,min,max,1) : this.opacityMin;

                const layer = L.geoJSON(district, {
                    style: {
                        ...this.styleRegion,
                        fillColor: color,
                        fillOpacity: opacity,
                    },
                    onEachFeature: this.onEachFeature//.bind(this)
                });
                layer.bindTooltip( (current) ? `<span class="font-bold">${current.quartier.replace(/,.*?$/, '')}</span><br/>${this.numberFormat.format(current.mean_price)} €` : 'No data found' )

                districtLayers.push(layer);

            })

            L.layerGroup(districtLayers).addTo(this.map);

        })
    }

}
