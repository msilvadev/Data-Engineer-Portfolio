import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *

def process_song_file(cur, filepath):
    """ Reads songs files row by row.
        Select necessary fields to load `songs` and `artists` table.

        Args:
            cur (psycopg2.cursor()): Cursor of the sparkifydb database
            filepath (str): Filepath of the file to be analyzed
    """

    df = pd.read_json(filepath, lines=True)

    for value in df.values:
        artist_id, artist_latitude, artist_location, artist_longitude, artist_name, duration, num_songs, song_id, title, year = value

        artist_data = [artist_id, artist_name, artist_location, artist_longitude, artist_latitude]
        cur.execute(artist_table_insert, artist_data)

        song_data = [song_id, title, artist_id, year, duration]
        cur.execute(song_table_insert, song_data)


def process_log_file(cur, filepath):
    """ Reads user activity log file row by row.
        Apply filter by NexSong, selects necessary fields, transforms them and inserts
        them into `time`, `user` and `songplay` tables.

        Args:
            cur (psycopg2.cursor()): Cursor of the sparkifydb database
            filepath (str): Filepath of the file to be analyzed
    """

    df = pd.read_json(filepath, lines=True)

    df = df[df['page']=='NextSong']

    t = pd.to_datetime(df['ts'], unit='ms')

    time_data = []
    for line in t:
        time_data.append([line, line.hour, line.day, line.week, line.month, line.year, line.day_name()])
    column_labels = ('start_time', 'hour', 'day', 'week', 'month', 'year', 'weekday')
    time_df = pd.DataFrame.from_records(time_data, columns=column_labels)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]

    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    for index, row in df.iterrows():

        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()

        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        songplay_data = (pd.to_datetime(row.ts, unit='ms'), int(row.userId), row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """Walks through all files nested under filepath, and processes all data.

    Args:
        cur (psycopg2.cursor()): cursor of the sparkifydb database
        conn (psycopg2.connect()): connection to the sparkifycdb database
        filepath (str): Filepath where are files
        func (python function): function to be used to process each file

    Returns:
        Name of files processed
    """

    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """The main function used to start ETL process and execute the extract, transform all data from song and logs files and finally load it into a database.
    Show result of a query where search register where song_id and artist_id is not null on songplays table to check out that was loaded
        Usage: python etl.py
    """
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    cur.execute("select * from songplays WHERE song_id is not null and artist_id is not null")
    results = cur.fetchall()
    print("Result of `select * from songplays WHERE song_id is not null and artist_id is not null`:")
    print(results)

    conn.close()


if __name__ == "__main__":
    main()