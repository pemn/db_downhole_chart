# db_downhole_chart
## 📌 Description
create charts showing downhole geology+grades of mining drillholes   
also included in the repository some variations that fulfill specific purposes  
Downhole charts are a common type of visualization for drillhole data. Those charts allow for a quick glipse of the information contained on the intervals. Many proprietary softwares already have bult-in tools for generating those charts, but open source tools are not available.  
## how to use
The required files is the assay database with intervals and rgb color table file. 
## 📸 Screenshot
![screenshot1](https://github.com/pemn/assets/blob/main/db_downhole_chart1.png?raw=true)  
## 📝 Parameters
name|optional|description
---|---|------
input|❎|database with holes
holeid|❎|variable with hole name
from|❎|hole interval start
to|❎|hole interval end
lito|☑️|variable with lithology
variables|☑️|each of the grades variables to be ploted alongside lito
lito_rgb|❎|excel with lito colors
output|☑️|path to save pdf file with charts
display|☑️|render the output chart on a window
page_charts|☑️|how many charts will each page contain
## 📓 Notes
### lito_rgb file example
lito|rgb
---|---
ore|#0000FF
waste|#FF0000
overburden|#00FF00
etc|#FFFFFF

## 📚 Examples
![screenshot2](https://github.com/pemn/assets/blob/main/db_downhole_chart2.png?raw=true)  
## 🧩 Compatibility
distribution|status
---|---
![winpython_icon](https://github.com/pemn/assets/blob/main/winpython_icon.png?raw=true)|✔
![vulcan_icon](https://github.com/pemn/assets/blob/main/vulcan_icon.png?raw=true)|❓
![anaconda_icon](https://github.com/pemn/assets/blob/main/anaconda_icon.png?raw=true)|❌
## 💎 License
Apache 2.0


