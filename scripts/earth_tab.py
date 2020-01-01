from bokeh.models import Panel
from bokeh.layouts import row, column
from bokeh.models.widgets import TextInput, Button
from bokeh.tile_providers import get_provider, Vendors
from bokeh.plotting import figure
import math

def format_lonlat_to_webmercator(lat, lon):
    #copied from https://gis.stackexchange.com/questions/247871/convert-gps-coordinates-to-web-mercator-epsg3857-using-python-pyproj
    RADIUS = 6378137.0
    return(math.log(math.tan(math.pi / 4 + math.radians(lat) / 2)) * RADIUS, math.radians(lon) * RADIUS)


def earth_tab(dataset_collection):
    def update_map_and_save_position_on_click():
        # TODO check the input!
        newpositions = format_lonlat_to_webmercator(float(lat_input.value), float(lon_input.value))

        tab.child.children[2] = figure(x_range=(newpositions[1] - 10000, newpositions[1] + 10000),
                                       y_range=(newpositions[0] - 10000, newpositions[0] + 10000),
               x_axis_type="mercator", y_axis_type="mercator")
        plot_object = tab.child.children[2]
        plot_object.add_tile(tile_provider)
        plot_object.circle(x=newpositions[1], y=newpositions[0], size=15, fill_color="blue", fill_alpha=0.8)

        #passing on the input to the data_collection object to be able to access them from the plotting_tab
        dataset_collection.latpos = lat_input.value
        dataset_collection.lonpos = lon_input.value



    lat_input = TextInput(value="default", title="Latitude")
    lon_input = TextInput(value="default", title="Longitude")
    save_gps_button = Button(label="Set map position", button_type="success")
    save_gps_button.on_click(update_map_and_save_position_on_click)

    tile_provider = get_provider(Vendors.CARTODBPOSITRON)
    # range bounds supplied in web mercator coordinates
    p = figure(x_range=(0, 6000000), y_range=(0, 7000000),
               x_axis_type="mercator", y_axis_type="mercator")
    p.add_tile(tile_provider)

    layout = column(row(lat_input, lon_input), save_gps_button, p)
    tab = Panel(child=layout, title='Map')
    return tab
