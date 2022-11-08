import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http'
import { environment } from '../../environments/environment';
import { Observable } from 'rxjs';

const httpOptions = {
  headers: new HttpHeaders({ 'Content-Type': 'application/json' })
};

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  constructor(private http: HttpClient) { }

  login(data:any) { 
    return this.http.post('http://localhost:8000/login/', data);
  }

  register(data:any) { 
    console.log(data);
    return this.http.post('http://localhost:8000/register/', data);
    // return this.http.post('/register', data);
    // return this.http.post('${environment.backend}/register', data);
  }

  logout(): Observable<any> {
    return this.http.post('http://localhost:8000/api-auth/logout/' + 'signout', { }, httpOptions);
  }

  user(){
    return this.http.get(environment.api + '/user', {withCredentials: true});
  }
}
