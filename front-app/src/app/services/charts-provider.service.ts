import { Injectable } from '@angular/core';
import { Chart, LinearScale, registerables } from 'chart.js';
import { HistogramDataset } from '../interfaces/HistogramDataset';

@Injectable({
  providedIn: 'root'
})
export class ChartsProvider {


  constructor() { Chart.register(...registerables);
  }


  public histogram(labels:any[], datasets:HistogramDataset[], xTitle:string, yTitle:string, canvas: HTMLCanvasElement, step:number = 1): Chart|undefined {

    const context = canvas.getContext('2d');
    datasets.forEach(e => {
      if (e.hidden === undefined) e.hidden = false;
    })
    let chart = undefined;
    let xAxisScale:'linear' | 'category' = (typeof labels[0] === 'string') ? 'category' : 'linear';

    if (context) chart = new Chart(
      context, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: datasets
      },
      options: {
        scales: {
          x: {
            type: xAxisScale,
            title: { display: true, text: xTitle
            }
          },
          y: {
            title: { display: true, text: yTitle
            }
          }
        }
      }
    });

    return chart;

  }


  public pieChart(labels: string[], data: number[], backgroundColor: string[], borderColor: string[], borderWidth: number, canvas: HTMLCanvasElement): void {
  const context = canvas.getContext('2d');
  if (context) {
    new Chart(
      context, {
        type: 'pie',
        data: {
          labels: labels,
          datasets: [{
            data: data,
            backgroundColor: backgroundColor,
            borderColor: borderColor,
            borderWidth: borderWidth
          }]
        }
      }
    );
  }
}

public priceHistogram(labels: string[], datasets: HistogramDataset[], xTitle: string, yTitle: string, canvas: HTMLCanvasElement): void {
  const context = canvas.getContext('2d');
  if (context) {
    new Chart(context, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: datasets
      },
      options: {
        scales: {
          x: {
            title: { display: true, text: xTitle }
          },
          y: {
            title: { display: true, text: yTitle }
          }
        }
      }
    });
  }
}
}
