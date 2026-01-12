import { Component, OnInit } from '@angular/core';
import { DataProviderService } from '../../services/data-provider.service';
import { ChartsProvider } from '../../services/charts-provider.service';
import { HistogramDataset } from '../../interfaces/HistogramDataset';
import { Chart } from 'chart.js';
import  _  from 'lodash';


@Component({
  selector: 'app-dynamic-stats-page',
  templateUrl: './dynamic-stats-page.component.html',
  styleUrl: './dynamic-stats-page.component.scss'
})
export class DynamicStatsPageComponent implements OnInit {


  /***| ATTRIBUTES |***/
  
  private dataset!:any;
  private chart!:HTMLCanvasElement;
  private chartContext?:Chart;
  public  lines:number = 0;


  /***| FORM ATTRIBUTES |****/

  public isAccessible:boolean = true
  public isFloorUnder:boolean = true
  public isRenewalNeeded:boolean = true
  public hasAc:boolean = false
  public hasPool:boolean = false
  public hasTerrace:boolean = false
  public hasBalcony:boolean = false
  public hasParking:boolean = false
  public energyCertificate:boolean = false
  public hasGarden:boolean = false
  public isNewDevelopment:boolean = false


  /***| FORM DEFINITIONS |***/

  public toggleIsAccessible = () => { this.isAccessible = !this.isAccessible;  this.refresh() }
  public toggleIsFloorUnder = () => { this.isFloorUnder = !this.isFloorUnder;  this.refresh() }
  public toggleIsRenewalNeeded = () => { this.isRenewalNeeded = !this.isRenewalNeeded;  this.refresh() }
  public toggleHasAc = () => { this.hasAc = !this.hasAc;  this.refresh() }
  public toggleHasPool = () => { this.hasPool = !this.hasPool;  this.refresh() }
  public toggleHasTerrace = () => { this.hasTerrace = !this.hasTerrace;  this.refresh() }
  public toggleHasBalcony = () => { this.hasBalcony = !this.hasBalcony;  this.refresh() }
  public toggleHasParking = () => { this.hasParking = !this.hasParking;  this.refresh() }
  public toggleEnergyCertificate = () => { this.energyCertificate = !this.energyCertificate;  this.refresh() }
  public toggleHasGarden = () => { this.hasGarden = !this.hasGarden;  this.refresh() }
  public toggleIsNewDevelopment = () => { this.isNewDevelopment = !this.isNewDevelopment;  this.refresh() }
  
  

  /***| HOOKS |***/

  constructor(private _data:DataProviderService, private _chart:ChartsProvider) {}
  ngOnInit() {
    
    this._data.getDataWithCoords().subscribe( data => this.dataset = this._data.parseCsv(data)
    )
    .add(() => this.init())

  }
  ngAfterViewInit() { this.chart = document.querySelector('#chart') as HTMLCanvasElement;
  }


  /***| PAGE METHODS |***/

  private init() { this.initChart();
  }

  private filters(data:any) {
    if(this.isAccessible) data = data.filter((e:any) => e.isAccessible === 'True')
    if(this.isFloorUnder) data = data.filter((e:any) => e.isFloorUnder === 'True')
    if(this.isRenewalNeeded) data = data.filter((e:any) => e.isRenewalNeeded === 'True')
    if(this.hasAc) data = data.filter((e:any) => e.hasAc === 'True')
    if(this.hasPool) data = data.filter((e:any) => e.hasPool === 'True')
    if(this.hasTerrace) data = data.filter((e:any) => e.hasTerrace === 'True')
    if(this.hasBalcony) data = data.filter((e:any) => e.hasBalcony === 'True')
    if(this.hasParking) data = data.filter((e:any) => e.hasParking === 'True')
    if(this.energyCertificate) data = data.filter((e:any) => e.energyCertificate === 'True')
    if(this.hasGarden) data = data.filter((e:any) => e.hasGarden === 'True')
    if(this.isNewDevelopment) data = data.filter((e:any) => e.isNewDevelopment === 'True')
    return data;
  }

  private refresh() {
    this.chartContext?.destroy();
    this.initChart();
  }

  private initChart() {
    
    let data = this.dataset.map((item:any) => {
      return { rentPrice: item.rent_price, buyPrice: item.buy_price, district: item.subtitle?.replace(/,\s*Madrid/g, ''), isAccessible: item.is_accessible, isFloorUnder: item.is_floor_under, isRenewalNeeded: item.is_renewal_needed, hasAc: item.has_ac, hasPool: item.has_pool, hasTerrace: item.has_terrace, hasBalcony: item.has_balcony, hasParking: item.has_parking, energyCertificate: item.energy_certificate, hasGarden: item.has_garden, isNewDevelopment: item.is_new_development }
    })
    
    data = this.filters(data)
    let grouped = _.groupBy(data, 'district');

    // TODO : DRY
    let roomBuyPrices = []; let roomRentPrices = []; let labels = []
    this.lines = data.length;

    const limit = 250;
    let   count = 0 ;
    
    for (const district in grouped) {

      if (count === limit) break;

      const buyPrices  = grouped[district].map(item => Math.abs(parseFloat(item.buyPrice ))).reduce((a,b) => a+b) / grouped[district].length;
      const rentPrices = grouped[district].map(item => Math.abs(parseFloat(item.rentPrice))).reduce((a,b) => a+b) / grouped[district].length;

      roomBuyPrices .push({ district: district, meanBuyPrice : Math.round(buyPrices  * 100) / 100 });
      roomRentPrices.push({ district: district, meanRentPrice: Math.round(rentPrices * 100) / 100 });

      labels.push(district)

    }

    const ds:HistogramDataset[] = [
      {
        label: 'Mean Buy Price',
        data: roomBuyPrices.map(e => e.meanBuyPrice),
        backgroundColor: 'rgba(255, 58, 58, 0.60)',
        borderColor: 'rgba(255, 255, 255, 0)',
        borderWidth: 1,
        hidden: true
      },
      {
        label: 'Mean Rent Price',
        data: roomRentPrices.map(e => e.meanRentPrice),
        backgroundColor: 'rgba(0, 79, 220, 0.60)',
        borderColor: 'rgba(255, 255, 255, 0)',
        borderWidth: 1
      }
    ]

    // Generate Chart HERE
    this.chartContext = this._chart.histogram( labels, ds, 'districts', 'prices €',  this.chart, 100
    );

  }

}
