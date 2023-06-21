## 📌 Description
Este script integra várias etapas já existentes em uma solução simples para comparação entre arquivos las e assay.
As etapas feitas anteriormente e que foram integradas são:
 1. Concatenar os arquivos las de cada furo em um arquivo só (db_las_export_table.py, db_append.py)
 2. Juntar os dados da etapa anterior com o arquivo ASSAY (db_join_interval.py)
 3. Criar o gráfico do furo (db_downhole_chart.py)
## 📸 Screenshot
![screenshot1](./assets/db_downhole_las_x_assay1.png)
## 📝 Parameters
|Name|optional|description|
|---|---|---------|
||❎||
||☑️||
## Notes
 - A curva DEPT (ou DEPTH) tem que ser a primeira da lista curves.
 - A operação interval join é pesada, então para testes é recomendável usar arquivos ASSAY pequenos com poucos
furos (< 10). E selecionar apenas os arquivos LAS destes.
## 📚 Examples
![screenshot2](./assets/db_downhole_las_x_assay2.png)
## 💎 License
Apache 2.0