import os
import sys
import datetime
import time

from django.core.management.base import BaseCommand
from django.conf import settings
import requests
import urllib.parse

from django.utils import timezone
from requests.adapters import HTTPAdapter

from pages.models import Page
from users.utils import lock
from verification_results.models import VerificationResult
from verifications.models import Verification

CURRENT_FILE_DIR = os.path.dirname(os.path.abspath(__file__))


class Command(BaseCommand):

    @lock(os.path.join(CURRENT_FILE_DIR, os.path.basename(__file__) + ".lock"))
    def handle(self, *args, **options):
        now = timezone.now()
        utc_now = now.utcnow()

        pages = Page.objects.all()
        print("Vérifications : " + str(pages))

        for page in pages:

            verification: Verification  # setting the type of http_verification
            for verification in page.verification_set.all():

                # Vérification HTTP
                # On essaye de parser au mieux l'addresse pour renvoyer le minimum d'erreurs
                url = verification.page.url
                if not url.startswith("http://") and not url.startswith("https://"):
                    url = "http://" + url

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
                        verification_result.success = False
                        verification_result.description = "Pas encore implémenté"

                    elif verification.verification_type.identifiant == "TIME":
                        print("Vérification TIME")
                        verification_result.success = False
                        verification_result.description = "Pas encore implémenté"

                    # On sauvegarde la vérification effectuée
                    verification_result.save()
                    print(verification_result)

        with open(os.path.join(settings.LOG_DIR, os.path.basename(__file__) + "_exec.log"), "a") as f:
            f.write(
                str(datetime.datetime.utcnow())
                + " ==> Elapsed %s" % (datetime.datetime.utcnow() - utc_now)
                + "\n")

    @staticmethod
    def verify_http_code(response, verification_result):
        success = int(verification_result.verification.verification_option) == int(response.status_code)
        verification_result.success = success
        verification_result.description = \
            "Erreur, code attendu : {0}, code obtenu : {1}" \
            .format(verification_result.verification.verification_option, response.status_code)

    @staticmethod
    def verify_http_code(response, verification_result):
        success = int(verification_result.verification.verification_option) == int(response.status_code)
        verification_result.success = success
        verification_result.description = \
            "Erreur, code attendu : {0}, code obtenu : {1}" \
            .format(verification_result.verification.verification_option, response.status_code)



