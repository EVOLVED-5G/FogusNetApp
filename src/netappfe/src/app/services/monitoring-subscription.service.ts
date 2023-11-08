import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http'
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class MonitoringSubscriptionService {

  constructor(private http: HttpClient) { }

  create_monitoring_subscription(data: string) {
    return this.http.get(environment.backend + '/netappserver/api/v1/monitoring/subscribe/' + data + '/');
  }
}
