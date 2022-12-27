import { Component, OnInit } from '@angular/core';
import {AbstractControl,FormBuilder, FormGroup, Validators, FormControl} from "@angular/forms";
import { AuthService } from 'src/app/services/auth.service';
import Validation from 'src/app/public/utils/validation_form';
import { Router } from '@angular/router';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss', '../public.component.scss']
})
export class RegisterComponent implements OnInit {
  form: FormGroup = new FormGroup({
    first_name: new FormControl(''),
    last_name : new FormControl(''),
    username: new FormControl(''),
    email: new FormControl(''),
    password: new FormControl(''),
    password_confirm: new FormControl('')
  })

  submitted: boolean = false;
  isSuccessful: boolean = false;
  isSignUpFailed: boolean = false;
  isUsername: boolean = false;
  isEmail: boolean = false;
  errorMessage = '';

  constructor(private formBulder: FormBuilder, private authService: AuthService, private router: Router) { }

  ngOnInit(): void {
    this.form = this.formBulder.group(
      {
        first_name: ['',Validators.required],
        last_name: ['',Validators.required],
        username: ['',Validators.required],
        email: ['',[Validators.required, Validators.email,Validators.pattern("^[a-z0-9._%+-]+@[a-z0-9.-]+\\.[a-z]{2,4}$")]],
        password: ['',Validators.required, Validators.minLength(8), Validators.maxLength(40)],
        password_confirm: ['',Validators.required, Validators.minLength(8), Validators.maxLength(40)]
      },
      {
        validators: [Validation.match('password', 'password_confirm')]
      });
  }

  submit(){
    const data = this.form.getRawValue();
    this.submitted = true;
    this.authService.register(data).subscribe({
      next: (res: any) =>{
      this.isSuccessful = true;
      this.isSignUpFailed = false;
      setTimeout(() => {
        this.router.navigate(['/sign-in']);
      }, 4000);
      },
      error: (err:any) => {
        console.log(err)
        if ( err.error.user.username == "user with this username already exists.") {this.isUsername = true}
        if (err.error.user.email == "user with this email already exists.") {this.isEmail = true}
        err.error.user.username
        this.errorMessage = err.error.message;
        this.isSignUpFailed = true;
      }
      });
  }
}
