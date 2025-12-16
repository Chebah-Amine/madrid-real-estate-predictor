import * as L from 'leaflet';
import { MapTypes } from './map.types';


/***| MAIN ABSTRACT CLASS |***/

export abstract class GeoData {


    /***| SHARED ATTRIBUTES |***/

    protected map!:L.Map;

    protected styleOuterBorders:L.PathOptions = { weight:2, color:'#00000060', fillOpacity:0 }
    protected styleRegion:L.PathOptions = { color:'#00000030', weight:1, dashArray:"1 2" }
    protected styleRegionHover:L.PathOptions = { color: '#00000090', weight:1, dashArray: '', fillOpacity: 0.8 };


    protected opacityMax:number = 0.89;
    protected opacityMin:number = 0.25;
    protected opacityMed:number = 0.40;


    protected numberFormat = new Intl.NumberFormat('eu', {
        useGrouping: true
    });

    /***| ABSTRACT METHODS |***/

    public abstract display():void;
    public abstract title():MapTypes;


    /***| SHARED METHODS |***/

    public defineMap(m:L.Map) { this.map = m 
    }
    public clear() { 
        if (this.map) this.map.eachLayer((e:any) => { if (e instanceof L.GeoJSON) this.map.removeLayer(e)
        });
    }
    protected borders(data:any) { L.geoJSON(data, {style: this.styleOuterBorders}).addTo(this.map)
    }
    protected normalize(value:number, min:number, max:number, scale:number) {
        return Math.max(0, Math.min(1, (value - min) / (max - min))) % this.opacityMax + this.opacityMin;
    }

    protected highlight = (e:any) => {
        var layer = e.target; 
        layer.options.originalStyle = layer.options.style;
        layer.setStyle(this.styleRegionHover);
        layer.bringToFront();
    }
    protected resetHighlight = (e:any) => {
        var layer = e.target; 
        layer.setStyle(layer.options.originalStyle);
        layer.bringToFront();
    }

    protected onEachFeature = (feature:any, layer:any) => {
        layer.on({
            mouseover: this.highlight,
            mouseout : this.resetHighlight,
        });
    }

}
