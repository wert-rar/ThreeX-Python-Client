# Changelog
All notable changes in this project will be documented in this file.  
The format of this file is based on [Keep a Changelog](https://keepachangelog.com/)
and this project uses [Semantic Versioning](http://semver.org/).

## [0.0.0] - 04.01.2025
### Added
The core of the project has been added and the project structure has been created.

## [0.1.0] - 06.01.2025
### Added
- Add almost all API methods for Client3XUI
- Add  `__check_inbound` that checks if inbound_id is safe

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

## [1.0.1] - 11.01.2025

### Fixed
- Fix issue with Client3XUI
  - Fix add_client 
  - Fix update_client




