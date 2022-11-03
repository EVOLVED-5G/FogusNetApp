import { Component, OnInit } from '@angular/core';
import {AbstractControl,FormBuilder, FormGroup, Validators, FormControl} from "@angular/forms";
import { AuthService } from 'src/app/services/auth.service';
import { NgModule } from '@angular/core';
import Validation from 'src/app/public/utils/validation_form';

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
  isSignUpFailed: boolean= false;
  errorMessage = '';

  constructor(private formBulder: FormBuilder, private authService: AuthService) { }

  ngOnInit(): void {
    this.form = this.formBulder.group(
      {
        first_name: ['',Validators.required],
        last_name: ['',Validators.required],
        username: ['',Validators.required],
        email: ['',[Validators.required, Validators.email,Validators.pattern("^[a-z0-9._%+-]+@[a-z0-9.-]+\\.[a-z]{2,4}$")]],
        password: ['',Validators.required, Validators.minLength(6), Validators.maxLength(40)],
        password_confirm: ['',Validators.required]
      },
      {
        validators: [Validation.match('password', 'confirmPassword')]
      });
  }

  submit(){
    const data = this.form.getRawValue();
    this.submitted = true;
    console.log(data);
    this.authService.register(data).subscribe( 
      res=>{
      // console.log(res);
      // this.isSuccessful = true;
      console.log(this.isSuccessful)
      // this.isSignUpFailed = false;
      },
      err => {
        this.errorMessage = err.error.message;
        // this.isSignUpFailed = true;
      });
  }

}
