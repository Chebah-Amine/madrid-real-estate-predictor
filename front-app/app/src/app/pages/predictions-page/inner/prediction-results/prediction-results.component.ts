import { AfterViewInit, Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { CountUp } from 'countup.js';

@Component({
  selector: 'app-prediction-results',
  templateUrl: './prediction-results.component.html',
  styleUrl: './prediction-results.component.scss'
})
export class PredictionResultsComponent implements OnInit, AfterViewInit {

  @Input () public result:any;
  @Output() public onRestart = new EventEmitter<void>();

  public display:{name:string, value:any}[] = [];

  ngOnInit() {

    if (this.result) {
      Object.keys(this.result.result).forEach((k:string) => {
        if (k !== "price")
          this.display.push({ name: k, value: this.result.result[k] });
      })

    }

  }
  ngAfterViewInit() {

    window.scrollTo({ top: 0, behavior: 'smooth' });
    const options = { duration: 2 };

    let price = (this.result && this.result.price) ? this.result.price : 0;

    let countup = new CountUp('countup', price, options);
    if (!countup.error) countup.start(() => {});
    else console.error(countup.error);

  }

  public onRestartButton() { this.onRestart.emit();
  }



}
