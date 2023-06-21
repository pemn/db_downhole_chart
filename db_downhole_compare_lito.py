#!python
# create downhole charts comparing multiple lito fields
# all lito fields must be on the same table
# mode:
# - series: a single chart where each lito variable is a bar
# - charts: one chart for each lito variable
# Copyright 2021 Vale
# v1.0 12/2021 paulo.ernesto
'''
usage: $0 data*csv,xlsx condition holeid:data from:data to:data litos#lito:data lito_rgb*xlsx mode%series,charts output_path*pdf display@
'''
import sys, os.path
import pandas as pd
import numpy as np
import math
from matplotlib.backends.backend_pdf import PdfPages

# import modules from a pyz (zip) file with same name as scripts
sys.path.append(os.path.splitext(sys.argv[0])[0] + '.pyz')

from _gui import usage_gui, pd_load_dataframe
from pbi_downhole import pd_downhole_charts, pd_downhole_series


def db_downhole_compare_lito(input_path, condition, v_hid, v_from, v_to, v_lito, lito_rgb, mode, output_path, display):
  if not mode:
    mode = 'series'

  df = pd_load_dataframe(input_path, condition)
  df_rgb = pd_load_dataframe(lito_rgb)

  pdf = None
  if output_path:
    pdf = PdfPages(output_path)

  r = n = 10
  s = 0
  while r == n:
    if mode == 'series':
      r = pd_downhole_series(df, v_hid, v_from, v_to, v_lito, df_rgb, display, pdf, n, s)
    if mode == 'charts':
      r = pd_downhole_charts(df, v_hid, v_from, v_to, v_lito, df_rgb, display, pdf, n, s)
    s += r

  if pdf:
    pdf.close()

main = db_downhole_compare_lito

if __name__=="__main__":
  usage_gui(__doc__)
