import random
import string

from model_bakery import baker

from .bale import BaleTestCase
from .inventory import InventoryRecordTestCase

# from .qc_transaction import QCTransactionTestCase

# from .single_user_login import LoginLogoutTestCase

# from .qr_code_stock import QRCodeScanningTestCase
# from .production import ProductionTestCase


def random_upper_case():
    return "".join(
        [random.choice(string.ascii_uppercase) for x in range(0, 3)]  # nosec
    )


baker.generators.add("common.models.UpperCharField", random_upper_case)


baker.generators.add(
    "phonenumber_field.modelfields.PhoneNumberField", lambda: "+91912345608"
)

baker.generators.add(
    "common.models.PositiveFloatField", lambda: random.random()  # nosec
)
