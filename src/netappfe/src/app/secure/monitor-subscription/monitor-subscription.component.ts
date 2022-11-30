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

  constructor(
    private formBuilder: FormBuilder,
    private monitoringSubService: MonitoringSubscriptionService
    ) {}

  ngOnInit(): void {
    this.form = this.formBuilder.group({
      callback_times: '',
      UE_selected: [null]
    });
    this.isCorrect = false
    this.UEs = UEdata.UEs
  }

  onSelected(value:string): void {
		this.selectedUE = value;
	}

  submit() {
    const data = this.form.getRawValue()
    this.monitoringSubService.create_monitoring_subscription(data.callback_times).subscribe(
      (res) => {
        console.log(res)
        this.isCorrect = true
      },
      (error) => {
        console.log(error)
        this.isCorrect = false
      }
    )
  }
}
