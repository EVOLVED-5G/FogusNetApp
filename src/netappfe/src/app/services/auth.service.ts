import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http'
import { environment } from '../../environments/environment';
import {UserService} from "src/app/services/user.service";
import { Observable } from 'rxjs';

const httpOptions = {
  headers: new HttpHeaders({ 'Content-Type': 'application/json' })
};

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  constructor(private http: HttpClient, private userService: UserService) { }

  login(data:any){
    this.userService.loggedIn = true;
    return this.http.post('http://' + environment.backend + '/api/login/', data) ;
  }

  register(data:any) {
    return this.http.post('http://' + environment.backend + '/api/register/', data);
  }

  logout(): Observable<any> {
    return this.http.post('http://' + environment.backend + '/api-auth/logout/' + 'signout', { }, httpOptions);
  }
}
