# Changelog

## [0.6.3](https://github.com/balancednetwork/balanced-backend/compare/v0.6.2...v0.6.3) (2024-07-19)


### Bug Fixes

* add another exception handler to make sure it crashes if there is any connection issue on session creation ([7b8f5a3](https://github.com/balancednetwork/balanced-backend/commit/7b8f5a37ecd3ea63eeb7302916ee158a5cbf2209))

## [0.6.2](https://github.com/balancednetwork/balanced-backend/compare/v0.6.1...v0.6.2) (2024-07-04)


### Bug Fixes

* add better logging handler from potentially changed pools [#58](https://github.com/balancednetwork/balanced-backend/issues/58) ([746c7c3](https://github.com/balancednetwork/balanced-backend/commit/746c7c33892265d2a0c19d0d6c0f825da014315d))

## [0.6.1](https://github.com/balancednetwork/balanced-backend/compare/v0.6.0...v0.6.1) (2024-06-28)


### Bug Fixes

* add another CG hack - rm iusdc ([46c74a2](https://github.com/balancednetwork/balanced-backend/commit/46c74a2796b61d8309d148f2750c2eaab22e94ce))

## [0.6.0](https://github.com/balancednetwork/balanced-backend/compare/v0.5.5...v0.6.0) (2024-06-25)


### Features

* add icx burned series [#44](https://github.com/balancednetwork/balanced-backend/issues/44) ([c2ec78b](https://github.com/balancednetwork/balanced-backend/commit/c2ec78b92d3dafce53549eb53e52fd530c6a336e))
* add implied pool prices chart ([7a2c735](https://github.com/balancednetwork/balanced-backend/commit/7a2c735f9d2976edd21c6c0c7b1ac134705c6428))
* add new collateral tokens ([ce9bab4](https://github.com/balancednetwork/balanced-backend/commit/ce9bab4017ca8c93da213077a215f4891a25a8c4))
* add savings rate deposit series [#45](https://github.com/balancednetwork/balanced-backend/issues/45) ([10d77d1](https://github.com/balancednetwork/balanced-backend/commit/10d77d1e2490a57834ed9f7fbcfdc04bd6c41eee))
* mark tokens as stable [#47](https://github.com/balancednetwork/balanced-backend/issues/47) ([2efad23](https://github.com/balancednetwork/balanced-backend/commit/2efad23c8385fba629b56992171ae2e13c27c175))


### Bug Fixes

* add back the collateral method addresses ([1594877](https://github.com/balancednetwork/balanced-backend/commit/1594877e99a138a5cd3428484207d2409d497a9c))
* db init function ([e7d9cbe](https://github.com/balancednetwork/balanced-backend/commit/e7d9cbeb950ab69075ded4c639416e0eed9b11c0))
* enable coingecko ([69a0c33](https://github.com/balancednetwork/balanced-backend/commit/69a0c3366e538f81513de31b5bd15f6570535852))

## [0.5.5](https://github.com/balancednetwork/balanced-backend/compare/v0.5.4...v0.5.5) (2024-06-05)


### Bug Fixes

* disable coingecko altogether ([54295be](https://github.com/balancednetwork/balanced-backend/commit/54295bee6bfcf283f893d21cac56122181c9eb78))

## [0.5.4](https://github.com/balancednetwork/balanced-backend/compare/v0.5.3...v0.5.4) (2024-06-05)


### Bug Fixes

* release ([fbe404c](https://github.com/balancednetwork/balanced-backend/commit/fbe404c200bb22da6024827271f389da8708e058))

## [0.5.3](https://github.com/balancednetwork/balanced-backend/compare/v0.5.2...v0.5.3) (2024-05-26)


### Bug Fixes

* gecko hack ([a92a6a7](https://github.com/balancednetwork/balanced-backend/commit/a92a6a7910dd42d2343ed9e5a51f6e193aaf5e6f))

## [0.5.2](https://github.com/balancednetwork/balanced-backend/compare/v0.5.1...v0.5.2) (2024-05-21)


### Bug Fixes

* add better health check for cache ([d5179ce](https://github.com/balancednetwork/balanced-backend/commit/d5179ce4b6b0e58a761b830e26f656d336c3f4b0))
* bump gecko cuttoff to 1000 ([c028c31](https://github.com/balancednetwork/balanced-backend/commit/c028c31fa91042b5b2612c6cb336c366574ff780))
* make sicx the same as icx for coingecko -&gt; wtf... ([b664283](https://github.com/balancednetwork/balanced-backend/commit/b664283d243de1fa79628c847176990b24933f13))
* remove low liquidity pools from coingecko and cmc endpoints ([d3147e3](https://github.com/balancednetwork/balanced-backend/commit/d3147e38e080a64e68a0f7de63f8f1be0f24a287))
* sleep in cache for early requests ([88b3777](https://github.com/balancednetwork/balanced-backend/commit/88b3777de015108f8434a4e6cf24fa44a9691626))

## [0.5.1](https://github.com/balancednetwork/balanced-backend/compare/v0.5.0...v0.5.1) (2024-04-25)


### Bug Fixes

* deadlock issue in pools list ([d948039](https://github.com/balancednetwork/balanced-backend/commit/d9480398f115f1bc8be1fad4178eb18a3cbbba9a))
* token list source ([216c52e](https://github.com/balancednetwork/balanced-backend/commit/216c52ecb5e3bb078a1ad34176a73c7c99603632))
* token list source raw ([c3af180](https://github.com/balancednetwork/balanced-backend/commit/c3af180d73998b965643318a09e43d3811fec2e1))

## [0.5.0](https://github.com/balancednetwork/balanced-backend/compare/v0.4.0...v0.5.0) (2024-03-21)


### Features

* add stability fund time series [#34](https://github.com/balancednetwork/balanced-backend/issues/34) ([0bc4ac3](https://github.com/balancednetwork/balanced-backend/commit/0bc4ac3a76678a93508e031c44eae691e4499a10))


### Bug Fixes

* add dex swaps endpoint ([c9f8e66](https://github.com/balancednetwork/balanced-backend/commit/c9f8e66904060af8893cd5143cde43a1c3ff1138))
* add sort to endpoints limitted to 1k records which are now missing data ([714a2b5](https://github.com/balancednetwork/balanced-backend/commit/714a2b5bddfdc7985014eec4d1b40ffc62fbbc0e))
* change order of cron - stats last ([b14cd51](https://github.com/balancednetwork/balanced-backend/commit/b14cd51adb8b96d7583795fa9dd5126a5e1bec10))
* pool series mismatch [#31](https://github.com/balancednetwork/balanced-backend/issues/31) [#29](https://github.com/balancednetwork/balanced-backend/issues/29) ([571fb9b](https://github.com/balancednetwork/balanced-backend/commit/571fb9b2c379bb29a0f769048d5982f05457db09))
* rm daily historical indexes and add ellipses to pks ([86be747](https://github.com/balancednetwork/balanced-backend/commit/86be7473221752980b008d07dc795bfd20fb3b07))

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
