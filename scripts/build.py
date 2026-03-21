# Cook County Cooks Build Script - see README for full version
import pandas as pd
import json, os, glob
from datetime import datetime

def col(l):
    l = l.upper()
    r = 0
    for c in l: r = r * 26 + ord(c) - ord('A') + 1
    return r - 1

JEFFREY = 'Jeffrey Bilbrey'

def find_excel():
    for p in ['data/Blufox_-_Sales_Report_*.xlsx','data/*.xlsx']:
        f = glob.glob(p)
        if f: return max(f, key=os.path.getmtime)
    raise FileNotFoundError("No Excel file in data/")

def parse_stores(fp):
    df = pd.read_excel(fp, sheet_name='Store Rank', header=None).iloc[7:]
    df.columns = range(len(df.columns))
    rs = []
    for _,r in df[df[4]==JEFFREY].iterrows():
        dm = 'None'
        if 'Fear' in str(r[5]): dm='Fear'
        elif 'Cabrales' in str(r[5]): dm='Cabrales'
        elif 'Brooks' in str(r[5]): dm='Brooks'
        def v(c,d=4):
            try: return round(float(r[c] or 0),d)
            except: return 0
        rs.append({'rank':int(r[0] or 0),'s':str(r[2]),'dm':dm,'gp_trend':v(col('M'),2),'mcr':v(col('V')),'fcr':v(col('X')),'nt':v(col('AB')),'gig':v(col('BJ')),
                   'mob':int(v(col('BL'),0)),'tab':int(v(col('BM'),0)),-watch':int(v(col('BN'),0)),'prem':v(col('BT')),'n2u':v(col('BY')),'apd':v(col('CJ'),2),'nps':v(col('CM')),'sc':v(col('DO'),1),'gp':v(7,2)})
    return rs

def parse_reps(fp,ss):
    df = pd.read_excel(fp,sheet_name='Rep Rank',header=None).iloc[5:]
    df.columns = range(len(df.columns))
    bs={}
    for _,r in df[df[3].isin(ss)].iterrows():
        st=str(r[3])
        if st not in bs: bs[st]=[]
        def v(c,d=4):
            try: return round(float(r[c] or 0),d)
            except: return 0
        bs[st].append({'natrank':int(v(col('A'),0)),'name':str(r[col('B')]),'store':st,'gp':v(col('G'),2),'gig':v(col('L')),'prem':v(col('U')),'acc':v(col('AD'),2)})
    for st in bs: bs[st].sort(key=lambda x:-x['gp'])
    return bs

def main():
    fp=find_excel()
    st=parse_stores(fp)
    rp=parse_reps(fp,{s['s'] for s in st})
    lg=open('scripts/logo.b64').read().strip() if os.path.exists('scripts/logo.b64') else ''
    html=open('scripts/template.html').read()
    html=html.replace('LOGO_SRC',lg).replace('SD_PLACE@HOLDER',json.dumps(st)).replace('RD_PLACE@HOLDER',json.dumps(rp)).replace('REPORT_DATE',datetime.now().strftime('%B %d, %Y'))
    open('index.html','w').write(html)
    print(f"Done! {len(st)} stores, {sum(len(v) for v in rp.values())} reps")

if __name__==' __main__': main()
