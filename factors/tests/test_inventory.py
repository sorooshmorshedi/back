from factors.models import Factor
from factors.models.factor import FactorItem
from factors.tests.test_factors import FactorTest
from factors.views.definite_factor import DefiniteFactor
from users.models import User
from helpers.test import MTestCase
from users.tests.test_users import UserTest
from wares.models import Ware, WareInventory


class InventoryTest(MTestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = UserTest.get_user()

    def test_inventory(self):
        self.client.force_authenticate(self.user)
        financial_year = self.user.active_financial_year

        ware_1 = Ware.objects.all()[0]
        buy_factor = FactorTest.create_factor(financial_year, factor_type=Factor.BUY)

        FactorTest.create_factor_item(buy_factor, ware=ware_1, count=1, fee=1)
        FactorTest.create_factor_item(buy_factor, ware=ware_1, count=10, fee=10)
        FactorTest.create_factor_item(buy_factor, ware=ware_1, count=15, fee=15)
        FactorTest.create_factor_item(buy_factor, ware=ware_1, count=20, fee=20)

        # --- Test Definition

        DefiniteFactor.definiteFactor(self.user, buy_factor.id, is_confirmed=True)

        self.assertEqual(WareInventory.get_inventory_count(ware_1, ware_1.warehouse), 46)

        # --- Test Update Factor Item

        DefiniteFactor.updateFactorInventory(buy_factor, True)
        factor_item = buy_factor.items.all()[0]
        factor_item.count = 5
        factor_item.fee = 5
        factor_item.save()
        DefiniteFactor.definiteFactor(self.user, buy_factor.id)

        self.assertEqual(WareInventory.get_inventory_count(ware_1, ware_1.warehouse), 50)

        # --- Test Add New Factor Item

        DefiniteFactor.updateFactorInventory(buy_factor, True)
        FactorTest.create_factor_item(buy_factor, ware=ware_1, count=25, fee=25)
        DefiniteFactor.definiteFactor(self.user, buy_factor.id)

        self.assertEqual(WareInventory.get_inventory_count(ware_1, ware_1.warehouse), 75)

        # --- Test Delete Factor Item

        DefiniteFactor.updateFactorInventory(buy_factor, True)
        buy_factor.items.first().delete()
        DefiniteFactor.definiteFactor(self.user, buy_factor.id)

        self.assertEqual(WareInventory.get_inventory_count(ware_1, ware_1.warehouse), 70)

        # --- Test Adding Sale Factor

        sale_factor = FactorTest.create_factor(financial_year, factor_type=Factor.SALE)

        FactorTest.create_factor_item(sale_factor, ware=ware_1, count=1, fee=1)
        FactorTest.create_factor_item(sale_factor, ware=ware_1, count=4, fee=4)
        FactorTest.create_factor_item(sale_factor, ware=ware_1, count=6, fee=6)
        FactorTest.create_factor_item(sale_factor, ware=ware_1, count=8, fee=8)

        DefiniteFactor.definiteFactor(self.user, sale_factor.id)

        self.assertEqual(WareInventory.get_inventory_count(ware_1, ware_1.warehouse), 51)

        # --- Test Update Sale Factor Item

        DefiniteFactor.updateFactorInventory(sale_factor, True)
        factor_item = sale_factor.items.all()[0]
        factor_item.count = 2
        factor_item.fee = 2
        factor_item.save()
        DefiniteFactor.definiteFactor(self.user, sale_factor.id)

        self.assertEqual(WareInventory.get_inventory_count(ware_1, ware_1.warehouse), 50)

        # --- Test Add New Sale Factor Item

        DefiniteFactor.updateFactorInventory(sale_factor, True)
        FactorTest.create_factor_item(sale_factor, ware=ware_1, count=16, fee=16)
        DefiniteFactor.definiteFactor(self.user, sale_factor.id)

        self.assertEqual(WareInventory.get_inventory_count(ware_1, ware_1.warehouse), 34)

        # --- Test Delete Sale Factor Item

        DefiniteFactor.updateFactorInventory(sale_factor, True)
        sale_factor.items.first().delete()
        DefiniteFactor.definiteFactor(self.user, sale_factor.id)

        self.assertEqual(WareInventory.get_inventory_count(ware_1, ware_1.warehouse), 36)
