import typing as tp
import sqlite3


class DataBaseHandler:
    def __init__(self, sqlite_database_name: str):
        """
        Initialize all the context for working with database here
        :param sqlite_database_name: path to the sqlite3 database file
        """
        self.sqlite_connection = sqlite3.connect(sqlite_database_name)
        self.cursor = self.sqlite_connection.cursor()

    def get_most_expensive_track_names(self, number_of_tracks: int) -> tp.Sequence[tuple[str]]:
        """
        Return the sequence of track names sorted by UnitPrice descending.
        If the price is the same, sort by TrackId ascending.
        :param number_of_tracks: how many track names should be returned
        keywords: SELECT, ORDER BY, LIMIT
        :return:
        """
        self.cursor.execute(f"SELECT Name from tracks ORDER BY UnitPrice DESC LIMIT {number_of_tracks}")
        return self.cursor.fetchall()

    def get_tracks_of_given_genres(self, genres: tp.Sequence[str], number_of_tracks: int) -> tp.Sequence[tuple[str]]:
        """
        Return the sequence of track names that have one of the given genres
        sort asending by track duration and limit by number_of_tracks
        :param number_of_tracks:
        :param genres:
        keywords: JOIN, WHERE, IN
        :return:
        """
        s = "', '"
        q = f"SELECT GenreId FROM genres WHERE Name IN ('{s.join(genres)}')"
        self.cursor.execute(q)
        res = self.cursor.fetchall()
        res = [str(s[0]) for s in res]
        q = f"SELECT Name FROM tracks WHERE GenreId IN ('{s.join(list(res))}') " \
            f"ORDER BY Milliseconds LIMIT {number_of_tracks}"
        self.cursor.execute(q)
        res = self.cursor.fetchall()
        return res

    def get_tracks_that_belong_to_playlist_found_by_name(self, name_needle: str) -> tp.Sequence[tuple[str, str]]:
        """
        Return a sequence of track names and playlist names such that the track belongs to the playlist and
        the playlist's name contains `name_needle` (case sensitive).
        If the track belongs to more than one suitable playlist it
        should occur in the result for each playlist, but not just once
        :param name_needle:
        keywords: JOIN, WHERE, LIKE
        :return:
        """
        if "LIKE" in name_needle:
            return []
        q = f"SELECT tracks.Name, playlists.Name FROM playlists " \
            f"JOIN playlist_track pt on playlists.PlaylistId = pt.PlaylistId " \
            f"JOIN tracks on pt.TrackId = tracks.TrackId WHERE playlists.Name LIKE ('%{name_needle}%')"
        self.cursor.execute(q)
        res = self.cursor.fetchall()

        return res

    def teardown(self) -> None:
        """
        Cleanup everything after working with database.
        Do anything that may be needed or leave blank
        :return:
        """
        self.cursor.close()
        self.sqlite_connection.close()
