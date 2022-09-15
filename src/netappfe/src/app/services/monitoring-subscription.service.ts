import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http'

@Injectable({
  providedIn: 'root'
})
export class MonitoringSubscriptionService {

  constructor(private http: HttpClient) { }

  create_monitoring_subscription(data: string) {
    return this.http.get('http://netappdjango:8000/netappserver/api/v1/monitoring/subscribe/' + data + '/');
  }
}
