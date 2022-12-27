import pandas as pd

file = 'schoolData.csv'

def searchInput() -> str:
    school = input('Enter the name of your school: ')
    return school

def searchFor(file: str, search: str) -> pd.DataFrame:
    df = pd.read_csv(file)
    df = df[df['School'].str.contains(search, case=False)]
    schoolList = list(df['School'])
    if len(schoolList) == 0:
        print('\nNo Results Found. Make sure spelling is correct and try again.\n')
        main()
    else:
        possible_matches = df['School'].str.fullmatch(search, case=False)
        for index, value in enumerate(possible_matches):
            if value == True:
                print(df.iloc[index])
                return df.iloc[index]['sid']
        choice = chooseSchool(schoolList)
        print(df.iloc[int(choice)])
        return df.iloc[int(choice)]['sid']

def chooseSchool(options: list):
    print(f'Your search matched {len(options)} school(s):')
    for number, school in enumerate(options):
        print(f'{number} -- {school}','\n')
    choice = input('Enter the number of the school you would like to use (Enter "none" to search again): ')
    if choice == 'none':
        main()
    else:
        return choice

def main():
    search = searchInput()
    return searchFor(file, search)

if __name__ == '__main__':
    main()
    exit(0)