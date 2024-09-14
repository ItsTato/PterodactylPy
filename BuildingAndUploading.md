# Building for Release
Requirements
```txt
wheel
```

```console
py -3.10 setup.py sdist bdist_wheel
```

# Uploading
Requirements
```txt
twine
```

```console
twine upload dist/*

```
