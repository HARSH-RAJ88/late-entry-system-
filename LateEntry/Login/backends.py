from django.contrib.auth.models import User
import mysql.connector

from LateEntry.credentialManager import CredentialManager as cm

connection = mysql.connector.connect(user=cm.user, password=cm.password, host=cm.host, database=cm.database,
                                     autocommit=True)


class loginBackend():
    def authenticate(self, request, username=None, password=None, role=None):
        with  connection.cursor() as cursor:
            if username is not None and password is not None:
                if role == 'Guard':
                    cursor.execute("SELECT password FROM Guard where g_id = %s", (username,))

                elif role == 'Warden':
                    cursor.execute("SELECT password FROM Warden where w_id = %s", (username,))

                elif role == 'Student':
                    cursor.execute("SELECT password FROM Student where roll_no = %s", (username,))

                records = cursor.fetchall()
                print(records, password)
                if len(records) == 0:
                    return None
                if records[0][0] != password:
                    return None
                else:

                    user, created = User.objects.get_or_create(username=username + ('g' if role == 'Guard' else 'w'))
                    if created:  # If the user is created, set unusable password and save
                        user.email = role  # we have stored the role in the email
                        user.set_unusable_password()
                        user.save()
                    return user
            return None

    def get_user(self, uid):
        try:
            user = User.objects.get(pk=uid)
            return user
        except:
            return None
