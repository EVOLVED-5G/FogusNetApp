# FOGUS-Evolved-NetApp

## Install NEF Emulator

Follow the instructions at:
https://github.com/EVOLVED-5G/NEF_emulator

## Install jq (optional)

```bash
sudo apt install -y jq
```

## Create properties file
Create a file named **_db_template.properties_** inside "evolvedfg" folder, with format:
```properties
# Database Configuration
[nef]
nef_user=<NEF host username>
nef_pass=<NEF host password>
emulator=<NEF hostname or IP>
em_port=<NEF backend port>

[vapp]
vapp_server=<VApp REST endpoint IP>
vapp_port=<VApp REST endpoint Port>

[callback]
cb_server=<Callback server hostname or IP>
cb_port=<Callback server port>
```

## Deploy the NetApp
```bash
cd FOGUS-Evolved-NetApp

# Build and deploy containers
./run.sh

# Print container logs
./logs.sh

# Stop containers
./stop.sh

# Stop and remove containers
./cleanup_docker_containers.sh
```

## Architecture

| Container             | Folder                | Description                                      |
|-----------------------|-----------------------|--------------------------------------------------|
| nefdjango             | evolvedfg             | Backend of NetApp                                |
| netappfe              | netappfe              | Frontend of NetApp                               |
| nefpostgres           | -                     | DB to store info exchanged with NEF              |


## Access NetApp
### In your browser, access the following url
```
http://localhost:4200/
```


## Use curl
### Populate cells from NEF Emulator
```
curl --location --request GET 'http://<HOST IP>:8000/netappserver/api/v1/cells/update/' | jq
```
### Make an one-time subscription to Monitoring Event API of NEF Emulator
```
curl --location --request GET http://<HOST IP>:8000/netappserver/api/v1/monitoring/subscribe/1/  | jq
```
### Make a multiple-times subscription to Monitoring Event API of NEF Emulator
```
curl --location --request GET http://<HOST IP>:8000/netappserver/api/v1/monitoring/subscribe/<times>/  | jq
```

## Monitoring Event Callback
### Example of MonitoringEventReport
```json
{
  "externalId": "123456789@domain.com",
  "monitoringType": "LOCATION_REPORTING",
  "locationInfo": {
    "cellId": "string",
    "enodeBId": "string"
  },
  "ipv4Addr": "string"
}
```

## Analytics Exposure Callback
### Example of AnalyticsEventNotification (for Abnormal Behaviour)
```json
{
  "notifId": "notif1",
  "analyEventNotifs": [
    {
      "analyEvent": "ABNORMAL_BEHAVIOR",
      "expiry": "2021-11-26T09:21:04.481Z",
      "timeStamp": "2021-11-26T09:21:04.481Z",
      "abnormalInfos": [
        {
          "gpsis": [
            "string"
          ],
          "appId": "string",
          "excep": {
            "excepId": "SUSPICION_OF_DDOS_ATTACK",
            "excepLevel": 0,
            "excepTrend": "UP"
          },
          "ratio": 100,
          "confidence": 0,
          "addtMeasInfo": {
            "ddosAttack": {
              "ipv4Addrs": [
                "198.51.100.1"
              ]
            }
          }
        }
      ]
    }
  ]
}
```

### Exceptions ('excep' field) for Abnormal Behaviour
| excepId  | Description |
| ------------- | ------------- |
| UNEXPECTED_UE_LOCATION  | Unexpected UE location  |
| UNEXPECTED_LONG_LIVE_FLOW  | Unexpected long-live rate flows  |
| UNEXPECTED_LARGE_RATE_FLOW | Unexpected large rate flows  |
| UNEXPECTED_WAKEUP  | Unexpected wakeup  |
| SUSPICION_OF_DDOS_ATTACK  | Suspicion of DDoS attack  |
| WRONG_DESTINATION_ADDRESS  | Wrong destination address  |
| TOO_FREQUENT_SERVICE_ACCESS  | Too frequent Service Access  |
| UNEXPECTED_RADIO_LINK_FAILURES  | Unexpected radio link failures  |
| PING_PONG_ACROSS_CELLS  | Ping-ponging across neighbouring cells  |