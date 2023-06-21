#!python
# compare drillholes to their nearest neighbor, within a distance
# data: path to input data in a supported format
# condition: (optional) python expression to filter data
# hid: field with hole id
# x,y,z: fields with hole collar midx,midy,midy coordinates
# from,to: fields with interval
# lito: field with lito
# group: (optional) only match twins that have a different value on this field
# distance: only match twins withing this distance
# lito_rgb: a xlsx file with the color legend in downhole format
# lsx output_csv*csv,xlsx output_pdf*pdf display@
# v1.0 05/2022 paulo.ernesto
'''
usage: $0 data*csv,xlsx condition hid:data x:data y:data z:data from:data to:data lito:data group:data distance=10 lito_rgb*xlsx output_csv*csv,xlsx output_pdf*pdf display@
'''

import sys, os.path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_pdf import PdfPages
from sklearn.metrics import pairwise_distances
from itertools import permutations

# import modules from a pyz (zip) file with same name as scripts
sys.path.insert(0, os.path.splitext(sys.argv[0])[0] + '.pyz')

from _gui import usage_gui, pd_load_dataframe, pd_save_dataframe, log
from db_join_interval import pd_join_interval

from round_robin import round_robin

def pd_twin_table(df, tk, v_hid, v_from, v_to):
  v_lut = [{},{}]
  v_lut[0]['hid']  = v_hid  or 'hid'
  v_lut[1]['hid']  = v_hid  or 'hid'
  v_lut[0]['from'] = v_from or 'from'
  v_lut[1]['from'] = v_from or 'from'
  v_lut[0]['to']   = v_to   or 'to'
  v_lut[1]['to']   = v_to   or 'to'

  r = pd.DataFrame()
  for r0, r1, d in tk:
    df0 = df.loc[r0]
    df1 = df.loc[r1].rename(lambda _: _ if _ in v_lut[1].values() else _ + '_nn', axis=1)
    df1[v_hid] = r0
    df2 = pd_join_interval([df0, df1], v_lut)
    df2['d_nn'] = d
    df2[v_hid] = r0
    df2[v_hid + '_nn'] = r1
    r = r.append(df2)
  return r.reset_index(drop=True)

def pd_near_distance(df_xyz, distance = None):
  if distance:
    distance = float(distance)
  else:
    distance = 10.0
  t = dict()
  if df_xyz.index.nlevels > 1:
    rr_n = round_robin(len(df_xyz.index.levels[0]), True)
    rr_i = np.take(np.asarray(df_xyz.index.levels[0]), rr_n)
    for n0,n1 in rr_i:
      df0 = df_xyz.loc[n0]
      df1 = df_xyz.loc[n1]
      d = pairwise_distances(df0, df1)
      for di in range(d.shape[0]):
        for dj in range(d.shape[1]):
          if d[di,dj] <= distance:
            fi = df0.index[di]
            fj = df1.index[dj]
            if fi != fj:
              fij = tuple(sorted((fi,fj)))
              if fij not in t or d[di,dj] < t[fij]:
                t[fij] = d[di,dj]
    return [k + (v,) for k,v in t.items()]
  else:
    d = pairwise_distances(df_xyz)
    for di in range(d.shape[0]):
      for dj in range(d.shape[1]):
        if d[di,dj] <= distance:
          if di == dj:
            continue
          ij = tuple(sorted((di,dj)))
          if ij not in t or d[di,dj] < t[ij]:
            t[ij] = d[di,dj]
    return [(df_xyz.index[_[0]], df_xyz.index[_[1]], t[_]) for _ in t.keys()]


def pd_twin_chart(df, tk, df_rgb, v_from, v_to, v_lito, pdf, page_size = None):
  mid_points = (df[v_from].values + df[v_to].values) / 2.0

  rgb = None

  if df_rgb is not None:
    rgb = [df_rgb.loc[_].iloc[0] if _ in df_rgb.index else 'w' for _ in df[v_lito].str.lower()]
  lito_legend = [mpatches.Patch(color=df_rgb.loc[_].iloc[0], label=_) for _ in df[v_lito].str.lower().unique() if _ in df_rgb.index]

  n0 = 0
  n1 = len(tk)
  if page_size is not None and n1 > page_size:
    n1 = page_size
  while True:
    plt.figure(tight_layout=True)
    #plt.grid(True, 'both', 'both')
    plt.grid(True, 'major', 'both')
    xtn = []
    for i in range(n0,n1):
      r0, r1, d = tk[i]
      n = n1 - n0
      for j in range(2):
        rx = tk[i][j]
        dfx = df.loc[rx]
        if np.ndim(dfx) == 1:
          dfx = pd.DataFrame.from_records([dfx])
        plt.bar(np.full(len(dfx), i - n0 + 0.25 + 0.5 * j), dfx[v_to] - dfx[v_from], 0.4, dfx[v_from], color=rgb)
        xtn.append(rx)
      else:
        plt.text(i - n0 + 0.4, np.max(dfx[v_from]) / 2, '⇱ %d m ⇲' % d, rotation='vertical')

    #plt.gca().tick_params('x', which='minor', grid_linestyle='--')
    #plt.gca().tick_params('x', which='major', grid_linewidth=2, grid_linestyle='-')
    #plt.gca().tick_params('y', which='both', grid_linestyle='--')
    plt.gca().set_xticks(range(n))
    plt.gca().set_xticklabels([''] * n)
    plt.gca().set_xticks(np.linspace(0.25, n-0.25, len(xtn), True), minor=True)
    plt.gca().set_xticklabels(xtn, minor=True)

    plt.gcf().legend(handles=lito_legend, labels=[_.get_label() for _ in lito_legend])
    if pdf:
      pdf.savefig()

    if n1 < len(tk):
      n0 = n1
      n1 = min(len(tk), n1 + page_size)
    else:
      break

def db_downhole_compare_twin(data, condition, v_hid, v_x, v_y, v_z, v_from, v_to, v_lito, v_group, distance, lito_rgb, output_csv, output_pdf, display):
  df = pd_load_dataframe(data, condition)
  df.set_index(v_hid, drop=False, inplace=True)
  df_rgb = pd_load_dataframe(lito_rgb)
  if df_rgb is not None:
    df_rgb = df_rgb.set_index(df_rgb.columns[0])
  df_xyz = pd.DataFrame()
  for ri in df.index.unique():
    if not ri or pd.isnull(ri):
      continue
    rd = df.loc[ri, [v_x, v_y, v_z]]
    if np.ndim(rd) > 1:
      rd = rd.iloc[0]
    if v_group:
      g = df.loc[ri, v_group]
      if np.ndim(g) > 0:
        g = g.iloc[0]
      rd.name = (g, rd.name)
    df_xyz = df_xyz.append(rd)
  if v_group:
    df_xyz = df_xyz.reindex(pd.MultiIndex.from_tuples(df_xyz.index))

  tk = pd_near_distance(df_xyz, distance)

  if len(tk) == 0:
    s = "no twin holes found within the distance"
    print(s)
    if int(display):
      plt.axis('off')
      plt.text(0.0, 0.5, s)
      plt.show()
    return

  pdf = None
  if output_pdf:
    pdf = PdfPages(output_pdf)

  if pdf or int(display):
    pd_twin_chart(df, tk, df_rgb, v_from, v_to, v_lito, pdf, 6)

    if pdf:
      pdf.close()
    
    if int(display):
      plt.show()

  if output_csv:
    pd_save_dataframe(pd_twin_table(df, tk, v_hid, v_from, v_to), output_csv)


main = db_downhole_compare_twin

if __name__=="__main__":
  usage_gui(__doc__)
