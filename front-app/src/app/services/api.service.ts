import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable } from "rxjs";


@Injectable({ providedIn: 'root'
})
export class ApiService {
  
    private url:string = 'http://127.0.0.1:7000/predict-house-price/neural-network';
    constructor(private http:HttpClient) { }

    public predict(data:any):Observable<any> { return this.http.post<any>(this.url, data);
    }

}
