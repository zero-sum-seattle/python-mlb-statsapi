## Usage that returns League objects

_To be added_

## People Structure

**People are expandable and collapsable - [Link to people dataclass](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/people.py)**

<blockquote>

<details>
<summary>id : int  </summary>

* People id 
</details>

<details>
<summary>link : str </summary>

* link to people endpoint
</details>

<details>
<summary>primaryposition : Position </summary>

* Person primary position. Dataclass: [Position](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/attributes.py) 

<blockquote>

<details>
<summary>code: str </summary>

* code number of the Position 
</details>

<details>
<summary>name: str </summary>

* the name of the Position 
</details>

<details>
<summary>type: str </summary>

* the type of the Position 
</details>

<details>
<summary>abbreviation: str </summary>

* the abbreviation of the Position 
</details>

</blockquote>

</details>

<details>
<summary>pitchhand : PitchHand </summary>

* Person primary position. Dataclass: [PitchHand](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/attributes.py) 

<blockquote>

<details>
<summary>code : str </summary>

* code number of the PitchHand 
</details>

<details>
<summary>descritpion: str </summary>

* description of the PitchHand 
</details>

</blockquote>

</details>

<details>
<summary>batside : BatSide </summary>

* Person's BatSide. Dataclass: [BatSide](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/attributes.py) 

<blockquote>

<details>
<summary>code : str </summary>

* code number of the BatSide 
</details>

<details>
<summary>descritpion: str </summary>

* description of the BatSide 
</details>

</blockquote>
 
</details>

<details>
<summary>fullname : str </summary>

* full name of the Person
</details>

<details>
<summary>firstname : str </summary>

* First name of the Person
</details>

<details>
<summary>lastname : str </summary>

* Last name of the Person
</details>

<details>
<summary>primarynumber : str </summary>

* Primary number of the Person
</details>

<details>
<summary>birthdate : str </summary>

* Birth date of the Person 
</details>

<details>
<summary>currentteam : str </summary>

* The current Team of the Person 
</details>

<details>
<summary>currentage : str </summary>

* The current age of the Person 
</details>

<details>
<summary>birthcity : str </summary>

* The birthcity of the Person 
</details>

<details>
<summary>birthstateprovince : str </summary>

* The province of the birth state 
</details>

<details>
<summary>height : str </summary>

* The height of the Person 
</details>

<details>
<summary>active : str </summary>

* The active status of the Person 
</details>

<details>
<summary>usename : str </summary>

* The use name of the Person 
</details>

<details>
<summary>middlename : str </summary>

* The middle name of the Person 
</details>

<details>
<summary>boxscorename : str </summary>

* The box score name of the Person 
</details>

<details>
<summary>nickname : str </summary>

* The nickname of the Person
</details>

<details>
<summary>draftyear : str </summary>

* The draft year of the Person 
</details>

<details>
<summary>mlbdebutdate : str </summary>

* The MLB debut date of the Person 
</details>

<details>
<summary>namefirstlast : str </summary>

* The first and last name of the Person 
</details>
        
<details>
<summary>nameslug : str </summary>

* The name slug of the Person
</details>
        
<details>
<summary>firstlastname : str </summary>

* The first and last name of the Person 
</details>
        
<details>
<summary>lastfirstname : str </summary>

* The last and first name of the Person
</details>

<details>
<summary>lastinitname : str </summary>

* The last and first name of the Person
</details>

<details>
<summary>lastfirstname : str </summary>

* The last init name of the Person
</details>

<details>
<summary>initlastname : str </summary>

* The init last name of the Person
</details>
        
<details>
<summary>fullfmlname : str </summary>

* The init last name of the Person
</details>

<details>
<summary>initlastname : str </summary>

* The full fml name of the Person
</details>

<details>
<summary>fulllfmname : str </summary>

* The full lfm name of the Person
</details>

<details>
<summary>uselastname : str </summary>

* The last name of the Person
</details>
        
<details>
<summary>birthcountry : str </summary>

* The birth country of the Person
</details>

<details>
<summary>pronunciation : str </summary>

* The pronuciation of the Person's name
</details>

<details>
<summary>strikezonetop : str </summary>

* The strike zone top of the Person
</details>

<details>
<summary>strikezonebottom : str </summary>

* The strike zone bottom of the Person
</details>

<details>
<summary>nametitle : str </summary>

* The name title of the Person
</details>

<details>
<summary>gender : str </summary>
 
 * The gender of the Person
</details>

<details>
<summary>isplayer : str </summary>

* The player status of the Person
</details>

<details>
<summary>isverified : str </summary>

* The verification of the Person
</details>

<details>
<summary>namematrilineal : str </summary>

* The name matrilineal of the Person
</details>
       
<details>
<summary>deathdate : str </summary>

* The death date of the Person
</details>

<details>
<summary>deathcity : str </summary>

* The death city of the Person
</details>
        
<details>
<summary>deathcountry : str </summary>

* The death country of the Person
</details>

<details>
<summary>lastplayeddate : str </summary>

* The last played date of the Person
</details>

<details>
<summary>namesuffix : str </summary>

* The namesuffix of the Person
</details>

</blockquote>

## Example output from MLB stats api endpoint

#### Mlb stats api Query:   
```https://statsapi.mlb.com/api/v1/people?personIds=605151```

#### Equivelant with *python-mlb-statsapi*:   
```
import mlbstatsapi

mlb = mlbstatsapi.Mlb()

mlb.get_person(player_id = 605151)
```