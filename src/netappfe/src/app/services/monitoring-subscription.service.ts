import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http'
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class MonitoringSubscriptionService {

  constructor(private http: HttpClient) { }

  create_monitoring_subscription(data: string) {
    console.log("data",data)
    return this.http.get('http://' + environment.backend + '/netappserver/api/v1/monitoring/subscribe/' + data + '/');
  }
}
