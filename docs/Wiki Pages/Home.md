Welcome to the python-mlb-statsapi wiki!

# [Python MLB Stats API - Unofficial MLB Stats API](..)

### The unofficial python wrapper for the MLB Stats API

*Python-mlb-statsapi* is an unofficial python wrapper for the MLB Stats API written in python 3.7+ and provides developers access to the MLB Stats API endpoint, created and maintained by [Kristian Nilssen](https://github.com/KCNilssen) and [Matthew Spah](https://github.com/Mattsface).

Get started at [https://github.com/zero-sum-seattle/python-mlb-statsapi](https://github.com/zero-sum-seattle/python-mlb-statsapi)!

*This is an educational project so no commercial use.*

## Copyright Notice
* This package and its authors are not affiliated with MLB or any MLB team. This API wrapper interfaces with MLB's Stats API. Use of MLB data is subject to the notice posted at http://gdx.mlb.com/components/copyright.txt.

## License
* The Python MLB Stats API is licensed under the MIT License
  * https://opensource.org/licenses/MIT 

## Contributing
Please read through our [contributing guidelines](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/CONTRIBUTING.md). Included are directions for opening issues, coding standards, and notes on development.

## Versioning
Font Awesome will be maintained under the Semantic Versioning guidelines as much as possible. Releases will be numbered with the following format:

```<major>.<minor>.<patch>```

And constructed with the following guidelines:

* Breaking backward compatibility bumps the major (and resets the minor and patch)
* New additions, including new icons, without breaking backward compatibility bumps the minor (and resets the patch)
* Bug fixes and misc changes bumps the patch
For more information on SemVer, please visit http://semver.org/.

## Authors
Kristian Nilssen
* Email: [krinilssen@gmail.com](mailto:krinilssen@gmail.com)
* GitHub: https://github.com/KCNilssen

Matthew Spah
* Email: [spahmatthew@gmail.com](mailto:spahmatthew@gmail.com)
* GitHub: https://github.com/Mattsface

## Installation
```python3 -m pip install -i https://test.pypi.org/simple/ python-mlb-statsapi```

## Usage
Include Python MLB Stats api

``` import mlbstatsapi ```

Create an instance of mlb

``` mlb = mlbstatsapi.Mlb() ```

Now use it to pull information related to MLB Rosters, Teams, Players, stats... ect.

```
import mlbstatsapi

mlb = mlbstatsapi.Mlb()

oak_id = mlb.get_team_id("Oakland Athletics")
print (oak_id)

>>>[133]
```
