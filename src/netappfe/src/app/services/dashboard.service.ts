import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http'
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class DashboardService {

  constructor(private http: HttpClient) { }

  get_monitoring_callbacks() {
    return this.http.get('http://' + environment.backend + '/netappserver/api/v1/monitoring/callback/');
  }
}
