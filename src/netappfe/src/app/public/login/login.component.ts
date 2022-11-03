import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, FormControl } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/services/auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss', '../public.component.scss']
})
export class LoginComponent implements OnInit {

  form: FormGroup;
  isLoggedIn: boolean = false;
  isLoginFailed: boolean = false;
  errorMessage = '';
  // roles: string[] = [];

  constructor(private formBuilder: FormBuilder,private authService: AuthService,private router: Router) { }

  ngOnInit(): void {
    this.form = this.formBuilder.group({
      username: ['',Validators.required],
      password: ['',Validators.required]
    });
  }

  submit() {
    const data = this.form.getRawValue()
    this.authService.login(data).subscribe(
      res=> {
        // console.log(res);
        // this.isLoginFailed = false;
        // this.isLoggedIn = true;
        // this.roles = this.tokenStorage.getUser().roles;
        // this.reloadPage();
      },
      err => {
        this.errorMessage = err.error.message;
        this.isLoginFailed = true;
      }
    )
    if (data.username == 'admin' && data.password == 'admin'){
      console.log('success');
      this.isLoginFailed = false;
      this.isLoggedIn = true;
      this.router.navigate(['/dashboard']);
      
    }
    else{
      console.log('failure')
      this.isLoginFailed = true;
    }
  }

  reloadPage(): void {
    window.location.reload();
  }

}
