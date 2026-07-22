# Publish This Project

If you want to publish your project to pypi, follow the following procedure:

## One-Time Step: Add The API Token

This API token allows a secured connection between GitHub and PyPI.
This document assumes you already created such a token from
[pypi.org](https://pypi.org).

1. In the Github project page, select *Settings*
2. From the left pane, select *Secrets and variables*
3. Select *Actions* under *Secrets and variables*
4. Under *Repository secrets*, select *New repository secret*
5. In the *New secret* page, fill in the following:
   - Name = PYPI_API_TOKEN
   - Secret = *Your token from PyPI*
6. Click *Add secret*


## Publish a Version of Your Project

Every time you reach an important milestone and wish to publish new
version, perform the following procedure:

1. Ensure that you bump up the project version from `pyproject.toml`
2. From the Github project page, select *Releases* from the right pane
3. Click *Create a new release*
4. In the New release page, fill out the fields
   - Choose a tag: I usually use versions for tags, e.g. "v1.0.0"
   - Release title: Again, I usually use the project version for this, e.g. "Version 1.0.0"
   - Write: s description of this release
   - Set as a pre-release: Select this if your release is a pre-release
   - Select *Publish release*

Once you perform the last step, the pipeline
`.github/workflows/python-publish.yaml` will start.

## Watch for Pipeline Success or Failures

From the Github project page, select *Actions* tab and watch the
new workflow to see if it succeeded or failed.

In case of success, navigate to PyPi to verify if your package has
been published.


