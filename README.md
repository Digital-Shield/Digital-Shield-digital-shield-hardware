<p align="center">
<img width="200" src="https://github.com/ziancube/digitshield-touch-firmware/blob/touch/core/src/trezor/res/logo.png"/>
</p>

---

[![Github Stars](https://img.shields.io/github/stars/ziancube/digitshield-touch-firmware?t&logo=github&style=for-the-badge&labelColor=000)](https://github.com/ziancube/digitshield-touch-firmware/stargazers)
[![Version](https://img.shields.io/github/release/ziancube/digitshield-touch-firmware.svg?style=for-the-badge&labelColor=000)](https://github.com/ziancube/digitshield-touch-firmware/releases)
[![](https://img.shields.io/github/contributors-anon/ziancube/digitshield-touch-firmware?style=for-the-badge&labelColor=000)](https://github.com/ziancube/digitshield-touch-firmware/graphs/contributors)
[![Last commit](https://img.shields.io/github/last-commit/ziancube/digitshield-touch-firmware.svg?style=for-the-badge&labelColor=000)](https://github.com/ziancube/digitshield-touch-firmware/commits/DigitShield)
[![Issues](https://img.shields.io/github/issues-raw/ziancube/digitshield-touch-firmware.svg?style=for-the-badge&labelColor=000)](https://github.com/ziancube/digitshield-touch-firmware/issues?q=is%3Aissue+is%3Aopen)
[![Pull Requests](https://img.shields.io/github/issues-pr-raw/ziancube/digitshield-touch-firmware.svg?style=for-the-badge&labelColor=000)](https://github.com/ziancube/digitshield-touch-firmware/pulls?q=is%3Apr+is%3Aopen)
[![Discord](https://img.shields.io/discord/868309113942196295?style=for-the-badge&labelColor=000)](https://discord.gg/DigitShield)
[![Twitter Follow](https://img.shields.io/twitter/follow/ziancube?style=for-the-badge&labelColor=000)](https://twitter.com/ziancube)


## Community & Support

- [Community Forum](https://github.com/orgs/ziancube/discussions). Best for: help with building, discussion about best practices.
- [GitHub Issues](https://github.com/ziancube/digitshield-touch-firmware/issues). Best for: bugs and errors you encounter using DigitShield.
- [Discord](https://discord.gg/DigitShield). Best for: sharing your ideas and hanging out with the community.


## 🚀 Getting Onboard

1. Install [nix](https://nixos.org/download.html)
2. Pulling the latest code via the git command line tool,  setting up the development environment

```
  git clone --recurse-submodules https://github.com/ziancube/digitshield-touch-firmware.git
  cd digitshield-touch-firmware
  nix-shell
  poetry install
```

3. Run the build with:

```
   cd core && poetry run make build_unix
```

4. Now you can start the emulator

```
   poetry run ./emu.py
```

5. You can now install the command line client utility to interact with the emulator

```
   cd python && poetry run python3 -m pip install .
```

## ✏ Contribute

- Adding a small feature or a fix

  If your change is somewhat subtle, feel free to file a PR in one of the appropriate repositories directly. See the PR requirements noted at [CONTRIBUTING.md](docs/misc/contributing.md)

- Add new coin/token/network to the official DigitShield firmware

  See [COINS.md](docs/misc/COINS.md)

Also please have a look at the [docs](docs/SUMMARY.md) before contributing. The misc chapter should be read in particular because it contains some useful assorted knowledge.

## 🔒 Security

- Please read [Bug Bunty Rules](https://github.com/ziancube/app-monorepo/blob/DigitShield/docs/BUG_RULES.md), we have detailed the exact plan in this article.
- Please report suspected security vulnerabilities in private to dev@DigitShield.so
- Please do NOT create publicly viewable issues for suspected security vulnerabilities.
- As an open source project, although we are not yet profitable, we try to give some rewards to white hat hackers who disclose vulnerabilities to us in a timely manner.

## ✨ Salute!

[![](https://img.shields.io/github/contributors-anon/ziancube/digitshield-touch-firmware?style=for-the-badge&labelColor=000)](https://github.com/ziancube/digitshield-touch-firmware/graphs/contributors)

<a href="https://github.com/ziancube/digitshield-touch-firmware/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=ziancube/digitshield-touch-firmware&max=240&columns=24"/>
</a>
