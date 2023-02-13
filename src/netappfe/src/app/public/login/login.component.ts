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
  data: any;

  constructor(private formBuilder: FormBuilder,private authService: AuthService,
    private router: Router) { }

  ngOnInit(): void {
    this.form = this.formBuilder.group({
      email: ['',Validators.required],
      password: ['',Validators.required]
    });
  }

  submit() : void {
    const data = this.form.getRawValue()
    if (this.form.invalid) {
      console.log(this.form.errors);
    } else {
        this.authService.login(data).subscribe({
          next: (data: any) => {
            if (localStorage.getItem('data') !== JSON.stringify(data)) {
              localStorage.setItem('data', JSON.stringify(data));
            }
            this.isLoginFailed = false;
            this.isLoggedIn = true;
            this.router.navigate(['/dashboard']);
          },
          error: (error: any) => {
            this.isLoginFailed = true;
            setTimeout(() => {
              this.reloadPage();
            }, 2000);
          }
        }
      );
    }
  }

  reloadPage(): void {
    window.location.reload();
  }

}
