# Changelog (WIP)

A complete changelog for each release in `pypiwrap`.

## 0.1.0

The first version of `pypiwrap`.

## 0.2.0

A complete rewrite of the original `pypiwrap` project. (WIP)

## 0.3.0

This release focuses on fixes and improvements to the pypiwrap package.

To better align with the API's structure/terminology:

- Renamed `PyPiClient` to `Client`
- Renamed `Package` to `Project`
- Renamed `ReleaseURL` to `ReleaseFile`
- Renamed `PackageFile` to `DistributionFile`
- Renamed `Client.get_package` to `Client.get_project`

To make the project less ambiguous:

- Removed `ReleaseFile.md5_digest` (if needed, fetch from `ReleaseFile.digests` instead)
- Renamed `ReleaseFile.packagetype` to `ReleaseFile.package_type`
- Renamed `DistributionFile.gpg_sig` to `DistributionFile.has_sig` (to better align with `ReleaseFile.has_sig`)

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
