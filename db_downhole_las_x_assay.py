#!python
# merge description and geophysics data
# create downhole chart comparing lito and curves
# input_assay: path to assay data file in a supported format
# input_las: multiple las files corresponding to the holes in ASSAY
# curves: select data columns. DEPTH or equivalent must be the first.
# output_data: path to save a file with the joined assay and las data
# downhole_chart: create a chart showing the selected curve
# v1.0 2022/04 paulo.ernesto
'''
usage: $0 input_assay*csv,xlsx,xlsm hid:input_assay from:input_assay to:input_assay input_las#las*las curves#curve:input_las output_data*csv,xlsx downhole_chart@5 lito:input_assay variables#variable:input_assay lito_rgb*xlsx output_pdf*pdf display@
'''
import sys, os.path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# import modules from a pyz (zip) file with same name as scripts
sys.path.insert(0, os.path.splitext(sys.argv[0])[0] + '.pyz')

from _gui import usage_gui, pd_load_dataframe, pd_save_dataframe, commalist, log

import lasio
from db_join_interval import pd_join_interval
from db_create_from_to import pd_create_from_to
from db_downhole_chart import db_downhole_chart

def las_get_curve(las, v):
  c = las.get_curve(v)
  d = c.data
  if d.dtype.num >= 19:
    d = np.asfarray(d)
  return d

def db_downhole_las_x_density(input_assay, v_hid, v_from, v_to, input_las, curves, output_data, downhole_chart, v_lito, v_data, lito_rgb, output_pdf, display):
  vl = commalist().parse(curves).split()
  df_assay = pd_load_dataframe(input_assay)
  df_las = pd.DataFrame()
  for fp in commalist().parse(input_las).split():
    f,c = lasio.open_file(fp, autodetect_encoding_chars=-1)
    las = lasio.read(f)
    dl = [las_get_curve(las, v) for v in vl]
    df = pd.DataFrame(np.stack(dl, 1), columns=vl)
    df[v_hid] = las.well.well.value
    df_las = df_las.append(df)

  pd_create_from_to(df_las, v_hid, vl[0], True)

  v_lut = [{'hid': v_hid, 'from': v_from, 'to': v_to}, {'hid': v_hid, 'from': 'from', 'to': 'to'}]
  # preprocess datasets keeping only holes that exists in both
  # to speed up the expensive join_interval step
  s = set(df_assay[v_hid]).intersection(df_las[v_hid])
  bi = df_assay[v_hid].isin(s)
  if not np.all(bi):
    df_assay = df_assay.loc[bi]
  log("preprocess optimization: %d rows removed from assay" % np.sum(np.equal(bi, 0)))
  bi = df_las[v_hid].isin(s)
  if not np.all(bi):
    df_las = df_las.loc[bi]
  log("preprocess optimization: %d rows removed from las" % np.sum(np.equal(bi, 0)))

  df_join = pd_join_interval([df_assay, df_las], v_lut)

  if output_data:
    pd_save_dataframe(df_join, output_data)

  if int(downhole_chart):
    log("downhole_chart")
    vl.pop(0)
    for v in commalist().parse(v_data).split():
      if v:
        vl.append(v)
    db_downhole_chart(df_join, '', None, None, None, v_lito, str(commalist(vl)), lito_rgb, output_pdf, display)
  log("finished")


main = db_downhole_las_x_density

if __name__=="__main__":
  usage_gui(__doc__)
