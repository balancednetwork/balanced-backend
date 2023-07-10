# Changelog

## [0.4.0](https://github.com/balancednetwork/balanced-backend/compare/v0.3.5...v0.4.0) (2023-07-10)


### Features

* add token/circulating-supply endpoints ([2db9be0](https://github.com/balancednetwork/balanced-backend/commit/2db9be075ee06d5d50acb7b7c785d2474bf7d41b))
* add tokens/prices endpoint ([43f71d7](https://github.com/balancednetwork/balanced-backend/commit/43f71d7dfb4a25d9f37698a1bf4aa411f47ad036))

## [0.3.5](https://github.com/balancednetwork/balanced-backend/compare/v0.3.4...v0.3.5) (2023-05-09)


### Bug Fixes

* switch order of series to newest to oldest ([851d726](https://github.com/balancednetwork/balanced-backend/commit/851d726fb37b280b77e8f96906993ee0f45fbadc))
* switch order of series to oldest to newest ([c13374c](https://github.com/balancednetwork/balanced-backend/commit/c13374c5ed6d0919e8ca766880b0428ba301c33b))

## [0.3.4](https://github.com/balancednetwork/balanced-backend/compare/v0.3.3...v0.3.4) (2023-05-09)


### Bug Fixes

* issue with method series not showing ([5e31d8c](https://github.com/balancednetwork/balanced-backend/commit/5e31d8c6e80a884547aeae0c8e6da9bff0a311dd))

## [0.3.3](https://github.com/balancednetwork/balanced-backend/compare/v0.3.2...v0.3.3) (2023-03-24)


### Bug Fixes

* pkeys in daily historicals deleting records ([3c6434d](https://github.com/balancednetwork/balanced-backend/commit/3c6434da750db62dbbc40d814d144b7f3d630227))

## [0.3.2](https://github.com/balancednetwork/balanced-backend/compare/v0.3.1...v0.3.2) (2023-03-22)


### Bug Fixes

* sorting of method endpoint ([56cec88](https://github.com/balancednetwork/balanced-backend/commit/56cec88807f4cb5154b950bf87507eae5e2fa257))

## [0.3.1](https://github.com/balancednetwork/balanced-backend/compare/v0.3.0...v0.3.1) (2023-03-21)


### Bug Fixes

* coingecko endpoint name: ([eae6372](https://github.com/balancednetwork/balanced-backend/commit/eae6372eb7fb456bec87811ff4e0129ed4a5d41e))

## [0.3.0](https://github.com/balancednetwork/balanced-backend/compare/v0.2.0...v0.3.0) (2023-03-20)


### Features

* add more method collectors for getTotalCollateralDebt ([62e7ca1](https://github.com/balancednetwork/balanced-backend/commit/62e7ca1fdb4686b2fd69a5852a95d89e15274775))


### Bug Fixes

* add additional where condition in method utils ([e369a0d](https://github.com/balancednetwork/balanced-backend/commit/e369a0df4d00b7abf1eeb959e404c09eef6d2680))

## [0.2.0](https://github.com/balancednetwork/balanced-backend/compare/v0.1.4...v0.2.0) (2023-03-16)


### Features

* add coingecko endpoints ([354f1ab](https://github.com/balancednetwork/balanced-backend/commit/354f1abbf9ff4550d49fed0fea99ef07f114e571))


### Bug Fixes

* decimals in contract methods cron ([04d9ba4](https://github.com/balancednetwork/balanced-backend/commit/04d9ba47a8bb6028ba58a64109e8be5ac6c86a1a))

## [0.1.4](https://github.com/balancednetwork/balanced-backend/compare/v0.1.3...v0.1.4) (2023-03-14)


### Bug Fixes

* ci issue ([8679f8b](https://github.com/balancednetwork/balanced-backend/commit/8679f8bc4fa12c4b3cf1cd7df047b3a61cd36dcc))

## [0.1.3](https://github.com/balancednetwork/balanced-backend/compare/v0.1.2...v0.1.3) (2023-03-14)


### Bug Fixes

* build ([6467cc7](https://github.com/balancednetwork/balanced-backend/commit/6467cc773d774635225a5bbee000bb15abd1e4ec))

## [0.1.2](https://github.com/balancednetwork/balanced-backend/compare/v0.1.1...v0.1.2) (2023-03-13)


### Bug Fixes

* pricing algorithm with inverse for path step ([72574a6](https://github.com/balancednetwork/balanced-backend/commit/72574a6dfde719749ab4807e0ed75a0a38711653))
* timestamp for method_addresses cron for start block init ([9436d3b](https://github.com/balancednetwork/balanced-backend/commit/9436d3bbe785a97f405f9977e644502450eba280))

## [0.1.1](https://github.com/balancednetwork/balanced-backend/compare/v0.1.0...v0.1.1) (2023-03-09)


### Bug Fixes

* ci make command: ([e1b5198](https://github.com/balancednetwork/balanced-backend/commit/e1b5198dd86ddbe98e66c06d7e8c947b154e645b))
* timestamp for initializing the method series ([a8a7f5d](https://github.com/balancednetwork/balanced-backend/commit/a8a7f5df4db47ebe0de30e9cecd52d5b19d72891))

## [0.1.0](https://github.com/balancednetwork/balanced-backend/compare/v0.0.1...v0.1.0) (2023-03-07)


### Features

* add contract method daily volumes worker ([f48b706](https://github.com/balancednetwork/balanced-backend/commit/f48b706173e6fd8e56bd55e5af9ea0555fab59cf))
* add dex adds index ([a699223](https://github.com/balancednetwork/balanced-backend/commit/a6992238e6248a75f7ede0b9f67dffdb92e84d35))
* add new volumes endpoint and add retry mechanisms along with refactor ([2765228](https://github.com/balancednetwork/balanced-backend/commit/276522858742d95ace1b9b0f1eec66afa3a57a11))
* update all the crons ([00b55b7](https://github.com/balancednetwork/balanced-backend/commit/00b55b7a80a40a4bcf6617bbe9dd4092f99790e2))
* update token pricing scheme ([685f049](https://github.com/balancednetwork/balanced-backend/commit/685f04971a9b91ae38fdb89f58b845788da548a7))


### Bug Fixes

* api prefix ([29af592](https://github.com/balancednetwork/balanced-backend/commit/29af592fea097caad3f472abfbb8dddecd405985))
* bad time conversion overflowing db int field ([9b51f5e](https://github.com/balancednetwork/balanced-backend/commit/9b51f5e8bbd323a987b2cded4dc9e2ba3c6ab7b1))
* change table name ([b7ce3a4](https://github.com/balancednetwork/balanced-backend/commit/b7ce3a42e162d9b38c2ddb762c43a09960d0419c))
* datetime type hint on api and expose api ([2e95213](https://github.com/balancednetwork/balanced-backend/commit/2e95213a1ff907c790fc86832347cdf7415cfb76))
* dividends math ([d7d1863](https://github.com/balancednetwork/balanced-backend/commit/d7d18636a34e097fd3a2664b0643d5b6f807cf74))
* don't overwrite pool data ([564e5c1](https://github.com/balancednetwork/balanced-backend/commit/564e5c19ff5497f89a9f80fc1d66737f27f1531d))
* error with timestamp unit overflowing sql column ([17e8818](https://github.com/balancednetwork/balanced-backend/commit/17e88182b044578d6e0556d48d4712361251885d))
* non-indexed lookup issue ([fbb8e78](https://github.com/balancednetwork/balanced-backend/commit/fbb8e783857205096583d2199a2487c46a3ff167))
* quote_volume_* in pools and dividends ([aa9a730](https://github.com/balancednetwork/balanced-backend/commit/aa9a7307876cbe98d8ab869c64bd86eec3dd5a3d))
* rebalance data in non indexed log ([9137f87](https://github.com/balancednetwork/balanced-backend/commit/9137f87a7ff3e3c3bfb1eb5ad5053b030cdf1005))
