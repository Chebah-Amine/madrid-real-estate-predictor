import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { PredictionVariable } from '../../../../interfaces/PredictionVariable';

@Component({
  selector: 'app-prediction-filters',
  templateUrl: './prediction-filters.component.html',
  styleUrl: './prediction-filters.component.scss'
})
export class PredictionFiltersComponent implements OnInit {

  @Input () public variables!:PredictionVariable[];
  @Output() private onSelect = new EventEmitter<PredictionVariable[]>();

  public hasSelection:boolean = false;
  private selected:PredictionVariable[] = [];

  public toggleVariable = (item:PredictionVariable) => { 
    !this.isIncluded(item) ? this.selected.push(item) : this.selected = this.selected.filter(e => e.label !== item.label)
    this.hasSelection = this.selected.length > 0;
  }
  public isIncluded(item:PredictionVariable):boolean { return this.selected.map(e => e.label).includes(item.label);
  }

  ngOnInit() {
  }

  public onSubmit() { this.onSelect.emit( this.selected ); 
  }

}
