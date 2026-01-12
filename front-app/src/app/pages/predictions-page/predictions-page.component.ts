import { Component, OnInit } from '@angular/core';
import { PredictionVariable } from '../../interfaces/PredictionVariable';
import { StructureProviderService } from '../../services/structure-provider';

@Component({
  selector: 'app-predictions-page',
  templateUrl: './predictions-page.component.html',
  styleUrl: './predictions-page.component.scss'
})
export class PredictionsPageComponent implements OnInit {
  
  public step = 1;
   
  public variables!:PredictionVariable[];
  public selectedFilters:PredictionVariable[] = [];
  public apiResults:any; // TODO : Create the appropriate interface for this

  constructor(private _structure:StructureProviderService) {}
  ngOnInit() { this._structure.getVariables().subscribe(data => this.variables = data)//.add(() => console.log(this.variables))
  }

  public onSelect(event:PredictionVariable[]) { this.selectedFilters = event; this.step ++;
  }
  public onSubmit(event:any) { // TODO : Create the appropriate interface
    this.step++;
    this.apiResults = event;
  }


  public onPrevious() { this.step -- ;
  }
  public onRestart () { this.step = 1;
  }

}
