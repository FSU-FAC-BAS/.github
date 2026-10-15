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
| [BAS-TOOL-X](https://github.com/FSU-FAC-BAS/BAS-TOOL-X) | BACnet device discovery, validation, and inventory in PostgreSQL |
| [connection-service](https://github.com/FSU-FAC-BAS/connection-service) | Connection management service |
| [fdd-common](https://github.com/FSU-FAC-BAS/fdd-common) | Wrapper package for AiM, Desigo, and BAS databases |
| [microservices](https://github.com/FSU-FAC-BAS/microservices) | Essential microservices for device exploration |
| [notification-service](https://github.com/FSU-FAC-BAS/notification-service) | BAS notifications: events, rules, in-app, email, Slack, Teams |

### Frontend Applications

| Repository | Description |
|------------|-------------|
| [bas-panel-monitoring](https://github.com/FSU-FAC-BAS/bas-panel-monitoring) | BAS Facilities Manager for energy & workorder management |
| [BAS-TOOL-X-console](https://github.com/FSU-FAC-BAS/BAS-TOOL-X-console) | Next.js frontend for BAS-TOOL-X device exploration |
| [BuildingElevationDashboard](https://github.com/FSU-FAC-BAS/BuildingElevationDashboard) | Building elevation dashboard |
| [BuildingsWatersHead](https://github.com/FSU-FAC-BAS/BuildingsWatersHead) | Campus water head explorer with hydraulic network model |
| [ClimateNexus](https://github.com/FSU-FAC-BAS/ClimateNexus) | Climate data visualization |
| [Facilities-BAS-Website](https://github.com/FSU-FAC-BAS/Facilities-BAS-Website) | FDD internal dashboard for building automation monitoring |

### Automation & Scripts

| Repository | Description |
|------------|-------------|
| [bas-automations](https://github.com/FSU-FAC-BAS/bas-automations) | BAS ETL automation scripts |
| [fdd-scripting](https://github.com/FSU-FAC-BAS/fdd-scripting) | FDD scripting utilities |
| [fsu-ai-dev-skills](https://github.com/FSU-FAC-BAS/fsu-ai-dev-skills) | Claude Code skills and proxies for the FSU AI gateway |
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
| [TennisCourtTracks](https://github.com/FSU-FAC-BAS/TennisCourtTracks) | Camera-based tennis court occupancy detection |
| [wifi-forecasting](https://github.com/FSU-FAC-BAS/wifi-forecasting) | Occupancy estimation POC |

### Integration & Configuration

| Repository | Description |
|------------|-------------|
| [BACpypes3](https://github.com/FSU-FAC-BAS/BACpypes3) | BACnet communications library (fork of BACpypes3) |
| [bas-sharepoint-test](https://github.com/FSU-FAC-BAS/bas-sharepoint-test) | SharePoint integration test |
| [fdd-desigo-aim](https://github.com/FSU-FAC-BAS/fdd-desigo-aim) | FDD Desigo-AiM integration |
| [WSI_SignalR_Client](https://github.com/FSU-FAC-BAS/WSI_SignalR_Client) | Siemens SignalR client |

### Documentation & Onboarding

| Repository | Description |
|------------|-------------|
| [.github](https://github.com/FSU-FAC-BAS/.github) | Org-wide templates and CI workflows |
| [FSU](https://github.com/FSU-FAC-BAS/FSU) | FSU resources |
| [onboarding](https://github.com/FSU-FAC-BAS/onboarding) | BAS Team getting started documents |

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
