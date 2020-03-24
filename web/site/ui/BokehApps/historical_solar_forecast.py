from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, LinearAxis, DataRange1d, Legend, LegendItem, Band
from bokeh.models.widgets import RadioButtonGroup, CheckboxButtonGroup, Div, DateSlider, Slider, Button
from bokeh.palettes import Category20
from bokeh.layouts import column, row, WidgetBox, Spacer
import pandas as pd
from bokeh.io import curdoc
import sqlite3
import datetime
import numpy as np
import re
import operator

conn = sqlite3.connect('../../db.sqlite3')
conn.row_factory = sqlite3.Row
c = conn.cursor()
data_labels_forecast_solar = c.execute("pragma table_info('ui_forecastssolardata')").fetchall()
data_labels_forecast_solar = list(map(lambda x: x['name'], data_labels_forecast_solar ))
current_datetime = datetime.datetime.now().replace(year=2010)

def get_string_date(date):
    # Return date in string without 0 padding on date month and day
    return date.strftime('%m/%d/%Y %H:%M')

label_colors = {}
lines = {}
bands = {}

def make_dataset(range_start, range_end):
    # Prepare data

    print(range_start)
    print(range_end)
    data = c.execute("select * from ui_forecastssolardata where timestamp >:range_start and timestamp <=:range_end",
    {'range_start':get_string_date(range_start), 'range_end':get_string_date(range_end)}).fetchall()
 
    cds = ColumnDataSource(data={
        'time': [datetime.datetime.strptime(entry['timestamp'], '%m/%d/%Y %H:%M') for entry in data]
    })

    for i,col_name in enumerate([label for label in data_labels_forecast_solar[2:] if re.search('_(minus|plus)', label) is None]):
        cds.data.update({
            col_name: [entry[col_name] for entry in data]
        })
        
        label_colors.update({
            col_name+'_color': i*2
        })

        r = re.compile(col_name+'_(minus|plus)')

        if len(list(filter(r.search, data_labels_forecast_solar))) == 2:

            value_arr = np.array(cds.data[col_name])
            value_minus_arr = np.array(
                [entry[col_name+'_minus']/100 for entry in data]) # Divide by 100 for percentage (%)
            value_plus_arr = np.array(
                [entry[col_name+'_plus']/100 for entry in data]) # Divide by 100 for percentage (%)

            cds.data[col_name+'_lower'] = list(\
                value_arr - np.multiply(value_arr, value_minus_arr))
            cds.data[col_name+'_upper'] = list(\
                value_arr + np.multiply(value_arr, value_plus_arr))
    
    return cds

# Styling for a plot
def style(p):
    # Title 
    p.title.align = 'center'
    p.title.text_font_size = '20pt'
    p.title.text_font = 'serif'

    # Axis titles
    p.xaxis.axis_label_text_font_size = '14pt'
    p.xaxis.axis_label_text_font_style = 'bold'
    p.yaxis.axis_label_text_font_size = '14pt'
    p.yaxis.axis_label_text_font_style = 'bold'

    # Tick labels
    p.xaxis.major_label_text_font_size = '12pt'
    p.yaxis.major_label_text_font_size = '12pt'

    return p

def make_plot(src): # Takes in a ColumnDataSource
    # Create the plot
    time = src.data['time']
    plot = figure(
        tools="", # this gives us our tools
        x_axis_type="datetime",
        plot_height=250,
        sizing_mode='scale_both',
        width_policy='max',
        toolbar_location = None,
        x_axis_label = None,
        y_axis_label = "Power (W/m^2)"
        )

    for label in [label for label in src.column_names[1:]]:

        legend_label = col_to_title_upper(label)

        if not re.search('(_lower|_upper)', label) is None:
            value_name = re.split('(_lower|_upper)', label)[0]
            bands[value_name] = Band(
                base='time',
                lower= value_name + '_lower',
                upper= value_name + '_upper',
                source=src,
                level = 'underlay',
                fill_alpha=1.0,
                fill_color=Category20[20][label_colors[value_name+'_color']+1],
                line_width=1, 
                line_color='black',
                visible = label in [title_to_col(plot_select.labels[i]) for i in plot_select.active],
                name = label)
            plot.add_layout(bands[value_name])
        else:
            color = Category20[20][label_colors[label+'_color']]
            lines[label] = plot.line( 
                x='time',
                y=label,
                line_color = color, 
                line_alpha = 1.0,
                line_width=1,
                legend_label = legend_label,
                source=src,
                visible = label in [title_to_col(plot_select.labels[i]) for i in plot_select.active],
                name = label,
                )

    # styling
    plot = style(plot)

    plot.legend.orientation = 'horizontal'
    plot.legend.location = 'top_center'

    return plot

def col_to_title_upper(label):
    # Convert column name to title

    legend_label = ' '.join([word.upper() for word in label.split('_')])

    return legend_label

def title_to_col(title):
    # Convert title to a column name

    col_name = title.lower().replace(' ','_')
    return col_name

def updateRange():
    # Update range when sliders move and update button is clicked
    delta = datetime.timedelta(hours=date_span_slider.value)
    selected_date = datetime.datetime.combine(date_slider.value, datetime.datetime.min.time())
    range_start = selected_date - delta
    range_end = selected_date + delta
    new_src = make_dataset(range_start, range_end)
    src.data.update(new_src.data)

def update(attr, old, new):
    # Update plots when widgets change

    # Update visible plots
    for label in lines.keys():
        label_name = col_to_title_upper(label)
        lines[label].visible = label_name in [plot_select.labels[i] for i in plot_select.active]
        if label in bands.keys():
            bands[label].visible = lines[label].visible


# Create widgets
# Create Checkbox Select Group Widget
labels_list = [col_to_title_upper(label) for label in data_labels_forecast_solar[2:] if re.search('_(minus|plus)', label) is None]
plot_select = CheckboxButtonGroup(
    labels = labels_list,
    active = [0],
    width_policy='min'
)
plot_select.on_change('active', update)

# Create Date Slider
# Get start and end date in table
end_date = c.execute('select timestamp from ui_forecastssolardata order by id desc limit 1').fetchall()
end_date = end_date[0]['timestamp']
start_date = c.execute('select timestamp from ui_forecastssolardata order by id asc limit 1').fetchall()
start_date = start_date[0]['timestamp']
date_slider = DateSlider(title='Date', start=start_date, end=end_date, value=current_datetime, step=1, width=250)

# Create Date Range Slider
date_span_slider = Slider(title='Time Span (Hours)', start=4, end=120, value=24, step=4, width=150)

# Create Update Button
update_range_button = Button(label='Update', button_type='primary', width=100)
update_range_button.on_click(updateRange)

title = Div(text="""<h2>Historical Solar Forecast</h2>""")

# Set initial plot information
initial_plots = [title_to_col(plot_select.labels[i]) for i in plot_select.active]

delta_init = datetime.timedelta(days=1)
src = make_dataset(current_datetime - delta_init, current_datetime + delta_init)

plot = make_plot(src)

# Setup Widget Layouts

# Dates
date_sliders = row(date_slider, date_span_slider)
date_widgets = column(date_sliders, update_range_button)
widgets = row(
    date_widgets,
    Spacer(width_policy='max'),
    column(
        Spacer(width_policy='max'), 
        plot_select),
    width_policy='max'
)

layout = column(title, widgets, plot, width_policy='max')

# Show to current document/page
curdoc().add_root(layout)
curdoc().title = "Historical Solar Forecast Plot"