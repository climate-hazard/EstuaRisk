# EstuaRisk
Web-based tool to quantify estuarine flood risks in the UK.

### Concepts
* Users can look up the map and see the hot spots with high estuarine risks based on analysis of the available data.
* Users can interact by choosing climate change scenarios and observe the change in risk level.

### Implementation

The code is written in Python and is intended to be easy and modifiable. 

* Tidal gauge data from https://www.bodc.ac.uk/data/hosted_data_systems/sea_level/uk_tide_gauge_network/processed/ 

    + Access to individual gauge is made by Selenium

* River data from SEPA API https://timeseriesdoc.sepa.org.uk/api-documentation/api-function-reference/specifying-date-and-time/


* Storm wave data is retrieved from Copernicus via the CDS API https://cds.climate.copernicus.eu/api-how-to 

### Development plan
* Integrate hydrodynamic modelling results to show the flooding inundation extent.

### Project info
SEARCH ``Sensitivity of Estuaries to Climate Hazards''. 