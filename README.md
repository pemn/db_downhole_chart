# db_downhole_chart
create charts showing downhole geology+grades of mining drillholes

## Description
Downhole charts are a common type of visualization for drillhole data. Those charts allow for a quick glipse of the information contained on the intervals. Many proprietary softwares already have bult-in tools for generating those charts, but open source tools are not available.  

## how to use
The required files is the assay database with intervals and a palete and legend file. 

## Palete and legend colors
The SCD file containing the palete and legend is in a proprietary format. Its a simple ASCII file formated with a proprietary DSL similar to JSON. It may may be adapted to your data, but may be easier to adapt the code to read palete and legends from other sources. Rather than a fork, it would be a good idea to detect the extension of the palette file and handle it in a similar way with a drop in replacement for the VulcanScd class.

## Result screenshot
![screenshot2](https://github.com/pemn/db_downhole_chart/blob/master/assets/screenshot2.png)
## Panel
![screenshot1](https://github.com/pemn/db_downhole_chart/blob/master/assets/screenshot1.png)
