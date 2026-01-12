import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { PredictionVariable } from "../interfaces/PredictionVariable";
import { Observable } from "rxjs";

@Injectable({ providedIn: 'root'
})
export class StructureProviderService {
  
    constructor(private http:HttpClient) { }
    public getVariables():Observable<PredictionVariable[]> { return this.http.get<PredictionVariable[]>('/assets/prediction-variables.json', { responseType: 'json' });
    }

}