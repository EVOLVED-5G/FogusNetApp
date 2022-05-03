import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './public/login/login.component';
import { PublicComponent } from './public/public.component';
import { RegisterComponent } from './public/register/register.component';
import { DashbardComponent } from './secure/dashbard/dashbard.component';
import { MonitorSubscriptionComponent } from './secure/monitor-subscription/monitor-subscription.component';
import { SecureComponent } from './secure/secure.component';

const routes: Routes = [
  // {
  //   path: '',
  //   component: PublicComponent,
  //   children: [
  //     {path: 'login', component: LoginComponent},
  //     {path: 'register', component: RegisterComponent},
  //   ]
  // },
  {
    path: '', 
    component: SecureComponent,
    children: [
      {path: '', redirectTo: '/dashboard', pathMatch: 'full'},
      {path: 'dashboard', component: DashbardComponent},
      {path: 'monitorsubscribe', component: MonitorSubscriptionComponent}
    ]
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
