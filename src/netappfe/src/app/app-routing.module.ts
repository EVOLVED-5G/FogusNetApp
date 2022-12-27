import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './public/login/login.component';
import { PublicComponent } from './public/public.component';
import { RegisterComponent } from './public/register/register.component';
import { DashbardComponent } from './secure/dashbard/dashbard.component';
import { MonitorSubscriptionComponent } from './secure/monitor-subscription/monitor-subscription.component';
import { SecureComponent } from './secure/secure.component';
import {AuthGuard} from 'src/app/services/guarding'

const routes: Routes = [
  {
    path: '', 
    component: SecureComponent,
    canActivate:[AuthGuard],
    children: [
      {path: 'dashboard', component: DashbardComponent,canActivateChild:[AuthGuard]},
      {path: 'monitorsubscribe', component: MonitorSubscriptionComponent,canActivateChild:[AuthGuard]}
    ]
  },
  {
    path: '',
    component: PublicComponent,
    children: [
      {path: 'sign-in', component: LoginComponent},
      {path: 'sign-up', component: RegisterComponent}
    ]
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
