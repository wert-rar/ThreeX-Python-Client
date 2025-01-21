# Changelog
>All notable changes in this project will be documented in this file.  
The format of this file is based on [Keep a Changelog](https://keepachangelog.com/)
and this project uses [Semantic Versioning](http://semver.org/).
---

## [1.2.0] - 21.01.2025

### Added
- Add `AsyncClient3XUI`.`from_env` methods realisation
- Add `AsyncClient3XUI`.`from_env` methods realisation
- Add `Documentation.md`

### Changed
- Change package name to `client3x`

## [1.1.0] - 20.01.2025

### Added
- Add `AsyncClient3XUI` methods realisation
- Add doc strings to `ClientError`
- Add `AsyncClient3XUI.start()` method

### Changed
- Update readme.md
- Update `AsyncClient3XUI` examples

### Fixed
- Delete prints in classes methods
- Fix `treex_ui_client/__init__.py` problem
- Fix `AsyncClient3XUI` cokkies update.
- Fix `Client3XUI` typo problems

--- 
## [1.0.1] - 11.01.2025

### Fixed
- Fix issue with Client3XUI
  - Fix add_client 
  - Fix update_client

---

## [1.0.0] - 08.01.2025
### Added
- Add `InboundPayload` for adding and updating inbounds
- Add `PanelResponse`
- Add `add_inbound` and `update_inbound` methods

### Changed
- Now `Client3XUI` methods return `PanelResponse` object instead of dict
some methods like `add_client` and `update_client` return sublink as sublink
- Change `Payload` class
  - Now it contains only _data_ field
  - Change how format works
- Rename `DefaultPayload` to `ClientPayload`

---

## [0.1.0] - 06.01.2025
### Added
- Add almost all API methods for Client3XUI
- Add  `__check_inbound` that checks if inbound_id is safe

--- 

## [0.0.0] - 04.01.2025
### Added
The core of the project has been added and the project structure has been created.

---




