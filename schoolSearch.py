import pandas as pd

def searchInput():
    school = input('Enter the name of your school: ')
    return school

def searchFor(file, search):
    df = pd.read_csv(file)
    df = df[df['School'].str.contains(search, case=False)]
    return df

def chooseSchool(options):
    print(f'Your search matched {len(options)} school(s):')
    for number, school in enumerate(options):
        print(number, school)
    choice = input('Enter the number of the school you would like to use (Enter "none" to search again): ')
    if choice == 'none':
        main()
    else:
        return int(choice)

def main():
    file = 'schoolData.csv'
    search = searchInput()
    results = searchFor(file, search)
    options = list(results['School'])
    choice = chooseSchool(options)
    return results.iloc[choice]['sid']

if __name__ == '__main__':
    main()
    exit(0)