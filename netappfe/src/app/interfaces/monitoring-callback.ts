export interface LocationInfo {
    cellId: string;
    enodeBId: string;
}

export interface MonitoringCallback {
    id: number;
    externalId: string;
    locationInfo: LocationInfo;
    monitoringType: string;
    subscription: string;
    ipv4Addr: string;
}
