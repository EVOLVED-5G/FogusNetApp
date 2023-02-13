import { Component, OnInit} from '@angular/core';
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
  isNullCheck: Boolean;
  isLocationReporting: Boolean;
  isUEReachability: Boolean;
  isLossOfConnectivity: Boolean;
  data_response: any;
  monitoring_type: any;
  external_id: any;
  ipv4Addr: any;
  cell_id: any;
  gNBId: any;
  hideSharedLinkCopyMessage: boolean;

  constructor(
    private formBuilder: FormBuilder,
    private monitoringSubService: MonitoringSubscriptionService
    ) {}

  ngOnInit(): void {
    this.form = this.formBuilder.group({
      callback_times: '',
      UE_selected: [null],
      MonitoringType_selected: [null],
      monitoring_type: '',
      external_id: '',
      ipv4Addr: '',
      cell_id: '',
      gNBId: ''
    });
    this.isCorrect = false;
    this.isUEReachability = false;
    this.isLossOfConnectivity = false;
    this.isLocationReporting = false;
    this.isNullCheck = false;
    this.isTime = false;
    this.UEs = UEdata.UEs;
  }

  onSelected(value:string): void {
		this.selectedUE = value;
	}

  submit() {
    const data = this.form.getRawValue()
    this.isNullCheck = false;
    if (data.callback_times == 1) {this.isTime = true}
    else {this.isTime = false}
    if (data.MonitoringType_selected == "LOCATION_REPORTING") { this.isLocationReporting = true}
    if (data.MonitoringType_selected == "UE_REACHABILITY") { this.isUEReachability = true}
    if (data.MonitoringType_selected == "LOSS_OF_CONNECTIVITY") { this.isLossOfConnectivity = true}
    console.log(data.UE_selected)
    var UE_id = new String(data.UE_selected).replace(/\D/g, "");
    // console.log(UE_id)
    // console.log(data.callback_times+'+'+data.UE_selected+'+'+data.MonitoringType_selected)
    this.monitoringSubService.create_monitoring_subscription(data.callback_times+'+'+data.UE_selected+'+'+data.MonitoringType_selected).subscribe(
      (res) => {
        if (res == "Out of range"){
          this.isNullCheck = true
          // this.FadeOutLink()
          // this.hideSharedLinkCopyMessage = true
        }
        this.data_response = JSON.parse(JSON.stringify(res))
        this.monitoring_type = this.data_response.monitoring_type
        this.external_id = this.data_response.external_id
        this.ipv4Addr = this.data_response.ipv4_addr
        if (this.isTime == true && this.isNullCheck == false){
          this.isNullCheck = false
          this.cell_id = this.data_response.location_info.cell_id
          this.gNBId = this.data_response.location_info.g_NB_Id
        }
        this.isCorrect = true
        // console.log("final",this.isNullCheck)
        // console.log("final 2",this.isNullCheck)
      },
      (error) => {
        this.isCorrect = false
      }
    )
  }
  FadeOutLink() {
    setTimeout( () => {
          this.hideSharedLinkCopyMessage = false;
        }, 2000);
   }
}
