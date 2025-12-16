import { Component, ElementRef, EventEmitter, Input, OnInit, Output, ViewChild } from '@angular/core';
import { PredictionVariable } from '../../../../interfaces/PredictionVariable';
import { FormBuilder, FormGroup } from '@angular/forms';
import { ApiService } from '../../../../services/api.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-prediction-form',
  templateUrl: './prediction-form.component.html',
  styleUrl: './prediction-form.component.scss'
})
export class PredictionFormComponent implements OnInit {

  @ViewChild("predictionForm") predictionForm!:ElementRef;

  @Input () public variables!:PredictionVariable[];
  @Output() public onPrevious = new EventEmitter<void>();
  @Output() public onSubmit   = new EventEmitter<any> ();

  public strings :PredictionVariable[] = [];
  public numbers :PredictionVariable[] = [];
  public booleans:PredictionVariable[] = [];

  public form!:FormGroup;

  public disabled:boolean = false;

  constructor (private formBuilder:FormBuilder, private _api:ApiService, private _router:Router) {}
  ngOnInit() {

    this.strings  = this.strings .concat(this.variables.filter(e => e.type === 'string' ))
    this.numbers  = this.numbers .concat(this.variables.filter(e => e.type === 'number' ))
    this.booleans = this.booleans.concat(this.variables.filter(e => e.type === 'boolean'))

    // this.variables = JSON.parse(`[{"label":"superficy1","type":"number", "value": "122"},{"label":"superficy6","type":"number"},{"label":"district","type":"string"},{"label":"superficy2","type":"number"},{"label":"superficy3","type":"number"},{"label":"superficy4","type":"number"},{"label":"superficy5","type":"number"}]`)

    this.form = this.formBuilder.group({});

    this.variables.forEach( e => {
      this.form.addControl(e.label, this.formBuilder.control(e.value, undefined));
    })

  }

  public onPreviousButton() { this.onPrevious.emit();
  }

  public onSubmitButton() {

    this.disabled = true;

    let result = this.variables.filter(e => this.form.value[e.label] !== undefined).map(e => {
      let value:any = this.form.value[e.label]
      switch(e.type) {
        case "number"  : value = parseFloat(value); break;
        case "boolean" : value = (value === "") ? false : value; break;
        default : break;
      }
      return { [e.label]: value }
    })

    if (Object.keys(result).length === 0) { alert('No data') ; return }

    // result.push({price: 1234})
    result = Object.assign({}, ...result)


    this._api.predict(result).subscribe( (data:any) => {
      console.log(data) ;
      let res = { result: result, price: data.price }
      this.onSubmit.emit(res)
    })
    .add ( () =>
      this.disabled = false
    )

  }

}
