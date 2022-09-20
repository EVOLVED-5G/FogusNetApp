import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http'
import { environment } from '../../environments/environment';
import { Globals } from '../globals';

@Injectable({
  providedIn: 'root'
})
export class DashboardService {

  constructor(private http: HttpClient, private globals: Globals) { }

  get_monitoring_callbacks() {
    console.log(this.globals.standardURL)
    return this.http.get('http://' + this.globals.standardURL + '/netappserver/api/v1/monitoring/callback/');
  }
}
