import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http'
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  constructor(private http: HttpClient) { }

  login(data: any) { 
    return this.http.post('http://localhost:8000/api/login', data);
  }

  register(data:any) { 
    return this.http.post('http://localhost:8000/api/register', data);
    // return this.http.post('/register', data);
    // return this.http.post('${environment.backend}/register', data);
  }

  user(){
    return this.http.get(environment.api + '/user', {withCredentials: true});
  }
}
