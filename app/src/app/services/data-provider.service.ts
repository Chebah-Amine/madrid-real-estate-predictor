import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Papa } from 'ngx-papaparse';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class DataProviderService {

  
  constructor(private http:HttpClient, private parser: Papa) { }

  
  /***| GET THE DATA FROM CSV FILE |***/

  public getData(): Observable<any> {
    return this.http.get('/assets/dataset-clean.csv', { responseType: 'text' });
  }

  public getDataWithCoords():Observable<any> {
    return this.http.get('/assets/dataset-with-geolocations.csv', { responseType: 'text' });
  }
  
  public getDistrictsRaw():Observable<any> {
    return this.http.get('/assets/barrios.json', { responseType: 'json' });
  }
  
  public getDistrictEstatePrices():Observable<any> {
    return this.http.get('/assets/barrios-precios.json', { responseType: 'json' });
  }
  
  public getDistrictPopulation():Observable<any> {
    return this.http.get('/assets/barrios-poblacion.json', { responseType: 'json' });
  }
  
  public getBordersRaw():Observable<any> {
    return this.http.get('/assets/borders.json', { responseType: 'json' });
  }


  /***| 3rd PARTY METHODS |***/

  public parseCsv(csv:string) {
    const json = this.parser.parse(csv, { header: true, skipEmptyLines: true }).data;
    return json;
  }

  
}
