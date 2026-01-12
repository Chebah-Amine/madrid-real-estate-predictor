import { DataProviderService } from '../../../services/data-provider.service';
import * as L from 'leaflet';
import * as T from '@turf/turf';
import { MapTypes } from '../map.types';
import { GeoData } from '../map.visualization';

/***| POPULATION |***/

export class PopulationGeoData extends GeoData {
    
    private dataDistrictsLight:any;
    constructor(private _provider:DataProviderService) { super(); this._provider.getDistrictPopulation().subscribe( ds => this.dataDistrictsLight = ds );
    }

    public title() { return MapTypes.Population }
    public display() { 
        this.styleOuterBorders.color = '#000000A0'
        this.styleRegion.color = '#00000070'
        this.styleRegionHover.color = '#000000A0'
        this._provider.getBordersRaw().subscribe( d => { this.borders(d) }); this.data(); 
    }

    private data() {
        this._provider.getDistrictsRaw().subscribe( d => {
            
            if (!d) return;

            const pops = this.dataDistrictsLight.map((e:any)=>e.population);
            const min = Math.min(...pops)
            const max = Math.max(...pops)

            const districtLayers: L.GeoJSON<any>[] = [];

            d.features.forEach((district:any) => {
                
                let polygon = T.polygon(district.coordinates)
                let current = this.dataDistrictsLight.find((k:any) => T.booleanPointInPolygon([k.longitude, k.latitude] , polygon))

                let color   = (current) ? "#008800" : 'gold';
                let opacity = (current) ? this.normalize(current.population,min,max,1) : this.opacityMed;
                const layer = L.geoJSON(district, {
                    style: {
                        ...this.styleRegion,
                        fillColor: color,
                        fillOpacity: opacity,
                    },
                    onEachFeature: this.onEachFeature//.bind(this)
                });

                layer.bindTooltip( (current) ? `<span class="font-bold">${current.name.replace(/,.*?$/, '')}</span><br/>${this.numberFormat.format(current.population)} hab.` : 'No data found' )
                districtLayers.push(layer);

            })

            L.layerGroup(districtLayers).addTo(this.map);

        })
    }

}
