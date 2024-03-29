# FOGUS-Evolved-NetworkApp

## Install NEF Emulator

Follow the instructions at:
https://github.com/EVOLVED-5G/NEF_emulator

## Install Docker

Follow the instructions at:
https://docs.docker.com/get-docker/

## Install Make

Follow the instructions at:
https://www.gnu.org/software/make/

## Install jq (optional)

```bash
sudo apt install -y jq
```

## Configure environmental variables 
Edit [env_to_copy.dev](./env_to_copy.dev)

## Deploy the NetworkApp
```bash
git clone https://github.com/EVOLVED-5G/FogusNetApp
cd FogusNetApp

# Build and deploy containers
make run

# Stop containers
make stop

# Stop and remove containers
make clean
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
