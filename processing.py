import logging
import pandas as pd
import sys


CLIENT_INFO_NAME = "dataset_one"
CLIENT_FINANCIAL_NAME = "dataset_two"
CLIENT_INFORMATION_DF_COLUMNS = {"id", "email"}
CLIENT_FINANCIAL_DF_COLUMNS = {"id", "btc_a", "cc_t"}
NECESSARY_COLUMNS = {
    CLIENT_INFO_NAME: CLIENT_INFORMATION_DF_COLUMNS,
    CLIENT_FINANCIAL_NAME: CLIENT_FINANCIAL_DF_COLUMNS,
}
DEFAULT_FILTER_COUNTRY = ["United Kingdom", "Netherlands"]
FILTER_BY = "country"
TABLES_MERGED_ON = {"left_on": "id", "right_on": "id"}
OUTPUT_COLUMN_NAMES_MAPPER = {
    "id": "client_identifier",
    "btc_a": "bitcoin_address",
    "cc_t": "credit_card_type",
}
OUTPUT_FILE_NAME = "client_data.csv"


def prepare_data(config):
    client_information, client_financial, countries = get_settings_from_config(config)
    df1, df2 = read_datasets_from_csvs(client_information, client_financial)
    df1 = verify_and_clean_data(CLIENT_INFO_NAME, df1, countries)
    df2 = verify_and_clean_data(CLIENT_FINANCIAL_NAME, df2)
    df = get_merged_dataset(df1, df2)
    df = get_properly_named_columns(df)
    save_output_dataset_to_the_file(df)


def get_settings_from_config(config):
    client_information = (
        config["client_info_path"] if not config["default"] else CLIENT_INFO_NAME
    )
    client_financial = (
        config["client_financial_path"]
        if not config["default"]
        else CLIENT_FINANCIAL_NAME
    )
    countries = config["countries"] if not config["default"] else DEFAULT_FILTER_COUNTRY
    logging.info(
        f"Start processing for db from paths: {client_information}, {client_financial}, and filter by: {countries}"
    )
    return client_information, client_financial, countries


def read_datasets_from_csvs(first_path, second_path):
    df1 = create_data_frame(first_path)
    logging.info(f"Data from {first_path} imported properly")
    df2 = create_data_frame(second_path)
    logging.info(f"Data from {second_path} imported properly")
    return df1, df2


def create_data_frame(path):
    path = add_extension_missed(path)
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        logging.critical(f"Wrong file name: {path}")
        sys.exit()
    return df


def add_extension_missed(path):
    if not ".csv" in path:
        path += ".csv"
    return path


def verify_and_clean_data(df_name, df, filter_countries=None):
    necessary_columns = NECESSARY_COLUMNS[df_name]
    verify_if_necessary_columns(df_name, df, necessary_columns)
    df = filter_per_counties(df, filter_countries)
    df = remove_unnecessary_columns(df, necessary_columns)
    return df


def verify_if_necessary_columns(df_name, df, necessary_columns):
    if not necessary_columns.issubset(df.columns):
        logging.critical("There are no all needed columns in dataset named: ", df_name)
        raise Exception


def filter_per_counties(df, filter_countries):
    if not filter_countries:
        return df

    filter_arg = filter_countries
    df = df.loc[df[FILTER_BY].isin(filter_arg)]
    logging.info(f"Data filtered for: {filter_arg} properly")
    return df


def remove_unnecessary_columns(df, necessary_columns):
    unnecessary_columns = necessary_columns ^ set(df.columns)
    if unnecessary_columns:
        df.drop([*unnecessary_columns], axis=1, inplace=True)
    logging.info(f"Unnecessary columns: {unnecessary_columns} removed properly")
    return df


def get_merged_dataset(left_df, right_df):
    df = left_df.merge(
        right_df,
        left_on=TABLES_MERGED_ON["left_on"],
        right_on=TABLES_MERGED_ON["right_on"],
        how="left",
    )
    logging.info(
        f"Datasets merged left_on={TABLES_MERGED_ON['left_on']} and right_on={TABLES_MERGED_ON['right_on']} properly"
    )
    return df


def get_properly_named_columns(df):
    return df.rename(columns=OUTPUT_COLUMN_NAMES_MAPPER)


def save_output_dataset_to_the_file(df):
    df.to_csv(OUTPUT_FILE_NAME, index=False)
    logging.info(f"Data saved in: {OUTPUT_FILE_NAME} properly")
