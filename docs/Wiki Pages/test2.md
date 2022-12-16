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