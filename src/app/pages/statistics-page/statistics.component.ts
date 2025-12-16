import { Component, OnInit } from '@angular/core';
import { DataProviderService } from '../../services/data-provider.service';
import { ChartsProvider } from '../../services/charts-provider.service';
import { HistogramDataset } from '../../interfaces/HistogramDataset';
import  _  from 'lodash';
import { PieChartDataset } from '../../interfaces/PieChartDataset';


@Component({
  selector: 'app-statistics',
  templateUrl: './statistics.component.html',
  styleUrls: ['./statistics.component.scss']
})
export class StatisticsComponent implements OnInit {
  

  /***| ATTRIBUTES |***/
  
  public dataset: any[] = [];
  private chart1!:HTMLCanvasElement;
  private chart2!:HTMLCanvasElement;
  private chart3!: HTMLCanvasElement;
  private chart4!: HTMLCanvasElement;

  
  /***| HOOKS |***/
  
  constructor( private _data:DataProviderService, private _charts:ChartsProvider ) { }
  

  ngAfterViewInit() {
    this.chart1 = document.querySelector('#chart-1') as HTMLCanvasElement;
    this.chart2 = document.querySelector('#chart-2') as HTMLCanvasElement;
    this.chart3 = document.querySelector('#chart-3') as HTMLCanvasElement;
    this.chart4 = document.querySelector('#chart-4') as HTMLCanvasElement;
  }  

  ngOnInit(): void {
    this._data.getData().subscribe(   (data: any) => { this.dataset = this._data.parseCsv(data); }
    )
    .add( () => this.charts() )
  }
  
  
  /***| METHODS |***/

  public charts() {

    this.initChart1();
    this.initChart2();
    this.initChart3();
    this.initChart4();

  }


  /***| INDIVIDUAL CHART GENERATION |***/

  private initChart1() {

    let data = this.dataset.map(item => {
      return { rentPrice: item.rent_price, buyPrice: item.buy_price, rooms: item.n_rooms }
    });

    let groupedByRooms = _.groupBy(data, 'rooms')
    let roomBuyPrices = []; let roomRentPrices = [];
    let labels = []

    for (const rooms in groupedByRooms) {
      const buyPrices  = groupedByRooms[rooms].map(item => Math.abs(parseFloat(item.buyPrice ))).reduce((a,b) => a+b) / groupedByRooms[rooms].length;
      const rentPrices = groupedByRooms[rooms].map(item => Math.abs(parseFloat(item.rentPrice))).reduce((a,b) => a+b) / groupedByRooms[rooms].length;

      roomBuyPrices .push({ rooms: rooms, meanBuyPrice : Math.round(buyPrices  * 100) / 100 });
      roomRentPrices.push({ rooms: rooms, meanRentPrice: Math.round(rentPrices * 100) / 100 });

      labels.push(`${rooms}`)

    }

    const ds:HistogramDataset[] = [
      {
        label: 'Mean Buy Price',
        data: roomBuyPrices.map(e => e.meanBuyPrice),
        backgroundColor: 'rgba(255, 58, 58, 0.60)',
        borderColor: 'rgba(255, 255, 255, 0)',
        borderWidth: 1
      },
      {
        label: 'Mean Rent Price',
        data: roomRentPrices.map(e => e.meanRentPrice),
        backgroundColor: 'rgba(0, 79, 220, 0.60)',
        borderColor: 'rgba(255, 255, 255, 0)',
        borderWidth: 1,
        hidden: true
      }
    ]

    // Generate Chart HERE
    this._charts.histogram( labels, ds, 'rooms', 'prices €',  this.chart1, 100
    );

  }

  private initChart2() {
    this.chart2
  }

  
  private initChart3() {
  // Filtrer les types de maison non vides
  const houseTypes = this.dataset
    .filter(item => item.house_type_id.trim() !== "") // Vérifie si house_type_id n'est pas vide
    .map(item => {
      // Mapping des équivalents pour chaque house_type_id
      switch (item.house_type_id) {
        case 'HouseType 1: Pisos':
          return 'Apartment';
        case 'HouseType 2: Casa o chalet':
          return 'House/Cottage';
        case 'HouseType 4: D√∫plex':
          return 'Duplex';
        case 'HouseType 5: √Åticos':
          return 'Attic';
        default:
          return item.house_type_id;
      }
    });

  // Obtenir les types de maison uniques
  const uniqueHouseTypes = [...new Set(houseTypes)];

  // Compter le nombre de chaque type de maison
  const countHouseTypes = uniqueHouseTypes.map(houseType => {
    return houseTypes.filter(type => type === houseType).length;
  });

  // Créer le jeu de données pour la charte
  const ds: PieChartDataset = {
    labels: uniqueHouseTypes,
    data: countHouseTypes,
    backgroundColor: ['rgba(255, 99, 132, 0.6)', 'rgba(54, 162, 235, 0.6)', 'rgba(255, 206, 86, 0.6)', 'rgba(75, 192, 192, 0.6)', 'rgba(153, 102, 255, 0.6)'],
    borderColor: ['rgba(255, 99, 132, 1)', 'rgba(54, 162, 235, 1)', 'rgba(255, 206, 86, 1)', 'rgba(75, 192, 192, 1)', 'rgba(153, 102, 255, 1)'],
    borderWidth: 1
  };

  // Afficher la pie chart
  this._charts.pieChart(ds.labels, ds.data, ds.backgroundColor, ds.borderColor, ds.borderWidth, this.chart3);
}

private initChart4() {
  // Colonnes booléennes spécifiées
  const columnsMap = [
    "has_green_zones",
    "is_accessible",
    "is_floor_under",
    "is_renewal_needed",
    "has_ac",
    "has_pool",
    "has_terrace",
    "has_balcony",
    "has_parking",
    "energy_certificate",
    "has_garden",
    "is_new_development"
  ];

  // Filtrage des colonnes booléennes
  const booleanColumns: string[] = [];
  this.dataset.forEach(item => {
    columnsMap.forEach(column => {
      if (typeof item[column] === 'boolean') {
        booleanColumns.push(column);
      }
    });
  });

  console.log("liste des colones bool : ",booleanColumns)

  const buyPriceData: number[] = [];
  booleanColumns.forEach(column => {
    const trueValues: number[] = [];
    const falseValues: number[] = [];

    this.dataset.forEach(item => {
      const buyPrice = parseFloat(item["buy_price"]);
      const value = item[column];

      if (!isNaN(buyPrice) && typeof value === "boolean") {
        if (value) {
          trueValues.push(buyPrice);
        } else {
          falseValues.push(buyPrice);
        }
      }
    });

    const trueMean = this.calculateMean(trueValues);
    const falseMean = this.calculateMean(falseValues);

    buyPriceData.push(trueMean, falseMean);
    console.log("liste des buprices : ", buyPriceData)
  });

  const labels: string[] = columnsMap.map(column => column.replace(/_/g, " "));
  const datasets: HistogramDataset[] = [
    {
      label: "True",
      data: buyPriceData.filter((_, index) => index % 2 === 0),
      backgroundColor: 'rgba(54, 162, 235, 0.6)',
      borderColor: 'rgba(54, 162, 235, 1)',
      borderWidth: 1
    },
    {
      label: "False",
      data: buyPriceData.filter((_, index) => index % 2 !== 0),
      backgroundColor: 'rgba(255, 99, 132, 0.6)',
      borderColor: 'rgba(255, 99, 132, 1)',
      borderWidth: 1
    }
  ];

  console.log("les labels : ", labels)
  console.log("les datasets : ", datasets)
  this._charts.priceHistogram(labels, datasets, 'Variables', 'Buy Price', this.chart4);
}

private calculateMean(data: number[]): number {
  if (data.length === 0) return 0;
  const sum = data.reduce((acc, curr) => acc + curr, 0);
  return sum / data.length;
}  

}
