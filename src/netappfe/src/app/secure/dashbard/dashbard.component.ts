import { Component, OnInit } from '@angular/core';
import { MonitoringCallback } from 'src/app/interfaces/monitoring-callback';
import { DashboardService } from 'src/app/services/dashboard.service';
import { Observable,Subscription, interval  } from 'rxjs';

@Component({
  selector: 'app-dashbard',
  templateUrl: './dashbard.component.html',
  styleUrls: ['./dashbard.component.scss']
})
export class DashbardComponent implements OnInit {

  callbacks: MonitoringCallback[];

  constructor(private dashboardService: DashboardService) { }

  ngOnInit(): void {

    this.dashboardService.get_monitoring_callbacks().subscribe(
      (res: any) => {
        this.callbacks = res;
      }
    )
    
    interval(10000).subscribe(
      (val) => { 
        this.dashboardService.get_monitoring_callbacks().subscribe(
          (res: any) => {
            this.callbacks = res;
          }
        )
      });
  }

}
