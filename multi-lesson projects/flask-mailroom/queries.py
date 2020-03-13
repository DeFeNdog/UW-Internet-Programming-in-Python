"""
Module for performing donor database actions
"""
import os
import base64
import logging
from peewee import *  # noqa F403
from models import db, Donor, Donation  # noqa F403
from utilities import *  # noqa F403

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Queries:
    """ Defines Queries class for interacting with DB """

    @staticmethod
    def get_donor_by_id(code):
        try:
            db.connect()
            # db.execute_sql('PRAGMA foreign_keys = ON;')
            # donor table
            d = Donor.get(Donor.code == code)  # noqa F403
            return d
        except Exception as e:
            # logger.info(f"Donor not found.")
            return False
        finally:
            db.close()

    @staticmethod
    def get_donors():
        try:
            db.connect()
            # db.execute_sql('PRAGMA foreign_keys = ON;')
            dl = list(Donor.select().execute())  # noqa F403
            # logger.info(f"Donors found.")
            return dl
        except Exception as e:
            logger.info(e)
            return False
        finally:
            db.close()

    @staticmethod
    def update_donor(code, first_name, last_name, prev_name):
        try:
            db.connect()
            # db.execute_sql('PRAGMA foreign_keys = ON;')
            # donor table
            person = (Donor  # noqa F403
                    .update(first_name=first_name, last_name=last_name)
                    .where(Donor.code == code)  # noqa F403
                    .execute())
            donation = (Donation  # noqa F403
                    .update(donor=last_name)
                    .where(Donation.donor == prev_name)  # noqa F403
                    .execute())
            # logger.info(f'Updated {first_name} {last_name}')
        except Exception as e:
            logger.info(e)
            return False
        finally:
            db.close()


    @staticmethod
    def insert_donation(code, donation):
        try:
            db.connect()
            # db.execute_sql('PRAGMA foreign_keys = ON;')
            # lookup
            row = Donor.get_by_id(code)  # noqa F403
            last_name = row.last_name
            # donation table
            Donation.insert(donation=donation, donor=last_name).execute()  # noqa F403
            # logger.info(f"Inserted: {last_name}, {donation}")
        except Exception as e:
            logger.info(e)
            return False
        finally:
            db.close()


    @staticmethod
    def delete_donations(code):
        """ deletes all donations for given donor """
        try:
            # lookup
            row = Donor.get_by_id(code)  # noqa F403
            last_name = row.last_name
            Donation.delete().where(Donation.donor == last_name).execute()  # noqa F403
        except Exception as e:
            logger.info(e)
            return False
        finally:
            db.close()


    def get_donor_single_summary(self, code):
        try:
            """
            Compiles a list for printing a single donor summary
            Called methods establish DB connection
            """
            nl = list()
            d = Donor.get_by_id(code)  # noqa F403

            if d:
                first = d.first_name
                last = d.last_name
                total = self.donations_total(code) if self.donations_total(code) else 0
                count = self.donations_count(code) if self.donations_count(code) else 0
                average = 0
                if total > 0 and count > 0:
                    average = total / count
                nl = [first, last, total, count, average]

            # logger.info('Donor found: {donor_id}')
            return nl

        except Exception as e:
            logger.info(e)
            return False
        finally:
            db.close()

    def get_donor_multiple_summary(self):
        try:
            """
            Compiles a list for printing multiple donor summaries
            Called methods establish DB connection
            """
            nl = list()
            donors = self.get_donors()
            for d in donors:
                code = d.code
                first = d.first_name
                last = d.last_name
                total = self.donations_total(code) if self.donations_total(code) else 0
                count = self.donations_count(code) if self.donations_count(code) else 0
                average = 0
                if total > 0 and count > 0:
                    average = total / count
                nl.append([code, first, last, total, count, average])
            # logger.info('Donors/donations found.')
            return nl

        except Exception as e:
            logger.info(e)
            return False
        finally:
            db.close()

    def delete_donor_donations(self, code):
        """ deletes donor and all donations associated with donor """
        try:
            db.connect()
            # db.execute_sql('PRAGMA foreign_keys = ON;')
            # donations table
            self.delete_donations(code)
            # donor table
            Donor.delete().where(Donor.code == code).execute()  # noqa F403
        except Exception as e:
            logger.info(e)
            return False
        finally:
            db.close()

    @staticmethod
    def insert_donor_donation(donor, donation):
        try:
            db.connect()
            # db.execute_sql('PRAGMA foreign_keys = ON;')
            # donor table
            code = base64.b32encode(os.urandom(8)).decode().strip('=')
            Donor.insert(  # noqa F403
                code=code,
                first_name=donor.first_name,
                last_name=donor.last_name).execute()
            # donation table
            Donation.insert(donation=donation, donor=donor.last_name).execute()  # noqa F403
            # logger.info("Inserted: {}, {}, {}".format(
            #             donor.first_name,
            #             donor.last_name,
            #             donation))
        except Exception as e:
            logger.info(e)
            return False
        finally:
            db.close()

    @staticmethod
    def donations_total(code):
        try:
            row = Donor.get_by_id(code)  # noqa F403
            last_name = row.last_name
            query = (Donation # noqa F403
                .select(fn.SUM(Donation.donation).alias('total')) # noqa F403
                .where(Donation.donor == last_name) # noqa F403
                .execute()) # noqa F403
            # logger.info(f"Total: id-{donor_id}, {query[0].total}")
            return query[0].total # noqa F403
        except Exception as e:
            logger.info(e)
            return False
        finally:
            db.close()

    @staticmethod
    def donations_count(code):
        try:
            db.connect()
            # db.execute_sql('PRAGMA foreign_keys = ON;')
            row = Donor.get_by_id(code)  # noqa F403
            last_name = row.last_name
            query = (Donation # noqa F403
                .select(fn.COUNT(Donation.donation).alias('count')) # noqa F403
                .where(Donation.donor == last_name) # noqa F403
                .execute()) # noqa F403

            # logger.info(f"Count: id-{donor_id}, {query[0].count}")
            return query[0].count
        except Exception as e:
            logger.info(e)
            return False
        finally:
            db.close()

    def donations_average(self, donor_id):
        try:
            db.connect()
            # db.execute_sql('PRAGMA foreign_keys = ON;')
            total = self.donations_total(d.id) if self.donations_total(d.id) else 0
            count = self.donations_count(d.id) if self.donations_count(d.id) else 0
            average = 0
            if total > 0 and count > 0:
                average = total / count
            # logger.info(f"Average: id-{donor_id}, {average}")
            return average
        except Exception as e:
            logger.info(e)
            return False
        finally:
            db.close()
