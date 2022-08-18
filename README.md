
# Ansible Role:  `thanos` 

Ansible role to install and configure [thanos](https://github.com/thanos-io/thanos).

[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/bodsch/ansible-thanos/CI)][ci]
[![GitHub issues](https://img.shields.io/github/issues/bodsch/ansible-thanos)][issues]
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/bodsch/ansible-thanos)][releases]

[ci]: https://github.com/bodsch/ansible-thanos/actions
[issues]: https://github.com/bodsch/ansible-thanos/issues?q=is%3Aopen+is%3Aissue
[releases]: https://github.com/bodsch/ansible-thanos/releases


If `latest` is set for `thanos_version`, the role tries to install the latest release version.  
**Please use this with caution, as incompatibilities between releases may occur!**

The binaries are installed below `/usr/local/bin/thanos/${thanos_version}` and later linked to `/usr/bin`. 
This should make it possible to downgrade relatively safely.

The Thanos archive is stored on the Ansible controller, unpacked and then the binaries are copied to the target system.
The cache directory can be defined via the environment variable `CUSTOM_LOCAL_TMP_DIRECTORY`. 
By default it is `${HOME}/.cache/ansible/thanos`.
If this type of installation is not desired, the download can take place directly on the target system. 
However, this must be explicitly activated by setting `thanos_direct_download` to `true`.


## Operating systems

Tested on

* Arch Linux
* Debian based
    - Debian 10 / 11
    - Ubuntu 20.10


## Contribution

Please read [Contribution](CONTRIBUTING.md)

## Development,  Branches (Git Tags)

The `master` Branch is my *Working Horse* includes the "latest, hot shit" and can be complete broken!

If you want to use something stable, please use a [Tagged Version](https://github.com/bodsch/ansible-thanos/tags)!

## Configuration

```yaml

```

---

## Author and License

- Bodo Schulz

## License

[Apache](LICENSE)

`FREE SOFTWARE, HELL YEAH!`
