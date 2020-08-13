from _dashtbashi.models import Lading, Car
from accounts.defaultAccounts.models import DefaultAccount
from sanads.models import clearSanad, Sanad, newSanadCode


class LadingSanad:
    def __init__(self, lading: Lading):
        self.lading = lading

    def update(self):
        lading = self.lading
        car = self.lading.driving.car
        driver = self.lading.driving.driver

        sanad = self.lading.sanad
        if not sanad:
            sanad = Sanad.objects.create(code=newSanadCode(), financial_year=self.lading.financial_year,
                                         date=self.lading.lading_date, createType=Sanad.AUTO)
            lading.sanad = sanad
            lading.save()
            return
        else:
            clearSanad(sanad)

        if lading.remittance_payment_method == Lading.TO_COMPANY:
            if lading.contractor_type == Lading.OTHER:
                # 1 & 2 & 3 & 4 & 5 & 6
                sanad.items.create(
                    bed=lading.lading_total_value,
                    account=lading.contractor,
                )

                if car.owner == Car.RAHMAN:
                    sanad.items.create(
                        bes=lading.company_commission_income,
                        account=DefaultAccount.get('companyCommissionIncomeInRahmanTransportationCars').account,
                    )
                    print(lading.car_income)
                    print(car.incomeAccount)
                    print(driver.floatAccount)
                    sanad.items.create(
                        bes=lading.car_income,
                        account=car.incomeAccount,
                        floatAccount=driver.floatAccount
                    )

                elif car.owner == Car.PARTNERSHIP:
                    sanad.items.create(
                        bes=lading.company_commission_income,
                        account=DefaultAccount.get('companyCommissionIncomeInPartnershipTransportationCars').account,
                    )
                    sanad.items.create(
                        bes=lading.car_income,
                        account=car.incomeAccount,
                        floatAccount=driver.floatAccount
                    )

                elif car.owner == Car.EBRAHIM:
                    sanad.items.create(
                        bes=lading.lading_total_value,
                        account=car.payableAccount,
                        floatAccount=driver.floatAccount
                    )

                elif car.owner == Car.RAHIM:
                    sanad.items.create(
                        bes=lading.company_commission_income,
                        account=DefaultAccount.get('companyCommissionIncomeInRahimTransportationCars').account,
                    )
                    sanad.items.create(
                        bes=lading.car_income,
                        account=car.payableAccount,
                        floatAccount=driver.floatAccount
                    )

                elif car.owner == Car.OTHER:
                    sanad.items.create(
                        bes=lading.company_commission_income,
                        account=DefaultAccount.get('companyCommissionIncomeInOtherTransportationCars').account,
                    )
                    sanad.items.create(
                        bes=lading.car_income,
                        account=car.payableAccount,
                        floatAccount=driver.floatAccount
                    )

        elif lading.remittance_payment_method == Lading.TO_COMPANY_AND_DRIVER:
            # 7 & 8
            sanad.items.create(
                bed=lading.company_commission_income,
                account=DefaultAccount.get('companyCommissionIncomeInOtherTransportationCars').account,
            )

            if car.owner == Car.OTHER:
                sanad.items.create(
                    bes=lading.company_commission_income,
                    account=DefaultAccount.get('companyCommissionIncomeInOtherTransportationCars').account,
                )

            if car.owner == Car.EBRAHIM:
                sanad.items.create(
                    bes=lading.company_commission_income,
                    account=DefaultAccount.get('companyCommissionIncomeInEbrahimTransportationCars').account,
                )

        elif lading.remittance_payment_method == Lading.COMPANY_PAYS and lading.contractor_type == Lading.COMPANY:
            # 9 & 10
            if lading.ware_type == Lading.BOUGHT:
                sanad.items.create(
                    bed=lading.car_income,
                    account=DefaultAccount.get('companyAccountForTransportingBoughtWare').account,
                )
            elif lading.ware_type == Lading.SOLD:
                sanad.items.create(
                    bed=lading.car_income,
                    account=DefaultAccount.get('companyAccountForTransportingSoldWare').account,
                )

            if car.owner == Car.RAHMAN:
                sanad.items.create(
                    bes=lading.car_income,
                    account=DefaultAccount.get('rahmanCarsTransportationIncome').account,
                )

            if car.owner == Car.PARTNERSHIP:
                sanad.items.create(
                    bes=lading.car_income,
                    account=DefaultAccount.get('partnershipCarsTransportationIncome').account,
                )

            if car.owner == Car.OTHER:
                sanad.items.create(
                    bes=lading.car_income,
                    account=lading.driving.car.payableAccount,
                    floatAccount=lading.driving.driver.floatAccount,
                )

        # Tip Sanads

        # 11 & 12
        if lading.driver_tip_payer == Lading.COMPANY:
            if car.owner == Car.RAHMAN:
                sanad.items.create(
                    bed=lading.driver_tip_price,
                    account=car.expenseAccount,
                    floatAccount_id=1
                )
            else:
                sanad.items.create(
                    bed=lading.driver_tip_price,
                    account=DefaultAccount.get('otherDriversTipExpense').account,
                )
        elif lading.driver_tip_payer == Lading.CONTRACTOR:
            sanad.items.create(
                bed=lading.driver_tip_price,
                account=lading.contractor,
            )
        sanad.items.create(
            bes=lading.driver_tip_price,
            account=car.payableAccount,
            floatAccount=driver.floatAccount,
        )

        # Lading Difference Sanads

        # 13 & 14
        sanad.items.create(
            bed=lading.lading_bill_difference,
            account=lading.contractor,
        )
        if car.owner in (Car.RAHMAN, Car.PARTNERSHIP):
            sanad.items.create(
                bes=lading.lading_bill_difference,
                account=DefaultAccount.get('ladingBillDifferenceIncome').account,
            )
        else:
            sanad.items.create(
                bes=lading.lading_bill_difference,
                account=car.payableAccount,
                floatAccount=driver.floatAccount,
            )

        # Lading Bill Sanads

        bed_account = None
        bed_float_account = None
        if lading.receive_type == Lading.CASH:
            bed_account = DefaultAccount.get('cargoFund').account
        elif lading.receive_type == Lading.POS:
            bed_account = DefaultAccount.get('cargoPOS').account
        elif lading.receive_type == Lading.CREDIT:
            if car.owner == Car.RAHMAN:
                bed_account = DefaultAccount.get('rahmanCargoReceivableAccount').account
            elif car.owner == Car.RAHIM:
                bed_account = DefaultAccount.get('rahimCargoReceivableAccount').account
            elif car.owner == Car.EBRAHIM:
                bed_account = DefaultAccount.get('ebrahimCargoReceivableAccount').account
            elif car.owner == Car.PARTNERSHIP:
                bed_account = DefaultAccount.get('partnershipCargoReceivableAccount').account
            else:
                bed_account = car.payableAccount
                bed_float_account = driver.floatAccount

        sanad.items.create(
            bed=lading.lading_bill_total_value,
            account=bed_account,
            floatAccount=bed_float_account,
        )

        sanad.items.create(
            bes=lading.bill_price,
            account=DefaultAccount.get('cargoIncome').account,
        )
        sanad.items.create(
            bes=lading.cargo_tip_price,
            account=DefaultAccount.get('cargoEmployeePayableAccount').account,
        )
        sanad.items.create(
            bes=lading.association_price,
            account=DefaultAccount.get('associationPayableAccount').account,
        )
