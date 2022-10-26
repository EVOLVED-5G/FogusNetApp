import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, FormControl, Validators} from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/services/auth.service';


@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss', '../public.component.scss']
})
export class LoginComponent implements OnInit {
  form: FormGroup;
  errorMessage=false;
  formData!: FormGroup;
  isSubmitted: boolean;

  constructor(private formBuilder: FormBuilder,private authService: AuthService,private router: Router) { }

  ngOnInit(): void {
    this.form = this.formBuilder.group({
      username: '',
      password: ''
    });
  }

  submit() : void {
    const data = this.form.getRawValue()
    this.isSubmitted = true;
    if (data.username == 'admin' && data.password == 'admin'){
      console.log('success')
      // console.log('Is Login Success: ' + data);
      this.router.navigate(['/dashboard'])
    }
    else{
      console.log('failure')
      window.alert('Login failed, please try again');
      // this.formData.setErrors({ unauthenticated: true })
    }

    // this.authService.login(data).subscribe(
    //   res => {
    //     console.log(res)
    //   }
    // )
  }

}
