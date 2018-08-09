# Changelog

## [Unreleased]

#### Changes from the previous release: ([diff](https://github.com/alphatwirl/alphatwirl/compare/v0.19.0...master))
- added `collect()` to `AllwCount`, `AnywCount`, `NotwCount`
  [\#33](https://github.com/alphatwirl/alphatwirl/issues/33)
- `mkdir_p()` checks if `path` is empty
- added unittest for `mkdir_p()`
- avoided mutable default of `ReaderComposite`, `AllwCount`,
  `AnywCount`.
- added a decorator `_removed()`

## [0.19.0] - 2018-08-08

**PyPI**: https://pypi.org/project/alphatwirl/0.19.0/

#### Changes from the previous release: ([diff](https://github.com/alphatwirl/alphatwirl/compare/v0.18.8...v0.19.0))
- removed deprecated sub-packages: `cmsedm`, `delphes`, `heppyresult`.
    - the contents of these packages can be found, respectively, in
      the following repositories:
        - https://github.com/alphatwirl/atcmsedm
        - https://github.com/alphatwirl/atdelphes
        - https://github.com/alphatwirl/atheppy

## [0.18.8] - 2018-08-08

**PyPI**: https://pypi.org/project/alphatwirl/0.18.8/

#### Changes from the previous release: ([diff](https://github.com/alphatwirl/alphatwirl/compare/v0.18.7...v0.18.8))
- fixed an import error at rtd

## [0.18.7] - 2018-08-07

**PyPI**: https://pypi.org/project/alphatwirl/0.18.7/

#### Changes from the previous release: ([diff](https://github.com/alphatwirl/alphatwirl/compare/v0.18.6...v0.18.7))
- changed behavior of `RoundLog`
    - returns the underflow bin for `0` and negative values if `min`
      is given. (previously, returns `0` for `0` and `None` for a
      negative number even when `min` is given)
    - returns the overflow bin for `inf` if `max` is given.
      (previously, returns `None` for `inf` even when `max` is given)
- optimized `RoundLog` and `Round` for speed, e.g., replacing linear
  search with binary search
- updated zenodo badge, using all-versions badge
- organized requirements [\#35](https://github.com/alphatwirl/alphatwirl/issues/35)
    - requirements/doc.txt for sphinx doc, used at Read the Docs
    - requirements/test.txt for test, used at travis-ci
- added CHANGELOG.md

## [0.18.6] - 2018-08-05

**PyPI**: https://pypi.org/project/alphatwirl/0.18.6/

#### Changes from the previous release: ([diff](https://github.com/alphatwirl/alphatwirl/compare/v0.18.5...v0.18.6))
- fixed Read The Docs. [\#47](https://github.com/alphatwirl/alphatwirl/issues/40)
- updated README.md
- updated travis-ci config
- updated unittests
