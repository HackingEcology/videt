# videt -- Vizualising Datasets of Ecological Trend

a collaborative project of [Hacking Ecology](https://hackingecology.eu/), a collective for open data, open source and
citizen science that helps us avert the sixth mass extinction.

videt visualizes open datasets of processes that might have an influence on ecosystem functioning. At its core, it uses
[bokeh](https://docs.bokeh.org/en/latest/) and allows users to interactively choose datasets to show.

### Usage

As there is no online version of videt yet, users need to clone the repo, `cd` into the videt folder and then run

```
bokeh serve ./ --show
```
s

### Structure

As required by Bokeh, `main.py` is the index file that points to the other features of videt. `scripts/plotting_tab.py`
contains the code for the GUI and all the plotting commands, `scripts/info_tab.py` creates the second tab of videt.
`scripts/datasets.py` contains the code that loads the datasets. If you want to add new datasets they need to inherit
from `timeseries_dataset` and implement all the fields and functions of it; please see to the other datasets already
implemented for reference. Currently, `config/` contains a single config file that indicates the datasets implemented
and the arguments relevant for them.


## To-Do's

Improve everything you want. Work on the todos in the code. Implement new datasets. Thank you very much in advance.

### (incomplete) List of Datasets to implement

Geographic Time Series
Land-cover change	https://catalog.data.gov/dataset/historical-land-cover-change-and-land-use-conversions-global-dataset	Need to convert from map (netCDF) to simple numbers
Sea Ice thickness	https://climatedataguide.ucar.edu/climate-data/sea-ice-thickness-data-sets-overview-comparison-table
Soil moisture	https://climatedataguide.ucar.edu/climate-data/soil-moisture-data-sets-overview-comparison-tables
Ocean Acidification	http://portal.goa-on.org/

Anthropogenic stuff
Heat flux	https://springernature.figshare.com/collections/A_new_global_gridded_anthropogenic_heat_flux_dataset_with_high_spatial_resolution_and_long-term_series/4182824
CO2 emissions 	https://www.icos-cp.eu/GCP/2018
Anthropogenic Biomes	https://sedac.ciesin.columbia.edu/data/collection/anthromes/sets/browse
Population	http://www.sustainableworld.com/data/pop_main.html
SDG progress	https://sdg-tracker.org/
Economy -- IMF	https://www.imf.org/en/Data
Economy -- World Bank	https://databank.worldbank.org/databases.aspx
Urbanization, fertilizer use, times of agriculture...

Biological time series
BioTIME	http://biotime.st-andrews.ac.uk/downloadArea.php	Many separate studies for different regions; no API, AFAIK
IUCN Red List of endangered species	--	API with token; 
Vegetation index (MODIS NDVI)	https://icdc.cen.uni-hamburg.de/1/daten/land/modis-vegetationindex.html	access is restricted
Global vegetation	https://lpdaac.usgs.gov/products/vcf5kyrv001/
Ocean acidification biological responses	http://oa-icc.ipsl.fr/


Weather/Climate time series
DWD	...	Necessary to figure out which of the folders 
Cloud Data	https://climserv.ipsl.polytechnique.fr/gewexca/index-2.html
Temperature	https://climatedataguide.ucar.edu/climate-data/global-temperature-data-sets-overview-comparison-table
Different athmospheric reanalyses	https://climatedataguide.ucar.edu/climate-data/atmospheric-reanalysis-overview-comparison-tables


Others / Collections
https://lpdaac.usgs.gov/product_search/
UN data	https://data.un.org/
https://datacatalog.worldbank.org/harvest-source/indicators-api
