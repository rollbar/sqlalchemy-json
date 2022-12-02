Rollbar Info
============

As of 2022-12-02, there should be a version on our Python private registry built and ready to use:
https://console.cloud.google.com/artifacts/python/rollbar-prod/us-central1/python-private-registry/sqlalchemy-json?project=rollbar-prod

This corresponds to the commit pinned as a dependency for mox at the time of writing: `ec26812e06f7896635b4495ac3c63e197338daab`
And it's marked as `0.2.3+ec26812`.

It has been build following this procedure, which can be replicated if we ever need to switch to a more recent version or push a patch to it.
You'll need a service account that has the `roles/artifactregistry.writer`.  This is needed for Python2, as we cannot use the keyring auth provider.
With that, you can see the config needed for twine.
Execute this command:

```
gcloud artifacts print-settings python \
  --repository=python-private-registry \
  --project=rollbar-prod \
  --location=us-central1 \
  --json-key=/path/to/my-sa-key.json
```

That will produce something like this:
```
# Insert the following snippet into your .pypirc

[distutils]
index-servers =
    python-private-registry

[python-private-registry]
repository: https://us-central1-python.pkg.dev/rollbar-prod/python-private-registry/
username: _json_key_base64
password: ...

# Insert the following snippet into your pip.conf

[global]
extra-index-url = https://_json_key_base64:...@us-central1-python.pkg.dev/rollbar-prod/python-private-registry/simple/
```

We're only interested on the username and password of the registry.  Copy those somewhere.

Now:

- checkout the repo to the commit or tag you need
- modify `setup.py` to reflect the new version.  Always
  append the `+HASH` to the version in order not to conflict with upstream.
- launch a shell into a docker image with Python 2.7 support (password is the base64 string from before):
  `docker run -ti --rm -v $(pwd):/app -e TWINE_USERNAME=_json_key_base64 -e TWINE_PASSWORD=<...> cimg/python:2.7 /bin/bash`
- launch the included `./tools/build_and_publish.sh` script


