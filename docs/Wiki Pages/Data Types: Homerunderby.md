## Homerunderby Structure

**Attributes are expandable and collapsable - [Link to Homerunderby dataclass](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/homerunderby/homerunderby.py)**

<blockquote>

<details>
<summary>info : Info  </summary>

* An object containing information about the game. Dataclass: [Info](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/homerunderby/attributes.py)

<blockquote>

<details>
<summary>id : int  </summary>

* The unique identifier of the event.  
</details>

<details>
<summary>name : str  </summary>

* The name of the event.  
</details>

<details>
<summary>eventtype : Eventtype  </summary>

* The type of event. Can be an instance of the Eventtype class or a dictionary containing the attributes for the Eventtype class. Datatype: [Eventtype](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/homerunderby/attributes.py)

<blockquote>

<details>
<summary>code (str):   </summary>

* The unique code of the event type.  
</details>

<details>
<summary>name (str):  </summary>

* The name of the event type.  
</details>

</blockquote>

</details>

<details>
<summary>eventdate : str  </summary>

* The date of the event.  
</details>

<details>
<summary>venue : Venue  </summary>

* The venue of the event. Can be an instance of the Venue class or a dictionary containing the attributes for the Venue class. Dataclass: [Venue](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/venue/venue.py)

<blockquote>

<details>
<summary>id : int </summary>

* id for this venue  
</details>

<details>
<summary>name : str </summary>

* Name for this venue  
</details>

<details>
<summary>link : str </summary>

* Link to venues endpoint  
</details>

</blockquote>

</details>

<details>
<summary>ismultiday : bool  </summary>

* Whether the event spans multiple days.  
</details>

<details>
<summary>isprimarycalendar : bool  </summary>

* Whether the event is on the primary calendar.  
</details>

<details>
<summary>filecode : str  </summary>

* The code of the file associated with the event.  
</details>

<details>
<summary>eventnumber : int  </summary>

* The number of the event.  
</details>

<details>
<summary>publicfacing : bool  </summary>

* Whether the event is public-facing.  
</details>

<details>
<summary>teams : List[Team]  </summary>

* The teams participating in the event. Can be a list of instances of the Team class or a list of dictionaries containing the attributes for the Team class. Dataclass: [Team](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/teams/team.py)

<blockquote>

<details>
<summary>id : int  </summary>

* id number of the team  
</details>

<details>
<summary>name : str  </summary>

* name of the team  
</details>

<details>
<summary>link : str  </summary>

* The API link for the team  
</details>

</blockquote>

</details>

</blockquote>

</details>

<details>
<summary>status : Status  </summary>

* An object containing the status of the game. Dataclass: [Status](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/homerunderby/attributes.py)

<blockquote>

<details>
<summary>state : str  </summary>

* The current state of the game or round (e.g. "in progress", "paused", "ended")  
</details>

<details>
<summary>currentround : int  </summary>

* The number of the current round in the game  
</details>

<details>
<summary>currentroundtimeleft : str  </summary>

* The amount of time left in the current round, in a human-readable format (e.g. "4:00")  
</details>

<details>
<summary>intiebreaker : bool  </summary>

* Whether the game or round is currently in a tiebreaker  
</details>

<details>
<summary>tiebreakernum : int  </summary>

* The number of the current tiebreaker, if applicable  
</details>

<details>
<summary>clockstopped : bool  </summary>

* Whether the round clock is currently stopped  
</details>

<details>
<summary>bonustime : bool  </summary>

* Whether the round is currently in bonus time  
</details>

</blockquote>

</details>

<details>
<summary>rounds : Round  </summary>

* A list of Round objects representing the rounds in the game. Dataclass: [Round](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/homerunderby/attributes.py)

<blockquote>

<details>
<summary>round : int  </summary>

* An integer representing the round number.  
</details>

<details>
<summary>numbatters : int  </summary>

* An integer representing the number of batters in the round.  
</details>

<details>
<summary>matchups : List[Matchup]  </summary>

* A list of objects containing the data for the matchups in the round. Dataclass: [Matchup](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/homerunderby/attributes.py)

<blockquote>

<details>
<summary>topseed : Seed  </summary>

* Containing the top seed in the matchup. Dataclass: [Seed](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/homerunderby/attributes.py)

<blockquote>

<details>
<summary>complete : bool  </summary>

* A boolean indicating whether the seed has been completed.
</details>

<details>
<summary>started : bool  </summary>

* A boolean indicating whether the seed has been started.
</details>

<details>
<summary>winner : bool  </summary>

* A boolean indicating whether the player for this seed is the winner of the game.
</details>

<details>
<summary>player : Person  </summary>

* An object containing the data for the player associated with this seed. This can either be a Person object or a dictionary. Dataclass: [Person](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/people.py)

<blockquote>

<details>
<summary>id : int  </summary>

* id number of the person
</details>

<details>
<summary>full_name : str  </summary>

* full_name of the person
</details>

<details>
<summary>link : str  </summary>

* Api link to person
</details>

</blockquote>

</details>

<details>
<summary>topderbyhitdata : Hitdata  </summary>

* An object containing the data for the top hit in the seed. This can either be a Hitdata object or a dictionary. Dataclass: [Hitdata](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/homerunderby/attributes.py)

<blockquote>

<details>
<summary>launchspeed : float  </summary>

* The speed at which the hit was launched
</details>

<details>
<summary>totaldistance : int  </summary>

* The total distance the hit traveled
</details>

<details>
<summary>launchangle : float  </summary>

* The angle at which the hit was launched, if applicable
</details>

<details>
<summary>coordinates : Coordinates  </summary>

* Coordinates for the hit. Dataclass: [Coordinates](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/homerunderby/attributes.py)

<blockquote>

<details>
<summary>coordx : float  </summary>

* The x-coordinate of the hit
</details>

<details>
<summary>coordy : float  </summary>

* The y-coordinate of the hit
</details>

<details>
<summary>landingposx : float  </summary>

* The x-coordinate of the hits's landing position, if applicable
</details>

<details>
<summary>landingposy : float  </summary>

* The y-coordinate of the hits's landing position, if applicable
</details>

</blockquote>

</details>

<details>
<summary>trajectorydata : Trajectorydata  </summary>

* Trajectory data for the hit. Dataclass: [Trajectorydata](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/homerunderby/attributes.py)

<blockquote>

<details>
<summary>trajectorypolynomialx : List[int]  </summary>

* A list of coefficients for the polynomial representing the x-coordinate of the hits's trajectory
</details>

<details>
<summary>trajectorypolynomialy : List[int]  </summary>

* A list of coefficients for the polynomial representing the y-coordinate of the hits's trajectory
</details>

<details>
<summary>trajectorypolynomialz : List[int]  </summary>

* A list of coefficients for the polynomial representing the z-coordinate of the hits's trajectory
</details>

<details>
<summary>validtimeinterval : List[int]  </summary>

* A list of two elements representing the start and end times for which the polynomial coefficients are valid
</details>

<details>
<summary>measuredtimeinterval : List[int]  </summary>

* A list of two elements representing the start and end times of the interval during which the hits's trajectory was measured
</details>

</blockquote>

</details>

</blockquote>

</details>

<details>
<summary>hits : Hits  </summary>

* An object containing the data for the hits in the seed. This can either be a Hits object or a dictionary. Dataclass: [Hits](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/homerunderby/attributes.py)

<blockquote>

<details>
<summary>bonustime : bool  </summary>

* A boolean indicating whether the hit occurred during bonus time.
</details>

<details>
<summary>homerun : bool  </summary>

* A boolean indicating whether the hit was a homerun.
</details>

<details>
<summary>tiebreaker : bool  </summary>

* A boolean indicating whether the hit occurred during a tiebreaker.
</details>

<details>
<summary>hitdata : Hitdata  </summary>

* An object containing the data for the hit. This can either be a Hitdata object or a dictionary. Dataclass: [Hitdata](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/homerunderby/attributes.py)

<blockquote>

<details>
<summary>launchspeed : float  </summary>

* The speed at which the hit was launched
</details>

<details>
<summary>totaldistance : int  </summary>

* The total distance the hit traveled
</details>

<details>
<summary>launchangle : float  </summary>

* The angle at which the hit was launched, if applicable
</details>

<details>
<summary>coordinates : Coordinates  </summary>

* Coordinates for the hit. Dataclass: [Coordinates](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/homerunderby/attributes.py)

<blockquote>

<details>
<summary>coordx : float  </summary>

* The x-coordinate of the hit
</details>

<details>
<summary>coordy : float  </summary>

* The y-coordinate of the hit
</details>

<details>
<summary>landingposx : float  </summary>

* The x-coordinate of the hits's landing position, if applicable
</details>

<details>
<summary>landingposy : float  </summary>

* The y-coordinate of the hits's landing position, if applicable
</details>

</blockquote>

</details>

<details>
<summary>trajectorydata : Trajectorydata  </summary>

* Trajectory data for the hit. Dataclass: [Trajectorydata](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/homerunderby/attributes.py)

<blockquote>

<details>
<summary>trajectorypolynomialx : List[int]  </summary>

* A list of coefficients for the polynomial representing the x-coordinate of the hits's trajectory
</details>

<details>
<summary>trajectorypolynomialy : List[int]  </summary>

* A list of coefficients for the polynomial representing the y-coordinate of the hits's trajectory
</details>

<details>
<summary>trajectorypolynomialz : List[int]  </summary>

* A list of coefficients for the polynomial representing the z-coordinate of the hits's trajectory
</details>

<details>
<summary>validtimeinterval : List[int]  </summary>

* A list of two elements representing the start and end times for which the polynomial coefficients are valid
</details>

<details>
<summary>measuredtimeinterval : List[int]  </summary>

* A list of two elements representing the start and end times of the interval during which the hits's trajectory was measured
</details>

</blockquote>

</details>

</blockquote>

</details>

<details>
<summary>ishomerun : bool  </summary>

* A boolean indicating whether the hit was a homerun. This attribute is a duplicate of the `homerun` attribute.
</details>

<details>
<summary>playid : str  </summary>

* A string containing the ID of the play in which the hit occurred.
</details>

<details>
<summary>timeremaining : str  </summary>

* A string indicating the amount of time remaining in the game when the hit occurred.
</details>

<details>
<summary>isbonustime : bool  </summary>

* A boolean indicating whether the hit occurred during bonus time. This attribute is a duplicate of the `bonustime` attribute.
</details>

<details>
<summary>istiebreaker : bool  </summary>

* A boolean indicating whether the hit occurred during a tiebreaker. This attribute is a duplicate of the `tiebreaker` attribute.
</details>


</blockquote>

</details>

<details>
<summary>seed : int  </summary>

* An integer representing the seed number.
</details>

<details>
<summary>order : int  </summary>

* An integer representing the order in which the seed was played.
</details>

<details>
<summary>iswinner : bool  </summary>

* A boolean indicating whether the player for this seed is the winner of the game. This attribute is a duplicate of the `winner` attribute.
</details>

<details>
<summary>iscomplete : bool  </summary>

* A boolean indicating whether the seed has been completed. This attribute is a duplicate of the `complete` attribute.
</details>

<details>
<summary>isstarted : bool  </summary>

* A boolean indicating whether the seed has been started. This attribute is a duplicate of the `started` attribute.
</details>

<details>
<summary>numhomeruns : int  </summary>

* An integer representing the number of homeruns hit in the seed.
</details>

</blockquote>

</details>

<details>
<summary>bottomseed : Seed  </summary>

* Containing the bottom seed in the matchup. Dataclass: [Seed](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/homerunderby/attributes.py)

<blockquote>

<details>
<summary>complete : bool  </summary>

* A boolean indicating whether the seed has been completed.
</details>

<details>
<summary>started : bool  </summary>

* A boolean indicating whether the seed has been started.
</details>

<details>
<summary>winner : bool  </summary>

* A boolean indicating whether the player for this seed is the winner of the game.
</details>

<details>
<summary>player : Person  </summary>

* An object containing the data for the player associated with this seed. This can either be a Person object or a dictionary. Dataclass: [Person](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/people.py)

<blockquote>

<details>
<summary>id : int  </summary>

* id number of the person
</details>

<details>
<summary>full_name : str  </summary>

* full_name of the person
</details>

<details>
<summary>link : str  </summary>

* Api link to person
</details>

</blockquote>

</details>

<details>
<summary>topderbyhitdata : Hitdata  </summary>

* An object containing the data for the top hit in the seed. This can either be a Hitdata object or a dictionary. Dataclass: [Hitdata](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/homerunderby/attributes.py)

<blockquote>

<details>
<summary>launchspeed : float  </summary>

* The speed at which the hit was launched
</details>

<details>
<summary>totaldistance : int  </summary>

* The total distance the hit traveled
</details>

<details>
<summary>launchangle : float  </summary>

* The angle at which the hit was launched, if applicable
</details>

<details>
<summary>coordinates : Coordinates  </summary>

* Coordinates for the hit. Dataclass: [Coordinates](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/homerunderby/attributes.py)

<blockquote>

<details>
<summary>coordx : float  </summary>

* The x-coordinate of the hit
</details>

<details>
<summary>coordy : float  </summary>

* The y-coordinate of the hit
</details>

<details>
<summary>landingposx : float  </summary>

* The x-coordinate of the hits's landing position, if applicable
</details>

<details>
<summary>landingposy : float  </summary>

* The y-coordinate of the hits's landing position, if applicable
</details>

</blockquote>

</details>

<details>
<summary>trajectorydata : Trajectorydata  </summary>

* Trajectory data for the hit. Dataclass: [Trajectorydata](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/homerunderby/attributes.py)

<blockquote>

<details>
<summary>trajectorypolynomialx : List[int]  </summary>

* A list of coefficients for the polynomial representing the x-coordinate of the hits's trajectory
</details>

<details>
<summary>trajectorypolynomialy : List[int]  </summary>

* A list of coefficients for the polynomial representing the y-coordinate of the hits's trajectory
</details>

<details>
<summary>trajectorypolynomialz : List[int]  </summary>

* A list of coefficients for the polynomial representing the z-coordinate of the hits's trajectory
</details>

<details>
<summary>validtimeinterval : List[int]  </summary>

* A list of two elements representing the start and end times for which the polynomial coefficients are valid
</details>

<details>
<summary>measuredtimeinterval : List[int]  </summary>

* A list of two elements representing the start and end times of the interval during which the hits's trajectory was measured
</details>

</blockquote>

</details>

</blockquote>

</details>

<details>
<summary>hits : Hits  </summary>

* An object containing the data for the hits in the seed. This can either be a Hits object or a dictionary. Dataclass: [Hits](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/homerunderby/attributes.py)

<blockquote>

<details>
<summary>bonustime : bool  </summary>

* A boolean indicating whether the hit occurred during bonus time.
</details>

<details>
<summary>homerun : bool  </summary>

* A boolean indicating whether the hit was a homerun.
</details>

<details>
<summary>tiebreaker : bool  </summary>

* A boolean indicating whether the hit occurred during a tiebreaker.
</details>

<details>
<summary>hitdata : Hitdata  </summary>

* An object containing the data for the hit. This can either be a Hitdata object or a dictionary. Dataclass: [Hitdata](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/homerunderby/attributes.py)

<blockquote>

<details>
<summary>launchspeed : float  </summary>

* The speed at which the hit was launched
</details>

<details>
<summary>totaldistance : int  </summary>

* The total distance the hit traveled
</details>

<details>
<summary>launchangle : float  </summary>

* The angle at which the hit was launched, if applicable
</details>

<details>
<summary>coordinates : Coordinates  </summary>

* Coordinates for the hit. Dataclass: [Coordinates](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/homerunderby/attributes.py)

<blockquote>

<details>
<summary>coordx : float  </summary>

* The x-coordinate of the hit
</details>

<details>
<summary>coordy : float  </summary>

* The y-coordinate of the hit
</details>

<details>
<summary>landingposx : float  </summary>

* The x-coordinate of the hits's landing position, if applicable
</details>

<details>
<summary>landingposy : float  </summary>

* The y-coordinate of the hits's landing position, if applicable
</details>

</blockquote>

</details>

<details>
<summary>trajectorydata : Trajectorydata  </summary>

* Trajectory data for the hit. Dataclass: [Trajectorydata](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/homerunderby/attributes.py)

<blockquote>

<details>
<summary>trajectorypolynomialx : List[int]  </summary>

* A list of coefficients for the polynomial representing the x-coordinate of the hits's trajectory
</details>

<details>
<summary>trajectorypolynomialy : List[int]  </summary>

* A list of coefficients for the polynomial representing the y-coordinate of the hits's trajectory
</details>

<details>
<summary>trajectorypolynomialz : List[int]  </summary>

* A list of coefficients for the polynomial representing the z-coordinate of the hits's trajectory
</details>

<details>
<summary>validtimeinterval : List[int]  </summary>

* A list of two elements representing the start and end times for which the polynomial coefficients are valid
</details>

<details>
<summary>measuredtimeinterval : List[int]  </summary>

* A list of two elements representing the start and end times of the interval during which the hits's trajectory was measured
</details>

</blockquote>

</details>

</blockquote>

</details>

<details>
<summary>ishomerun : bool  </summary>

* A boolean indicating whether the hit was a homerun. This attribute is a duplicate of the `homerun` attribute.
</details>

<details>
<summary>playid : str  </summary>

* A string containing the ID of the play in which the hit occurred.
</details>

<details>
<summary>timeremaining : str  </summary>

* A string indicating the amount of time remaining in the game when the hit occurred.
</details>

<details>
<summary>isbonustime : bool  </summary>

* A boolean indicating whether the hit occurred during bonus time. This attribute is a duplicate of the `bonustime` attribute.
</details>

<details>
<summary>istiebreaker : bool  </summary>

* A boolean indicating whether the hit occurred during a tiebreaker. This attribute is a duplicate of the `tiebreaker` attribute.
</details>


</blockquote>

</details>

<details>
<summary>seed : int  </summary>

* An integer representing the seed number.
</details>

<details>
<summary>order : int  </summary>

* An integer representing the order in which the seed was played.
</details>

<details>
<summary>iswinner : bool  </summary>

* A boolean indicating whether the player for this seed is the winner of the game. This attribute is a duplicate of the `winner` attribute.
</details>

<details>
<summary>iscomplete : bool  </summary>

* A boolean indicating whether the seed has been completed. This attribute is a duplicate of the `complete` attribute.
</details>

<details>
<summary>isstarted : bool  </summary>

* A boolean indicating whether the seed has been started. This attribute is a duplicate of the `started` attribute.
</details>

<details>
<summary>numhomeruns : int  </summary>

* An integer representing the number of homeruns hit in the seed.
</details>

</blockquote>

</details>

</blockquote>

</details>


</blockquote>

</details>

<details>
<summary>players : List[Person]  </summary>

* A list of objects containing the data for the players in the game. Dataclass: [Person](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/people.py)

<blockquote>

<details>
<summary>id : int  </summary>

* id number of the person
</details>

<details>
<summary>full_name : str  </summary>

* full_name of the person
</details>

<details>
<summary>link : str  </summary>

* Api link to person
</details>

<details>
<summary>primaryposition : Position  </summary>

* PrimaryPosition of the Person. Dataclass: [Position](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/development/mlbstatsapi/models/people/attributes.py)

<blockquote>

<details>
<summary>lcode: str  </summary>

* code number of the Position
</details>

<details>
<summary>lname: str  </summary>

* the name of the Position
</details>

<details>
<summary>ltype: str  </summary>

* the type of the Position
</details>

<details>
<summary>labbreviation: str  </summary>

* the abbreviation of the Position
</details>

</blockquote>

</details>

<details>
<summary>pitchhand : str  </summary>

* PitchHand of the Person
</details>

<details>
<summary>batside : str  </summary>

* BatSide of the Person
</details>

<details>
<summary>fullname : str  </summary>

* full name of the Person
</details>

<details>
<summary>firstname : str  </summary>

* First name of the Person
</details>

<details>
<summary>lastname : str  </summary>

* Last name of the Person
</details>

<details>
<summary>primarynumber : str  </summary>

* Primary number of the Person
</details>

<details>
<summary>birthdate : str  </summary>

* Birth date of the Person
</details>

<details>
<summary>currentteam : str  </summary>

* The current Team of the Person
</details>

<details>
<summary>currentage : str  </summary>

* The current age of the Person
</details>

<details>
<summary>birthcity : str  </summary>

* The birthcity of the Person
</details>

<details>
<summary>birthstateprovince : str  </summary>

* The province of the birth state
</details>

<details>
<summary>height : str  </summary>

* The height of the Person
</details>

<details>
<summary>weight : str  </summary>

* The weight of the Person
</details>

<details>
<summary>active : str  </summary>

* The active status of the Person
</details>

<details>
<summary>usename : str  </summary>

* The use name of the Person
</details>

<details>
<summary>middlename : str  </summary>

* The middle name of the Person
</details>

<details>
<summary>boxscorename : str  </summary>

* The box score name of the Person
</details>

<details>
<summary>nickname : str  </summary>

* The nickname of the Person
</details>

<details>
<summary>draftyear : int  </summary>

* The draft year of the Person
</details>

<details>
<summary>mlbdebutdate : str  </summary>

* The MLB debut date of the Person
</details>

<details>
<summary>namefirstlast : str  </summary>

* The first and last name of the Person
</details>

<details>
<summary>nameslug : str  </summary>

* The name slug of the Person
</details>

<details>
<summary>firstlastname : str  </summary>

* The first and last name of the Person
</details>

<details>
<summary>lastfirstname : str  </summary>

* The last and first name of the Person
</details>

<details>
<summary>lastinitname : str  </summary>

* The last init name of the Person
</details>

<details>
<summary>initlastname : str  </summary>

* The init last name of the Person
</details>

<details>
<summary>fullfmlname : str  </summary>

* The full fml name of the Person
</details>

<details>
<summary>fulllfmname : str  </summary>

* The full lfm name of the Person
</details>

<details>
<summary>uselastname : str  </summary>

* The last name of the
</details>

<details>
<summary>birthcountry : str  </summary>

* The birth country of the Person
</details>

<details>
<summary>pronunciation : str  </summary>

* The pronuciation of the Person's name
</details>

<details>
<summary>strikezonetop : float  </summary>

* The strike zone top of the Person
</details>

<details>
<summary>strikezonebottom : float  </summary>

* The strike zone bottom of the Person
</details>

<details>
<summary>nametitle : str  </summary>

* The name title of the Person
</details>

<details>
<summary>gender : str  </summary>

* The gender of the Person
</details>

<details>
<summary>isplayer : bool  </summary>

* The player status of the Person
</details>

<details>
<summary>isverified : bool  </summary>

* The verification of the Person
</details>

<details>
<summary>namematrilineal : str  </summary>

* The name matrilineal of the Person
</details>

<details>
<summary>deathdate : str  </summary>

* The death date of the Person
</details>

<details>
<summary>deathcity : str  </summary>

* The death city of the Person
</details>

<details>
<summary>deathcountry : str  </summary>

* The death country of the Person
</details>

<details>
<summary>lastplayeddate : str  </summary>

* The last played date of the Person
</details>

<details>
<summary>namesuffix : str  </summary>

* The namesuffix of the Person
</details>

</blockquote>

</details>

</blockquote>

## Usage that returns Homerunderby objects

### `get_homerun_derby`

Description: Return a Homerunderby

**Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `award_id` | string | Yes      | Insert gamePk to return HomerunDerby data for a specific gamepk. | None

**Other Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `fields` | string | No      | Format: Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute | None

## Example output from MLB stats api endpoint

#### Mlb stats api Query:   
```https://statsapi.mlb.com/api/v1/homeRunDerby/511101```

#### Equivelant with *python-mlb-statsapi*:   
```
import mlbstatsapi

mlb = mlbstatsapi.Mlb()

mlb.get_homerunderby(game_id = 511101)
```