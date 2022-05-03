import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http'

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  constructor(private http: HttpClient) { }

  // login(data: any) { 
  //   return this.http.post('http://localhost:8000/api-auth/login/', data);
  // }
}
