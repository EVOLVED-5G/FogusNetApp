import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SecureComponent } from './secure.component';
import { MonitoringCallbacksComponent } from './monitoring-callbacks/monitoring-callbacks.component';
import { MenuComponent } from './menu/menu.component';
import { DashbardComponent } from './dashbard/dashbard.component';
import { MonitorSubscriptionComponent } from './monitor-subscription/monitor-subscription.component';
import { RouterModule } from '@angular/router';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';



@NgModule({
  declarations: [
    SecureComponent,
    MonitoringCallbacksComponent,
    MenuComponent,
    DashbardComponent,
    MonitorSubscriptionComponent
  ],
  exports: [
    SecureComponent
  ],
  imports: [
    CommonModule,
    RouterModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
  ]
})
export class SecureModule { }
