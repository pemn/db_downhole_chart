## 📌 Description
compare a drillhole to its nearest neighbor  
create a downhole chart and/or a interval join of each pair
## 📸 Screenshot
![screenshot1](./assets/db_downhole_compare_twin1.png)
## 📝 Parameters
Name|optional|description
---|---|------
data|❎|path to a structured data file in a supported format
condition|☑️|python expression to limite records which will be used
hid|❎|field with hole unique identifier
x,y,z|❎|fields x,y,z coordinates of the sample mid
from,to|❎|assay intervals for downhole chart
lito|❎|lithology variable for color in downhole chart
group|☑️|holes that share the same group value will not be paired together
distance|❎|the nearest holes up to this maximum distance will be paired
lito_rgb|❎|path to structured data with lito rgb colors
output_csv|☑️|path to save the structured table with joined data
output_pdf|☑️|path to save a pdf with downhole chart
display||show the downhole chart in a graphic window

## 📓 Notes
 - If data does not yet has midx,midy,midz but you have the header and assay, you can use the script db_desurvey_straight.py
 - If the twins are in separated files, you should concatenate the files manually or using script db_append.py
## 📚 Examples
### downhole chart
![screenshot2](./assets/db_downhole_compare_twin2.png)
### join table
![screenshot3](./assets/db_downhole_compare_twin3.png)
### lito rgb file format example
lito|rgb
---|---
if|#0000FF
hf|#FF0000
cg|#00FF00

## 💎 License
Apache 2.0