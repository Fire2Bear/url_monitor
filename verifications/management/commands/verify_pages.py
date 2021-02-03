import os
import socket
import ssl
import urllib
from datetime import datetime, timedelta

import OpenSSL.crypto as crypto
import requests
from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.timezone import utc
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

                    # Valeurs par défaut
                    # On set les paramètres communs en cas d'échec et de réussite
                    verification_result = VerificationResult()
                    verification_result.verification = verification
                    verification_result.date = now
                    verification_result.success = False
                    verification_result.description = "An error occurred !"

                    # Vérification HTTP
                    # On essaye de parser au mieux l'addresse pour renvoyer le minimum d'erreurs
                    url = verification.page.url
                    if not url.startswith("http://") and not url.startswith("https://"):
                        url = "https://" + url

                    adapter = HTTPAdapter(max_retries=5)
                    http = requests.Session()
                    http.mount("https://", adapter)
                    http.mount("http://", adapter)

                    if "CERT" in verification.verification_type.identifiant:
                        if verification.verification_type.identifiant == "CERT-VALID":
                            print("Vérification CERT-VALID")
                            self.verify_ssl_validity(url, verification_result)

                        elif verification.verification_type.identifiant == "CERT-EXPIR":
                            print("Vérification CERT-EXPIR")
                            self.verify_cert_expiration(url, verification_result)
                    else:

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

                    # On sauvegarde la vérification effectuée
                    print(verification_result)
                    print("----")
                    verification_result.save()
                    if not verification_result.success:
                        errors.append(verification_result)
            if len(errors) > 0:
                self.send_mail_errors(errors)
        with open(os.path.join(settings.LOG_DIR, os.path.basename(__file__) + "_exec.log"), "a") as f:
            f.write(
                str(datetime.utcnow())
                + " ==> Elapsed %s" % (datetime.utcnow() - utc_now)
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

    @staticmethod
    def verify_ssl_validity(url, verification_result):
        data = get_cert_data(url)

        success = not data.get('expired')

        verification_result.success = success
        verification_result.description = \
            (
                "Erreur, certificat valide du {0} au {1}"
                if not success
                else "Succès, certificat valide du {0} au {1}"
            ).format(data.get('notAfter'), data.get('notBefore'))

    @staticmethod
    def verify_cert_expiration(url, verification_result):
        data = get_cert_data(url)

        date = verification_result.date
        end_date = date + timedelta(days=int(verification_result.verification.verification_option))

        success = end_date < data.get('notAfter').replace(tzinfo=utc)

        verification_result.success = success
        verification_result.description = \
            (
                "Erreur, certificat valide jusqu'au {0}"
                if not success
                else "Succès, certificat valide jusqu'au {0}"
            ).format(data.get('notAfter').replace(tzinfo=utc))


def get_cert_data(url) -> []:
    parsed_url = urllib.parse.urlparse(url)
    hostname = parsed_url.netloc

    datas = []
    now = datetime.now()

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    with ctx.wrap_socket(socket.socket(), server_hostname=hostname) as s:
        s.connect((hostname, 443))
        cert = s.getpeercert(True)
        x509 = crypto.load_certificate(crypto.FILETYPE_ASN1, cert)
        common_name = x509.get_subject().CN
        not_after = datetime.strptime(x509.get_notAfter().decode('ascii'), '%Y%m%d%H%M%SZ')
        not_before = datetime.strptime(x509.get_notBefore().decode('ascii'), '%Y%m%d%H%M%SZ')
        return {
            "name": common_name,
            "notAfter": not_after,
            "notBefore": not_before,
            "expired": (not_after < now) or (not_before > now)
        }
