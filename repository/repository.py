from datetime import date, datetime, timedelta
import fitbit
from fitbit.api import Fitbit
from fitbit.exceptions import HTTPBadRequest
from oauth2.server import OAuth2Server
from repository.csv import Csv
from repository.firestore import Firestore

class Repository():
    def __init__(self, fitbit: Fitbit, firestore: Firestore, csv: Csv, start_date, end_date):
        self.fitbit = fitbit
        self.firestore = firestore
        self.csv = csv
        self.start_date = start_date
        self.end_date = end_date
    
    def _log_err(self, err):
        print("  x", err)

    def get_profile(self):
        profile = self.fitbit.user_profile_get()['user']
        print("\n--------------------------------------------------")
        print('You are authorized to access data for the user: {}'.format(profile['fullName']))
        print("--------------------------------------------------\n")
        self.firestore.store_profile(profile)
        self.csv.store_profile(profile)
        return profile['encodedId']

    def get_intraday(self):
        for x in range((self.end_date-self.start_date).days + 1):
            date = self.start_date + timedelta(x)
            steps = self.fitbit.intraday_time_series(
                resource="steps", 
                start_date=date,
                end_date=date)
            self.firestore.store_intraday(data=steps, date=date, doc_name="steps")
            self.csv.store_intraday(data=steps, date=date, doc_name="steps")

            calories = self.fitbit.intraday_time_series(
                resource="calories", 
                start_date=date,
                end_date=date)
            self.firestore.store_intraday(data=calories, date=date, doc_name="calories")
            self.csv.store_intraday(data=calories, date=date, doc_name="calories")
            
            distance = self.fitbit.intraday_time_series(
                resource="distance", 
                start_date=date,
                end_date=date)
            self.firestore.store_intraday(data=distance, date=date, doc_name="distance")
            self.csv.store_intraday(data=calories, date=date, doc_name="calories")

            heart = self.fitbit.intraday_time_series(
                resource="heart", 
                start_date=date,
                end_date=date)
            self.firestore.store_intraday(data=heart, date=date, doc_name="heart")
            self.csv.store_intraday(data=heart, date=date, doc_name="heart")

            try:
                elevation = self.fitbit.intraday_time_series(
                    resource="elevation", 
                    start_date=date,
                    end_date=date)
                self.firestore.store_intraday(data=elevation, date=date, doc_name="elevation")
                self.csv.store_intraday(data=elevation, date=date, doc_name="elevation")
            except HTTPBadRequest as e:
                self._log_err(e)

            try:
                floors = self.fitbit.intraday_time_series(
                    resource="floors", 
                    start_date=date,
                    end_date=date)
                self.firestore.store_intraday(data=floors, date=date, doc_name="floors")
                self.csv.store_intraday(data=floors, date=date, doc_name="floors")
            except HTTPBadRequest as e:
                self._log_err(e)
    
    def get_time_series(self):
        sleeps = self.fitbit.time_series(
            resource='sleep', 
            api_version=1.2,
            base_date=self.start_date,
            end_date=self.end_date)
        self.firestore.store_time_series(data=sleeps, doc_name="sleeps")
        self.csv.store_time_series(data=sleeps, doc_name="sleeps")

        heart_rates = self.fitbit.time_series(
            resource='activities/heart',
            base_date=self.start_date,
            end_date=self.end_date)
        self.firestore.store_time_series(data=heart_rates, doc_name="heart_rates")
        self.csv.store_time_series(data=heart_rates, doc_name="heart_rates")

        activity_calories = self.fitbit.time_series(
            resource='activities/activityCalories',
            base_date=self.start_date,
            end_date=self.end_date)
        self.firestore.store_time_series(data=activity_calories, doc_name="activity_calories")
        self.csv.store_time_series(data=activity_calories, doc_name="activity_calories")

        calories = self.fitbit.time_series(
            resource='activities/calories',
            base_date=self.start_date,
            end_date=self.end_date)
        self.firestore.store_time_series(data=calories, doc_name="calories")
        self.csv.store_time_series(data=calories, doc_name="calories")

        calories_bmr = self.fitbit.time_series(
            resource='activities/caloriesBMR',
            base_date=self.start_date,
            end_date=self.end_date)
        self.firestore.store_time_series(data=calories_bmr, doc_name="calories_bmr")
        self.csv.store_time_series(data=calories_bmr, doc_name="calories_bmr")

        distance = self.fitbit.time_series(
            resource='activities/distance',
            base_date=self.start_date,
            end_date=self.end_date)
        self.firestore.store_time_series(data=distance, doc_name="distance")
        self.csv.store_time_series(data=distance, doc_name="distance")

        try:
            elevation = self.fitbit.time_series(
                resource='activities/elevation',
                base_date=self.start_date,
                end_date=self.end_date)
            self.firestore.store_time_series(data=elevation, doc_name="elevation")
            self.csv.store_time_series(data=elevation, doc_name="elevation")
        except HTTPBadRequest as e:
            self._log_err(e)

        try:
            floors = self.fitbit.time_series(
                resource='activities/floors',
                base_date=self.start_date,
                end_date=self.end_date)
            self.firestore.store_time_series(data=floors, doc_name="floors")
            self.csv.store_time_series(data=floors, doc_name="floors")
        except HTTPBadRequest as e:
            self._log_err(e)

        minutes_sedentary = self.fitbit.time_series(
            resource='activities/minutesSedentary',
            base_date=self.start_date,
            end_date=self.end_date)
        self.firestore.store_time_series(data=minutes_sedentary, doc_name="minutes_sedentary")
        self.csv.store_time_series(data=minutes_sedentary, doc_name="minutes_sedentary")

        minutes_lightly_active = self.fitbit.time_series(
            resource='activities/minutesLightlyActive',
            base_date=self.start_date,
            end_date=self.end_date)
        self.firestore.store_time_series(data=minutes_lightly_active, doc_name="minutes_lightly_active")
        self.csv.store_time_series(data=minutes_lightly_active, doc_name="minutes_lightly_active")

        minutes_fairly_active = self.fitbit.time_series(
            resource='activities/minutesFairlyActive',
            base_date=self.start_date,
            end_date=self.end_date)
        self.firestore.store_time_series(data=minutes_fairly_active, doc_name="minutes_fairly_active")
        self.csv.store_time_series(data=minutes_fairly_active, doc_name="minutes_fairly_active")

        minutes_very_active = self.fitbit.time_series(
            resource='activities/minutesVeryActive',
            base_date=self.start_date,
            end_date=self.end_date)
        self.firestore.store_time_series(data=minutes_very_active, doc_name="minutes_very_active")
        self.csv.store_time_series(data=minutes_very_active, doc_name="minutes_very_active")

        steps = self.fitbit.time_series(
            resource='activities/steps',
            base_date=self.start_date,
            end_date=self.end_date)
        self.firestore.store_time_series(data=steps, doc_name="steps")
        self.csv.store_time_series(data=steps, doc_name="steps")

