import datetime
import os

import requests
from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.utils import timezone
from requests.adapters import HTTPAdapter

from users.models import UserProfile
from users.utils import lock
from verification_results.models import VerificationResult
from verifications.models import Verification

CURRENT_FILE_DIR = os.path.dirname(os.path.abspath(__file__))


class Command(BaseCommand):

    @lock(os.path.join(CURRENT_FILE_DIR, os.path.basename(__file__) + ".lock"))
    def handle(self, *args, **options):
        now = timezone.now()
        utc_now = now.utcnow()

        users = UserProfile.objects.all()

        for user in users:
            errors = []
            for page in user.page_set.all():

                verification: Verification  # setting the type of http_verification
                for verification in page.verification_set.all():

                    # Vérification HTTP
                    # On essaye de parser au mieux l'addresse pour renvoyer le minimum d'erreurs
                    url = verification.page.url
                    if not url.startswith("http://") and not url.startswith("https://"):
                        url = "https://" + url

                    adapter = HTTPAdapter(max_retries=5)
                    http = requests.Session()
                    http.mount("https://", adapter)
                    http.mount("http://", adapter)

                    # On set les paramètres communs en cas d'échec et de réussite
                    verification_result = VerificationResult()
                    verification_result.verification = verification
                    verification_result.date = now

                    try:
                        response = http.get(url)
                    except requests.exceptions.SSLError:
                        pass
                    except Exception as err:
                        # Catch les exception retournée par la requête
                        verification_result.success = True
                        verification_result.description = err
                        print(err)
                        print("Ca marche pô l'URL doit être cassey : %s" % err)

                    else:
                        if verification.verification_type.identifiant == "HTTP":
                            print("Vérification HTTP")
                            self.verify_http_code(response, verification_result)

                        elif verification.verification_type.identifiant == "TXT":
                            print("Vérification TXT")
                            self.verify_page_content(response, verification_result)

                        elif verification.verification_type.identifiant == "TIME":
                            print("Vérification TIME")
                            self.verify_time_response(response, verification_result)

                        else:
                            verification_result.success = False
                            verification_result.description = "Identifiant unique du type de vérification incorrect !"

                        # On sauvegarde la vérification effectuée
                        print(verification_result)
                        verification_result.save()
                        if not verification_result.success:
                            errors.append(verification_result)
            if len(errors) > 0:
                self.send_mail_errors(errors)
        with open(os.path.join(settings.LOG_DIR, os.path.basename(__file__) + "_exec.log"), "a") as f:
            f.write(
                str(datetime.datetime.utcnow())
                + " ==> Elapsed %s" % (datetime.datetime.utcnow() - utc_now)
                + "\n")

    @staticmethod
    def send_mail_errors(errors: [VerificationResult]):

        content = ""
        for verification_result in errors:
            content += str(verification_result.verification.verification_type.name) \
                       + " " \
                       + str(verification_result.verification.verification_option) \
                       + " ==> Erreur ❌ : " + verification_result.description + "\n"

        send_mail(
            'At %s errors occurs' % errors[0].date,
            content,
            'admin.jandco@gmail.com',
            ['joussetn49@gmail.com'],
            fail_silently=False,
        )

    @staticmethod
    def verify_http_code(response: requests.Response, verification_result):
        success = int(verification_result.verification.verification_option) == int(response.status_code)
        verification_result.success = success
        verification_result.description = \
            ("Erreur, " if not success else " Succès, ") + "code attendu : {0}, code obtenu : {1}" \
                .format(verification_result.verification.verification_option, response.status_code)

    @staticmethod
    def verify_page_content(response: requests.Response, verification_result):
        success = str(verification_result.verification.verification_option) in str(response.text)

        verification_result.success = success
        verification_result.description = \
            (
                "Erreur, la page ne contient pas le(s) terme(s) : \"{0}\""
                if not success
                else "Succès, la page contient le texte : \"{0}\""
            ).format(verification_result.verification.verification_option)

    @staticmethod
    def verify_time_response(response: requests.Response, verification_result):
        success = float(verification_result.verification.verification_option) > float(response.elapsed.total_seconds())

        verification_result.success = success
        verification_result.description = \
            (
                "Erreur, temps de réponse de : {0} ms (> {1} ms)"
                if not success
                else "Succès, temps de réponse de : {0} ms (< {1} ms)"
            ).format(round(float(response.elapsed.total_seconds()), 3),
                     float(verification_result.verification.verification_option))

    # @staticmethod
    # def get_ssl_cert(response: requests.Response):
    #     pool = response.connection.poolmanager.connection_from_url(response.url)
    #     conn = pool.pool.get()
    #     # get() removes the connection from the pool, so put it back in
    #     pool.pool.put(conn)
    #     return conn.sock.getpeercert()
    #
    # def verify_ssl_validity(self, first_response, verification_result):
    #     session = requests.Session()
    #     # Create request
    #     request = requests.Request(first_response.request.method, url=first_response.url).prepare()
    #
    #     # Send request
    #     response = session.send(request)
    #     cert = self.get_ssl_cert(response)
    #     print(cert)
    #     print(cert)
    #     success = True
    #
    #     verification_result.success = success
    #     verification_result.description = \
    #         (
    #             "Erreur, temps de réponse de : {0} ms (> {1} ms)"
    #             if not success
    #             else "Succès, temps de réponse de : {0} ms (< {1} ms)"
    #         ).format(round(float(response.elapsed.total_seconds()), 3),
    #                  float(verification_result.verification.verification_option))
