import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { MonitoringSubscriptionService } from 'src/app/services/monitoring-subscription.service';
import UEdata from '../../../assets/scenario.json' 

@Component({
  selector: 'app-monitor-subscription',
  templateUrl: './monitor-subscription.component.html',
  styleUrls: ['./monitor-subscription.component.scss']
})

export class MonitorSubscriptionComponent implements OnInit {

  form: FormGroup;
  isCorrect: boolean;
  UEs : any;
  selectedUE: any;
  dataJson: any;
  isTime: Boolean;
  isLocationReporting: Boolean;
  isUEReachability: Boolean;
  isLossOfConnectivity: Boolean;
  data_response: any;

  constructor(
    private formBuilder: FormBuilder,
    private monitoringSubService: MonitoringSubscriptionService
    ) {}

  ngOnInit(): void {
    this.form = this.formBuilder.group({
      callback_times: '',
      UE_selected: [null],
      MonitoringType_selected: [null]
    });
    this.isCorrect = false
    this.isUEReachability = false;
    this.isLossOfConnectivity = false;
    this.isLocationReporting = false;
    this.UEs = UEdata.UEs
  }

  onSelected(value:string): void {
		this.selectedUE = value;
	}

  submit() {
    const data = this.form.getRawValue()
    if (data.callback_times == 1) {this.isTime = true}
    else {this.isTime = false}
    if (data.MonitoringType_selected == "LOCATION_REPORTING") { this.isLocationReporting = true}
    if (data.MonitoringType_selected == "UE_REACHABILITY") { this.isUEReachability = true}
    if (data.MonitoringType_selected == "LOSS_OF_CONNECTIVITY") { this.isLossOfConnectivity = true}
    this.monitoringSubService.create_monitoring_subscription(data.callback_times+'+'+data.UE_selected+'+'+data.MonitoringType_selected).subscribe(
      (res) => {
        console.log(res)
        this.data_response = JSON.stringify(res)
        this.isCorrect = true
      },
      (error) => {
        this.isCorrect = false
      }
    )
  }

}
