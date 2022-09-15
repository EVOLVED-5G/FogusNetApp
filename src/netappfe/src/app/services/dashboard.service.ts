import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http'

@Injectable({
  providedIn: 'root'
})
export class DashboardService {

  constructor(private http: HttpClient) { }

  get_monitoring_callbacks() {
    // this.http.get('http://localhost:8000/netappserver/api/v1/cells/update/');
    return this.http.get('http://netappdjango:8000/netappserver/api/v1/monitoring/callback/');
  }
}
