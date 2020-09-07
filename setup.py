#!/usr/bin/env python
import setuptools

setuptools.setup(use_scm_version={
    "write_to": "mypackage/version.py",
    "version_scheme": "release-branch-semver"
})
