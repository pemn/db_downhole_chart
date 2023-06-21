## 📌 Description
create downhole charts comparing multiple lito fields
## 📸 Screenshot
![screenshot1](./assets/db_downhole_compare_lito1.png)
## 📝 Parameters
|Name|optional|description|
|---|---|---------|
|data|❎|tabular data in one of the supported file formats|
|condition|☑️|python syntax expression to filter data|
|holeid|❎|field with hole unique indentifier|
|from|❎|field with interval start|
|to|❎|field with interval end|
|litos|❎|list of fields with lito value|
|lito_rgb|❎|path to excel table with rgb color for each lito value|
|mode||how the comparison between each lito will be presented|
|output_path|☑️|path to save the result|
|display||show the result in a new window|
## 📓 Notes
## 📚 Examples
### mode: series
![screenshot2](./assets/db_downhole_compare_lito2.png)
### mode: chart
![screenshot3](./assets/db_downhole_compare_lito3.png)
## 💎 License
Apache 2.0