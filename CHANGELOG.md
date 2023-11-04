# Changelog

A complete changelog for the `pypiwrap` project.

## 1.1.0 (4-11-2023)

This release adds a few small changes to the API and cleans up the documentation of the project.

Client:

- Clients now support a new `host` parameter so a user can provide a different host than the default.
- Added a new `PYPI_HOST` constant.
  - With this change, the `JSON_URL`, `STATS_URL`, and `SIMPLE_URL` constants have been marked for potential deprecation and are no longer used within the package.

Objects:

- Deprecated `Project.bugtrack_url` and `ReleaseFile.has_sig`
- Added `DistributionFile.core_metadata` (PEP 714)
- Addressed datetime conversion error for `upload_time` values not containing an microsecond component.

## 1.0.0 (19-5-2023)

This is the first major release :tada:. It adds some notable changes to the structure of the project.

Client:

- `Client`'s functionality has been split into two new classes:
  - `PyPIClient`: The JSON and Stats API
    - `Client.get_project` -> `PyPIClient.get_project`
    - `Client.get_stats` -> `PyPIClient.get_stats`
  - `SimpleClient`: The Simple API
    - `Client.get_all_projects` -> `SimpleClient.get_index`
    - `Client.get_files` -> `SimpleClient.get_page`
- Clients can now be used as context managers (`with`)
- Clients now report an user agent

Objects:

Objects have also been split into two modules:  `pypi` and `simple`. The base class has also been moved to a separate `base` module.

- Renamed `Base` to `APIObject`
- Added `Vulnerability.withdrawn`
- `Stats.top_packages` is now sorted by size
- Added `DistributionFile.size` and `DistributionFile.upload_time` (PEP 700)
- Added `ProjectPage` (PEP 700)

Other Changes:

- Added some documentation to the utilities
- `exceptions.error_from_response` was rewritten into `exceptions.raise_for_status`
- Renamed `Size.from_bytes` to `Size.from_int` (to avoid confusion with the builtin)

## 0.3.0 (1-11-2022)

This release focuses on fixes and improvements to the pypiwrap package. It can be considered stable.

To better align with the API's structure/terminology:

- Renamed `PyPiClient` to `Client`
- Renamed `Package` to `Project`
- Renamed `ReleaseURL` to `ReleaseFile`
- Renamed `PackageFile` to `DistributionFile`
- Renamed `Client.get_package` to `Client.get_project`
- Renamed `ReleaseFile.packagetype` to `ReleaseFile.package_type`
- Renamed `DistributionFile.gpg_sig` to `DistributionFile.has_sig` (to better align with `ReleaseFile.has_sig`)
- Removed `ReleaseFile.md5_digest` (if needed, fetch from `ReleaseFile.digests` instead)

Bug Fixes:

- Fixed incorrect type hint of `Project.requires_dist`
- Fixed incorrect SI step size for `utils.bytes_to_readable`
  - Older versions used 1024 rather than the correct one (1000) as the step size for SI

Other changes:

- Migrated exceptions to a separate module (`exceptions`)
- Added representation (`__repr__`) to `Stats`
- Added `utils.gpg_from_url`
- Updated docs for `ReleaseFile.python_version` to be clearer (along with other members)
- Fixed typos in documentation

## 0.2.0 (11-9-2022)

This is a complete rewrite of the original project designed with a more Pythonic approach and a simpler API.

Client:

- Removed `MainAPI` in favor of `PyPiClient`
- Removed `PackageInfo` and `ReleaseInfo`. Their functionalities have been merged into `PyPiClient`. (`Client.get_package`)
- Added `Client.get_stats`. This also removes the `Statistics` and `TopPackage` models, in favor of a single `Stats` model.
- Added `Client.get_all_projects` and `Client.get_files` from the Simple API.

Objects:

- Added data classes `Base`, `Package`, `ReleaseURL`, `Vulnerability`, and `PackageFile`.

Utils:

- Added `Size` to represent human-readable sizes.
- Added `iso_to_datetime` and `remove_additional`.

Other Changes:

- Moved package information from `setup.py` to `setup.cfg`
- Merged `PackageNotFound` and `VersionNotFound` into a single exception `NotFound`.
- Added a general exception: `ClientError`.

## 0.1.0 (13-3-2021)

This is the first release of `pypiwrap`. :tada:
