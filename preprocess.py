import pandas as pd

def load_csv_data(file_path, print=False):
    df = pd.read_csv(file_path)
    df['valid_time'] = pd.to_datetime(df['valid_time'])
    print(f"    Number of rows in the dataset:", len(df)) if print else None
    # drop number and surface columns
    df.drop(columns=['number', 'surface'], inplace=True)
    # check if there are any missing values in the dataset
    print(f"    Missing values in the dataset:", df.isnull().sum().sum()) if print else None
    # drop any rows with missing values
    df.dropna(inplace=True)
    print(f"    Number of rows after dropping missing values:", len(df)) if print else None
    # check if there are any duplicate rows by valid_time and take mean of duplicates
    df = df.groupby('valid_time').mean().reset_index()
    return df

def create_data_for_years(years, csv_data):
    all_years_df = pd.DataFrame()
    for year in years:
        print(f"Loading data for year: {year}")
        file_path = csv_data + f"era5_{year}.csv"
        year_df = load_csv_data(file_path)
        all_years_df = pd.concat([all_years_df, year_df], ignore_index=True)
    
    all_years_df = all_years_df.sort_values(by='valid_time')
    all_years_df.reset_index(drop=True, inplace=True)
    all_years_df['valid_time'] = pd.to_datetime(all_years_df['valid_time'])
    all_years_df['year'] = all_years_df['valid_time'].dt.year
    all_years_df['month'] = all_years_df['valid_time'].dt.month
    all_years_df['day'] = all_years_df['valid_time'].dt.day
    all_years_df['hour'] = all_years_df['valid_time'].dt.hour
    all_years_df['minute'] = all_years_df['valid_time'].dt.minute
    all_years_df['second'] = all_years_df['valid_time'].dt.second

    for freq, cols in [('year', ['yearly_mean', 'yearly_max', 'yearly_min', 'yearly_std', 'yearly_var']),
                    (['year', 'month'], ['monthly_mean', 'monthly_max', 'monthly_min', 'monthly_std', 'monthly_var']),
                    (['year', 'month', 'day'], ['daily_mean', 'daily_max', 'daily_min', 'daily_std', 'daily_var'])]:
        for col, stat in zip(cols, ['mean', 'max', 'min', 'std', 'var']):
            all_years_df[col] = all_years_df.groupby(freq)['tp'].transform(stat)
    
    return all_years_df

csv_data = './data/era5/'
save_path = './data/'

# train_years = range(2011, 2021)
# train_data = create_data_for_years(train_years, csv_data)
# train_data.to_csv(save_path + 'train_data.csv', index=False)

val_years = range(2021, 2023)
val_data = create_data_for_years(val_years, csv_data)
val_data.to_csv(save_path + 'val_data.csv', index=False)

test_years = range(2023, 2025)
test_data = create_data_for_years(test_years, csv_data)
test_data.to_csv(save_path + 'test_data.csv', index=False)

print(f"Train, validation, and test datasets saved to {save_path}.")
print("Preprocessing completed.")