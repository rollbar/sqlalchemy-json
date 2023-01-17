Rollbar Info
============

As of 2022-12-02, there should be a version on our Python private registry built and ready to use:
https://pypi.rollbar.tools

This corresponds to the commit pinned as a dependency for mox at the time of writing: `ec26812e06f7896635b4495ac3c63e197338daab`
And it's marked as `0.2.3+ec26812`.

It has been build following this procedure, which can be replicated if we ever need to switch to a more recent version or push a patch to it.
You'll need the username and password of the registry's write user to publish.
The credentials are on LastPass, under the `devpi rollbar user` entry.

Export these environment variables to use with twine later:

```
export TWINE_USERNAME=rollbar
export TWINE_PASSWORD=......  # get it from LastPass
```

Now:

- checkout the repo to the commit or tag you need
- modify `setup.py` to reflect the new version.  Always
  append the `+HASH` to the version in order not to conflict with upstream.
- launch a shell into a docker image with Python 2.7 support (password is the base64 string from before):
  `docker run -ti --rm -v $(pwd):/app -e TWINE_USERNAME=$TWINE_USERNAME -e TWINE_PASSWORD=$TWINE_PASSWORD cimg/python:2.7 /bin/bash`
- launch the included `./tools/build_and_publish.sh` script


