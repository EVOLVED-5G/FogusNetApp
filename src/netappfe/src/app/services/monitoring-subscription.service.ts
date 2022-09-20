import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http'
import { environment } from '../../environments/environment';
import { Globals } from '../globals';

@Injectable({
  providedIn: 'root'
})
export class MonitoringSubscriptionService {

  constructor(private http: HttpClient, private globals: Globals) { }

  create_monitoring_subscription(data: string) {
    console.log(this.globals.standardURL)
    return this.http.get('http://' + this.globals.standardURL + '/netappserver/api/v1/monitoring/subscribe/' + data + '/');
  }
}
