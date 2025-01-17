<!-- markdownlint-configure-file { "MD024": { "siblings_only": true } } -->
# Changelog

(versions follow [Semantic Versioning v2.0.0](https://semver.org/spec/v2.0.0.html))

## [1.1.0] (2023-11-04)

This release adds a few small changes to the API and cleans up the documentation of the project.

### Additions

- Clients now support a `host` parameter allowing users to provide an alternative host compatible with the APIs.
- Created a new `PYPI_HOST` constant.
- Added `DistributionFile.core_metadata` (PEP 714).

### Deprecations

- `JSON_URL`, `STATS_URL`, and `SIMPLE_URL`: These constants are no longer used by pypiwrap.
- `Project.bugtrack_url`: This is no longer reported by the API and always returns None. Users may consult for bugtracking URLs in `Project.project_urls`.
- `ReleaseFile.has_sig`: This is no longer reported by the API and always returns None. Users should simply add `.asc` at the end of `ReleaseFile.url` and perform a GET request.

### Fixes

- Addressed datetime conversion error for `upload_time` values not containing a microsecond component.

## [1.0.0] (2023-05-19)

This is the first major release :tada:. It adds some notable changes to the structure of the project.

### Additions

- Added `PyPIClient` (for the JSON and Stats API) and `SimpleClient` (for the Simple API) as replacements for `Client`.
  - `Client.get_project` -> `PyPIClient.get_project`
  - `Client.get_stats` -> `PyPIClient.get_stats`
  - `Client.get_all_projects` -> `SimpleClient.get_index`
  - `Client.get_files` -> `SimpleClient.get_page`
- Clients can now be used as context managers (`with` statement).
- Clients now report an appropriate user agent.
- Added `exceptions.raise_for_status` as a replacement for `exceptions.error_from_response`.
- Added `Vulnerability.withdrawn` attribute.
- Added `DistributionFile.size` and `DistributionFile.upload_time` (PEP 700).
- Added `ProjectPage` (PEP 700).
- Added some documentation to the utilities.

### Changes

- Renamed `Base` to `APIObject`
- Renamed `Size.from_bytes` to `Size.from_int` to avoid confusion with the builtin `bytes`.
- `Stats.top_packages` is now sorted by size.

### Removals

- `Client`: Its functionality has been split into `PyPIClient` and `SimpleClient`.
- `exceptions.error_from_response`: Now replaced by `exceptions.raise_for_status`.

## [0.3.0] (2022-11-01)

This release focuses on fixes and improvements to the pypiwrap package. This release can be considered stable.

### Additions

- Added representation (`__repr__`) to `Stats`.
- Added `utils.gpg_from_url`.

### Changes

- The following have been renamed to better align with the API's structure and terminology:
  - `PyPiClient` -> `Client`.
  - `Package` -> `Project`.
  - `ReleaseURL` -> `ReleaseFile`.
  - `PackageFile` -> `DistributionFile`.
  - `Client.get_package` -> `Client.get_project`.
  - `ReleaseFile.packagetype` -> `ReleaseFile.package_type`.
  - `DistributionFile.gpg_sig` -> `DistributionFile.has_sig` (to better align with `ReleaseFile.has_sig`).
- Updated docs for `ReleaseFile.python_version` to be clearer (along with other members).
- Migrated exceptions to a separate module (`exceptions`).

### Removals

- `ReleaseFile.md5_digest`: If needed, fetch from `ReleaseFile.digests` instead.

### Fixes

- Fixed incorrect type hint of `Project.requires_dist`.
- Fixed incorrect SI step size for `utils.bytes_to_readable`. Older versions used 1024 rather than the correct one (1000) as the step size for SI
- Fixed typos in documentation.

## [0.2.0] (2022-09-11)

This is a complete rewrite of the original project, designed with a more Pythonic approach and a simpler API.

### Additions

- Added `PyPiClient` as a replacement for the other API classes.
- Added the data classes `Base`, `Package`, `ReleaseURL`, `Vulnerability`, and `PackageFile`.
- Added the `NotFound` exception as a replacement for `PackageNotFound` and `VersionNotFound`.
- Added the `ClientError` exception.
- Added `utils.Size` for representing human-readable sizes.
- Added `utils.iso_to_datetime` for converting ISO 8601 strings to date times.
- Added `utils.remove_additional` for discarding unneeded fields.
- Added `Client.get_all_projects` and `Client.get_files` from the Simple API.

### Changes

- Switched to `setup.cfg` for package information.

### Removals

- Removed `MainAPI`. Users should use `PyPiClient` instead.
- Removed `PackageInfo` and `ReleaseInfo`. They have been merged into `PyPiClient` as `PyPiClient.get_package`.
- Removed `Statistics` and `TopPackage` in favor of a single `Stats` model.
- Removed `PackageNotFound` and `VersionNotFound` in favor of the new `NotFound` exception.

## [0.1.0] (2021-03-13)

This is the first release of `pypiwrap`. :tada:

[1.1.0]: https://github.com/aescarias/pypiwrap/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/aescarias/pypiwrap/compare/0.3.0...v1.0.0
[0.3.0]: https://github.com/aescarias/pypiwrap/compare/0.2.0...0.3.0
[0.2.0]: https://github.com/aescarias/pypiwrap/compare/0.1.0...0.2.0
[0.1.0]: https://github.com/aescarias/pypiwrap/releases/tag/0.1.0
