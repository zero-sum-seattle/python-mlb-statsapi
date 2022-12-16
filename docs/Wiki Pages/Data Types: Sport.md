## Usage that returns Sport objects

_To be added_

## Sport Structure

**Attributes are expandable and collapsable - [Link to Sport dataclass](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/sports/sport.py)**


<blockquote>

<details>
<summary>id : int   </summary>

* id number of the sport  
</details>

<details>
<summary>link : str   </summary>

* link of the sport  
</details>

<details>
<summary>name : str    </summary>

* name the sport  
</details>

<details>
<summary>code : str   </summary>

* Sport code  
</details>

<details>
<summary>abbreviation : str   </summary>

* Abbreviation for the sport  
</details>

<details>
<summary>sortorder : int   </summary>

* Some sort of sorting order  
</details>

<details>
<summary>activestatus : bool   </summary>

* Is the sport active  
</details>

</blockquote>


## Example output from MLB stats api endpoint

#### Mlb stats api Query:   
```http://statsapi.mlb.com/api/v1/sports```

#### Equivelant with *python-mlb-statsapi*:   
```
import mlbstatsapi

mlb = mlbstatsapi.Mlb()

mlb.get_sports()
```