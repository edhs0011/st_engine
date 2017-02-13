import pandas as pd

def to_argus(df):
    col_name = "StartTime,Dur,Proto,SrcAddr,Sport,Dir,DstAddr,Dport,State,sTos,dTos,TotPkts,TotBytes".split(",")
    df[col_name[0]] = pd.to_datetime(df["unix_secs"], unit='s').dt.strftime('%Y/%m/%d %H:%M:%S.%f')
    df[col_name[1]] = df["last"] - df["first"]
    rename = {
        "prot": col_name[2],
        "srcaddr": col_name[3],
        "srcport": col_name[4],
        "dstaddr": col_name[6],
        "dstport": col_name[7],
        "dpkts": col_name[11],
        "doctests": col_name[12]
    }
    df.rename(columns=rename, inplace=True)
    df = df.ix[:, col_name]
    for line in df.to_csv(index=False).split("\n"):
        yield line