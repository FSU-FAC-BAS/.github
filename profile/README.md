<p align="center">
  <img src="https://raw.githubusercontent.com/FSU-FAC-BAS/.github/main/docs/assets/fsu-facilities-logo.png" alt="FSU Facilities" width="400">
</p>

# SmartFDD

**Smart Fault Detection & Diagnostics** — Building automation intelligence for FSU Facilities.

<!-- claude_bot:repos:start -->
## Our Repositories

### Core Services

| Repository | Description |
|------------|-------------|
| [BacnetServices](https://github.com/FSU-FAC-BAS/BacnetServices) | BACnet Services API based on bacpypes 3 |
| [connection-service](https://github.com/FSU-FAC-BAS/connection-service) | Connection management service |
| [fdd-common](https://github.com/FSU-FAC-BAS/fdd-common) | Wrapper package for AiM, Desigo, and BAS databases |
| [microservices](https://github.com/FSU-FAC-BAS/microservices) | Essential microservices for device exploration |

### Frontend Applications

| Repository | Description |
|------------|-------------|
| [bas-panel-monitoring](https://github.com/FSU-FAC-BAS/bas-panel-monitoring) | BAS Facilities Manager for energy & workorder management |
| [BuildingElevationDashboard](https://github.com/FSU-FAC-BAS/BuildingElevationDashboard) | Building elevation dashboard |
| [ClimateNexus](https://github.com/FSU-FAC-BAS/ClimateNexus) | Climate data visualization |

### Automation & Scripts

| Repository | Description |
|------------|-------------|
| [bas-automations](https://github.com/FSU-FAC-BAS/bas-automations) | BAS ETL automation scripts |
| [fdd-scripting](https://github.com/FSU-FAC-BAS/fdd-scripting) | FDD scripting utilities |
| [PPCL-Script-Generation](https://github.com/FSU-FAC-BAS/PPCL-Script-Generation) | Automated PPCL code generation |
| [siemens_tools](https://github.com/FSU-FAC-BAS/siemens_tools) | Siemens integration tools |
| [UpgradeScripts](https://github.com/FSU-FAC-BAS/UpgradeScripts) | Version development tool updaters |

### Data & Analytics

| Repository | Description |
|------------|-------------|
| [bas-ahu-rag](https://github.com/FSU-FAC-BAS/bas-ahu-rag) | AHU RAG system |
| [bas-utility-insights](https://github.com/FSU-FAC-BAS/bas-utility-insights) | BAS utility insights |
| [bas_powerbi_dashboards](https://github.com/FSU-FAC-BAS/bas_powerbi_dashboards) | BAS Team PowerBI Dashboards |
| [DESIGO_SQL_SERVER](https://github.com/FSU-FAC-BAS/DESIGO_SQL_SERVER) | Desigo SQL Server integration |
| [fdd-sustainability](https://github.com/FSU-FAC-BAS/fdd-sustainability) | FSU Campus Utility Dashboard backend |
| [wifi-forecasting](https://github.com/FSU-FAC-BAS/wifi-forecasting) | Occupancy estimation POC |

### Integration & Configuration

| Repository | Description |
|------------|-------------|
| [bas-sharepoint-test](https://github.com/FSU-FAC-BAS/bas-sharepoint-test) | SharePoint integration test |
| [fdd-desigo-aim](https://github.com/FSU-FAC-BAS/fdd-desigo-aim) | FDD Desigo-AiM integration |
| [WSI_SignalR_Client](https://github.com/FSU-FAC-BAS/WSI_SignalR_Client) | Siemens SignalR client |

### Documentation & Onboarding

| Repository | Description |
|------------|-------------|
| [.github](https://github.com/FSU-FAC-BAS/.github) | Org-wide templates and CI workflows |
| [FSU](https://github.com/FSU-FAC-BAS/FSU) | FSU resources |
| [onboarding](https://github.com/FSU-FAC-BAS/onboarding) | BAS Team getting started documents |

### Other

| Repository | Description |
|------------|-------------|
| [BACpypes3](https://github.com/FSU-FAC-BAS/BACpypes3) | BACnet communications library |
| [BAS-TOOL-X](https://github.com/FSU-FAC-BAS/BAS-TOOL-X) | A Python tool for automated BACnet device discovery, validation, and inventory management. It parses config files, verifies devices via Who-Is/I-Am, and stores verified data in PostgreSQL—ideal for building automation pros auditing large BACnet networks. |
| [BAS-TOOL-X-console](https://github.com/FSU-FAC-BAS/BAS-TOOL-X-console) | Next.js frontend for Building Automation Device Exploration Dashboard |
| [BuildingsWatersHead](https://github.com/FSU-FAC-BAS/BuildingsWatersHead) | FSU Facilities - Campus Water Head Explorer. Next.js hydraulic network demo with CUP at (0,0,0), four plants, and pipe diameter losses. |
| [Facilities-BAS-Website](https://github.com/FSU-FAC-BAS/Facilities-BAS-Website) | - |
| [fsu-ai-dev-skills](https://github.com/FSU-FAC-BAS/fsu-ai-dev-skills) | Claude Code skills and proxy setup for FSU Azure APIM AI gateway — access Claude and OpenAI models via subscription key |
| [notification-service](https://github.com/FSU-FAC-BAS/notification-service) | BAS notification service — events, rules, multi-channel delivery (in-app, email, Slack, Teams) |
| [TennisCourtTracks](https://github.com/FSU-FAC-BAS/TennisCourtTracks) | - |

### Archived

| Repository | Description |
|------------|-------------|
| [aim](https://github.com/FSU-FAC-BAS/aim) | AiM wrapper |
| [bluemonkey](https://github.com/FSU-FAC-BAS/bluemonkey) | FDD API |
| [desigo](https://github.com/FSU-FAC-BAS/desigo) | Desigo wrapper in Python |
| [FSU-Desigo-AiM](https://github.com/FSU-FAC-BAS/FSU-Desigo-AiM) | Desigo-AiM API integration |
| [smartfdd](https://github.com/FSU-FAC-BAS/smartfdd) | Official SmartFDD app |

<!-- claude_bot:repos:end -->

## Documentation Standards

Every repository follows a standardized documentation structure:

```
repo/
  README.md              # Project overview
  CONTRIBUTING.md        # How to contribute
  docs/
    architecture.md      # System design
    setup.md             # Installation guide
    usage.md             # Usage guide
    CHANGELOG.md         # Version history
  .github/
    workflows/
      docs-check.yml     # CI enforcement
```
