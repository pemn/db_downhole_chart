#!python
# create a custom downhole chart showing the lito and grades
# Copyright 2019 Vale
# input: database with holes
# holeid: variable with hole name
# from: hole interval start
# to: hole interval end
# lito: variable with lithology
# variables: each of the grades variables to be ploted alongside lito
# lito_rgb: excel with lito colors
# output: (optional) path to save pdf file with charts
# display: (optional) render the output chart on a window
# page_charts: how many charts will each page contain
# v2.0 12/2021 paulo.ernesto
# v1.0 09/2018 paulo.ernesto
'''
usage: $0 input_path*csv,isis,xlsx,xlsm condition holeid:input_path from:input_path to:input_path lito:input_path variables#variable:input_path lito_rgb*xlsx output*pdf display@ page_charts=6
'''
import sys, os.path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.ticker as mticker
import matplotlib.patches as mpatches
import matplotlib.collections as mcollections
from matplotlib.backends.backend_pdf import PdfPages

# import modules from a pyz (zip) file with same name as scripts
sys.path.insert(0, os.path.splitext(sys.argv[0])[0] + '.pyz')

from _gui import usage_gui, commalist, pd_load_dataframe, log

def plot_downhole(df, hid, gs, col, v_from, v_to, v_lito, variables, df_rgb, v_minmax = None, v_rgb = 'rgb'):
    if df.ndim == 1:
      df = pd.DataFrame([df], columns=df.index)
    mid_points = (df[v_from].values + df[v_to].values) / 2.0
    df.reset_index(inplace=True)
    ax = gs.flat[col]
    ax.grid(True, 'both', 'both')

    ax.set_title(hid)
    if v_minmax is not None:
      ax.set_ylim(v_minmax[0][1], v_minmax[0][0])
    else:
      ax.set_ylim(df[v_to].max(), 0)

    rgb = [df_rgb.loc[_].iloc[0] if _ in df_rgb.index else 'w' for _ in df[v_lito].str.lower()]
    for i in range(len(variables)):
      ax.plot(df[variables[i]], mid_points, label = variables[i])
    if len(variables):
      ax.legend()
    x0, x1 = ax.get_xlim()
    barx = np.asfarray(df[v_to] - df[v_from])
    barw = (x1 - x0) * .2
    barh = np.full(barx.size, x0 - barw)
    ax.bar(barh, barx, barw, df[v_from], color=rgb, xerr=0.2)

def db_downhole_chart(input_path, condition, v_hid, v_from, v_to, v_lito, variables, lito_rgb, output, display, page_charts = 6):
  v_hid = v_hid or 'hid'
  v_from = v_from or 'from'
  v_to  = v_to or 'to'
  df_rgb = pd_load_dataframe(lito_rgb)
  if not df_rgb.empty:
    df_rgb = df_rgb.set_index(df_rgb.columns[0])

  if int(page_charts) < 1:
    page_charts = 1
  else:
    page_charts = int(page_charts)
  
  if variables:
    variables = commalist().parse(variables).split()
  else:
    variables = []

  idf = pd_load_dataframe(input_path, condition, None, [v_hid, v_from, v_to, v_lito] + variables)
  
  idf.set_index(v_hid, inplace=True)

  hid_count = len(idf.index.unique())

  page_cols = min(page_charts, hid_count)
  pdf = None
  if output:
    pdf = PdfPages(output)
  pagec = 0

  fig = None
  lito_legend = [mpatches.Patch(color=df_rgb.loc[_].iloc[0], label=_) for _ in idf[v_lito].str.lower().unique() if _ in df_rgb.index]
  v_minmax = [(idf[_].min(), idf[_].max()) for _ in [v_to] + variables]
  for hid in idf.index.unique():
    if pagec % page_cols == 0:
      if pagec and pdf is not None:
        pdf.savefig()
      if pagec < hid_count:
        fig, gs = plt.subplots(1, page_cols, sharey=True, figsize=np.multiply(plt.rcParams["figure.figsize"], 2), squeeze=False)
        fig.legend(handles=lito_legend, labels=[_.get_label() for _ in lito_legend])
        if pagec + page_cols > hid_count:
          for i in range(hid_count - pagec, gs.size):
            gs.flat[i].set_axis_off()

    log(hid)
    plot_downhole(idf.loc[hid], hid, gs, pagec % page_cols, v_from, v_to, v_lito, variables, df_rgb, v_minmax)
    
    pagec += 1

  if pdf is not None:
    pdf.savefig()
    pdf.close()

  if int(display):
    plt.show()

main = db_downhole_chart

if __name__=="__main__":
  usage_gui(__doc__)
