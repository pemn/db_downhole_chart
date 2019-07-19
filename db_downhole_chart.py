#!python
# Copyright 2019 Vale
# create a custom downhole chart showing the lito and grades
# input: database with holes
# holeid: variable with hole name
# from: hole interval start
# to: hole interval end
# lito: variable with lithology
# variables: each of the grades variables to be ploted alongside lito
# scd: vulcan format legend file, containg color palete and a legend with same name as lito
# output_path: (optional) charts will be saved to a file on this path
# output_window: (optional) render the output chart on a window
# page_charts: how many charts will each page contain
# v1.0 09/2018 paulo.ernesto
'''
usage: $0 input_path*csv,isis,xlsx,xlsm condition holeid:input_path from:input_path to:input_path lito:input_path variables#variable:input_path scd*scd output_path*pdf output_window@ page_charts=6
'''
import sys, os.path
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.ticker as mticker
import matplotlib.patches as mpatches
import matplotlib.collections as mcollections
from matplotlib.backends.backend_pdf import PdfPages

# import modules from a pyz (zip) file with same name as scripts
sys.path.append(os.path.splitext(sys.argv[0])[0] + '.pyz')

from _gui import usage_gui, pd_load_dataframe, table_field, smartfilelist

from vulcan_mapfile import VulcanScd

def plot_downhole(df, hid, gs, col, v_from, v_to, v_lito, variables, lito_rgb, v_minmax = None):
    if df.ndim == 1:
      df = pd.DataFrame([df], columns=df.index)
    mid_points = (df[v_from].values + df[v_to].values) / 2.0
    df.reset_index(inplace=True)
    ax = gs[0][col]
    ax.grid(True, 'both', 'y')
    ax.tick_params(axis='both', which='both', bottom=False, labelbottom=False, labelsize='small')
    ax.set_title(hid)
    if v_minmax is not None:
      ax.set_ylim(v_minmax[0][1], v_minmax[0][0])
    else:
      ax.set_ylim(np.max(mid_points), 0)

    for row in df.index:
      ax.bar(0, df.loc[row, v_to] - df.loc[row, v_from], 0.5, df.loc[row, v_from], color=lito_rgb[df.loc[row, v_lito]])

    for i in range(len(variables)):
      ax = gs[i + 1][col]
      ax.grid(True, 'both', 'y')
      ax.tick_params(axis='both', which='both', bottom=False, labelbottom=False, top=True, labeltop=True, labelsize='small')
      ax.set_xlabel(variables[i])
      ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.2f"))
      ax.plot(df[variables[i]], mid_points)
      if v_minmax is not None:
        ax.set_ylim(v_minmax[0][1], v_minmax[0][0])
        ax.set_xlim(v_minmax[i+1][0], v_minmax[i+1][1])
      else:
        ax.set_ylim(np.max(mid_points), 0)

def db_downhole_chart(input_path, condition, v_hid, v_from, v_to, v_lito, variables, scd, output_path, output_window, page_charts):
  lito_rgb = VulcanScd(scd, 'DRILL_COLOUR', v_lito)
  if int(page_charts) < 1:
    page_charts = 1
  else:
    page_charts = int(page_charts)
  
  variables = list(filter(len, variables.split(';')))

  idf = pd_load_dataframe(input_path, condition, None, [v_hid, v_from, v_to, v_lito] + variables)
  
  idf.set_index(v_hid, inplace=True)

  hid_count = len(idf.index.unique())

  page_cols = min(page_charts, hid_count)

  pdf = PdfPages(output_path)
  pagec = 0

  # 11.69,8.27
  # print(plt.rcParams["figure.figsize"])
  fig = None
  lito_legend = [mpatches.Patch(color=lito_rgb[_], label=_) for _ in idf[v_lito].unique()]
  v_minmax = [(idf[_].min(), idf[_].max()) for _ in [v_to] + variables]
  for hid in idf.index.unique():
    if pagec % page_cols == 0:
      if pagec:
        pdf.savefig()
      if pagec < hid_count:
        fig, gs = plt.subplots(len(variables) + 1, page_cols, sharey=True, figsize=np.multiply(plt.rcParams["figure.figsize"], 2))
        fig.legend(handles=lito_legend, labels=[_.get_label() for _ in lito_legend])

    print(hid)
    plot_downhole(idf.loc[hid], hid, gs, pagec % page_cols, v_from, v_to, v_lito, variables, lito_rgb, v_minmax)
    
    pagec += 1
  
  if pagec % page_cols == 0:
    pdf.savefig()
    
  pdf.close()

  if (int(output_window)):
    plt.show(True)

main = db_downhole_chart

if __name__=="__main__":
  usage_gui(__doc__)
