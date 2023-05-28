import pandas as pd

file = 'schoolData.csv'
def findMatch(search: str):
    df = pd.read_csv(file)
    df = df[df['School'].str.contains(search, case=False)] #All school names that contain the search string within it
    possibleMatch = df['School'].str.fullmatch(search, case=False) #Series of bools if search string is complete match it is true.
    # Return sid of school to be used by RateMyProfessor.py
    for index, value in enumerate(possibleMatch):
        if value == True:
            sid = str(df.iloc[index]['sid'])
            status = str('Match Found')
            return status, sid
    # Return list of sid and list of school names for rmp-gui to get user selection of the correct school
    schoolList = list(df['School'])
    sidList = list(df['sid'])
    return schoolList, sidList