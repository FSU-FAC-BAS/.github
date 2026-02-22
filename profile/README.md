<p align="center">
  <img src="https://raw.githubusercontent.com/SmartFDD/.github/main/docs/assets/fsu-facilities-logo.png" alt="FSU Facilities" width="400">
</p>

# SmartFDD

**Smart Fault Detection & Diagnostics** — Building automation intelligence for FSU Facilities.

## Our Repositories

### Core Services

| Repository | Description |
|------------|-------------|
| [fdd-common](https://github.com/SmartFDD/fdd-common) | Wrapper package for AiM, Desigo, and BAS databases |
| [DeviceExploration](https://github.com/SmartFDD/DeviceExploration) | BACnet device discovery, validation, and inventory management |
| [BacnetServices](https://github.com/SmartFDD/BacnetServices) | BACnet Services API based on bacpypes 3 |
| [connection-service](https://github.com/SmartFDD/connection-service) | Connection management service |
| [microservices](https://github.com/SmartFDD/microservices) | Essential microservices for device exploration |
| [bluemonkey](https://github.com/SmartFDD/bluemonkey) | FDD API |

### Frontend Applications

| Repository | Description |
|------------|-------------|
| [FSU-Facilties-DeviceExplorer](https://github.com/SmartFDD/FSU-Facilties-DeviceExplorer) | Next.js frontend for Building Automation Device Exploration |
| [BAS-INTERNAL-SITE](https://github.com/SmartFDD/BAS-INTERNAL-SITE) | BAS internal site |
| [bas-panel-monitoring](https://github.com/SmartFDD/bas-panel-monitoring) | BAS Facilities Manager for energy & workorder management |
| [BuildingElevationDashboard](https://github.com/SmartFDD/BuildingElevationDashboard) | Building elevation dashboard |
| [ClimateNexus](https://github.com/SmartFDD/ClimateNexus) | Climate data visualization |
| [smartfdd](https://github.com/SmartFDD/smartfdd) | Official SmartFDD app |

### Automation & Scripts

| Repository | Description |
|------------|-------------|
| [PPCL-Script-Generation](https://github.com/SmartFDD/PPCL-Script-Generation) | Automated PPCL code generation |
| [bas-automations](https://github.com/SmartFDD/bas-automations) | BAS ETL automation scripts |
| [fdd-scripting](https://github.com/SmartFDD/fdd-scripting) | FDD scripting utilities |
| [UpgradeScripts](https://github.com/SmartFDD/UpgradeScripts) | Version development tool updaters |
| [siemens_tools](https://github.com/SmartFDD/siemens_tools) | Siemens integration tools |

### Data & Analytics

| Repository | Description |
|------------|-------------|
| [bas_powerbi_dashboards](https://github.com/SmartFDD/bas_powerbi_dashboards) | BAS Team PowerBI Dashboards |
| [fdd-sustainability](https://github.com/SmartFDD/fdd-sustainability) | FSU Campus Utility Dashboard backend |
| [wifi-forecasting](https://github.com/SmartFDD/wifi-forecasting) | Occupancy estimation POC |
| [bas-ahu-rag](https://github.com/SmartFDD/bas-ahu-rag) | AHU RAG system |
| [DESIGO_SQL_SERVER](https://github.com/SmartFDD/DESIGO_SQL_SERVER) | Desigo SQL Server integration |
| [bas-utility-insights](https://github.com/SmartFDD/bas-utility-insights) | BAS utility insights |

### Integration & Configuration

| Repository | Description |
|------------|-------------|
| [FSU-Desigo-AiM](https://github.com/SmartFDD/FSU-Desigo-AiM) | Desigo-AiM API integration |
| [desigo](https://github.com/SmartFDD/desigo) | Desigo wrapper in Python |
| [aim](https://github.com/SmartFDD/aim) | AiM wrapper |
| [fdd-desigo-aim](https://github.com/SmartFDD/fdd-desigo-aim) | FDD Desigo-AiM integration |
| [WSI_SignalR_Client](https://github.com/SmartFDD/WSI_SignalR_Client) | Siemens SignalR client |
| [bas-sharepoint-test](https://github.com/SmartFDD/bas-sharepoint-test) | SharePoint integration test |

### Documentation & Onboarding

| Repository | Description |
|------------|-------------|
| [onboarding](https://github.com/SmartFDD/onboarding) | BAS Team getting started documents |
| [FSU](https://github.com/SmartFDD/FSU) | FSU resources |
| [.github](https://github.com/SmartFDD/.github) | Org-wide templates and CI workflows |

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
