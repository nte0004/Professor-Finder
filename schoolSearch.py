import pandas as pd

file = 'schoolData.csv'
def findMatch(search: str):
    df = pd.read_csv(file)
    df = df[df['School'].str.contains(search, case=False)]
    possibleMatch = df['School'].str.fullmatch(search, case=False)
    for index, value in enumerate(possibleMatch):
        if value == True:
            sid = str(df.iloc[index]['sid'])
            status = str('Match Found')
            return status, sid
    schoolList = list(df['School'])
    sidList = list(df['sid'])
    return schoolList, sidList