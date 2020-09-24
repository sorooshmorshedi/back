from _dashtbashi.models import Lading, Car, OilCompanyLading
from accounts.defaultAccounts.models import DefaultAccount
from sanads.models import clearSanad, Sanad, newSanadCode


class LadingSanad:
    def __init__(self, lading: Lading):
        self.lading = lading

    def update(self):
        lading = self.lading
        car = self.lading.driving.car
        driver = self.lading.driving.driver

        contract_type = "Transportation" if car.contract_type == car.TRANSPORTATION else "OilCompany"
        print(contract_type)

        sanad = self.lading.sanad
        if not sanad:
            sanad = Sanad.objects.create(code=newSanadCode(), financial_year=self.lading.financial_year,
                                         date=self.lading.lading_date)
            lading.sanad = sanad
            lading.save()
            return
        else:
            clearSanad(sanad)
            sanad.is_auto_created = True
            sanad.save()

        sanad.explanation = "{}, {}, {}, {}, {}, {}".format(
            car.car_number_str,
            driver.name,
            lading.origin.name,
            lading.destination.name,
            lading.contractor.name,
            str(lading.lading_date)
        )
        sanad.save()

        sanad_items = []

        def get_explanation(fee):
            return "{}, {}, {}, {}, {:g}, {:g}, {}, {}".format(
                lading.id,
                lading.lading_number,
                car.car_number_str,
                driver.name,
                float(fee),
                float(lading.destination_amount),
                lading.ware.name,
                lading.destination.name
            )

        if lading.remittance_payment_method == Lading.TO_COMPANY:
            if lading.contractor_type == Lading.OTHER:
                # 1 & 2 & 3 & 4 & 5 & 6
                sanad_items.append({
                    'bed': lading.lading_total_value,
                    'account': lading.contractor,
                    'explanation': get_explanation(lading.contractor_price)
                })

                if car.owner == Car.RAHMAN:
                    sanad_items.append({
                        'bes': lading.company_commission_income,
                        'account': DefaultAccount.get(
                            'companyCommissionIncomeInRahman{}Cars'.format(contract_type)).account,
                        'explanation': get_explanation(lading.company_commission_income)
                    })
                    sanad_items.append({
                        'bes': lading.car_income,
                        'account': car.incomeAccount,
                        'floatAccount': driver.floatAccount,
                        'explanation': get_explanation(lading.fare_price)
                    })

                elif car.owner == Car.PARTNERSHIP:
                    sanad_items.append({
                        'bes': lading.company_commission_income,
                        'account': DefaultAccount.get(
                            'companyCommissionIncomeInPartnership{}Cars'.format(contract_type)).account,
                        'explanation': get_explanation(lading.company_commission_income)
                    })
                    sanad_items.append({
                        'bes': lading.car_income,
                        'account': car.incomeAccount,
                        'floatAccount': driver.floatAccount,
                        'explanation': get_explanation(lading.fare_price)
                    })

                elif car.owner == Car.EBRAHIM:
                    sanad_items.append({
                        'bes': lading.lading_total_value,
                        'account': car.payableAccount,
                        'floatAccount': driver.floatAccount,
                        'explanation': get_explanation(lading.fare_price)
                    })

                elif car.owner == Car.RAHIM:
                    sanad_items.append({
                        'bes': lading.company_commission_income,
                        'account': DefaultAccount.get(
                            'companyCommissionIncomeInRahim{}Cars'.format(contract_type)).account,
                        'explanation': get_explanation(lading.company_commission_income)
                    })
                    sanad_items.append({
                        'bes': lading.car_income,
                        'account': car.payableAccount,
                        'floatAccount': driver.floatAccount,
                        'explanation': get_explanation(lading.fare_price)
                    })

                elif car.owner == Car.OTHER:
                    sanad_items.append({
                        'bes': lading.company_commission_income,
                        'account': DefaultAccount.get(
                            'companyCommissionIncomeInOther{}Cars'.format(contract_type)).account,
                        'explanation': get_explanation(lading.company_commission_income)
                    })
                    sanad_items.append({
                        'bes': lading.car_income,
                        'account': car.payableAccount,
                        'floatAccount': driver.floatAccount,
                        'explanation': get_explanation(lading.fare_price)
                    })

        elif lading.remittance_payment_method == Lading.TO_COMPANY_AND_DRIVER:
            # 7 & 8
            sanad_items.append({
                'bed': lading.company_commission_income,
                'account': lading.contractor,
                'explanation': get_explanation(lading.company_commission_income)
            })

            if car.owner == Car.OTHER:
                sanad_items.append({
                    'bes': lading.company_commission_income,
                    'account': DefaultAccount.get('companyCommissionIncomeInOther{}Cars'.format(contract_type)).account,
                    'explanation': get_explanation(lading.fare_price)
                })

            if car.owner == Car.EBRAHIM:
                sanad_items.append({
                    'bes': lading.company_commission_income,
                    'account': DefaultAccount.get(
                        'companyCommissionIncomeInEbrahim{}Cars'.format(contract_type)).account,
                    'explanation': get_explanation(lading.fare_price)
                })

        elif lading.remittance_payment_method == Lading.COMPANY_PAYS and lading.contractor_type == Lading.COMPANY:
            # 9 & 10
            if lading.ware_type == Lading.BOUGHT:
                sanad_items.append({
                    'bed': lading.car_income,
                    'account': DefaultAccount.get('companyAccountForTransportingBoughtWare').account,
                    'explanation': get_explanation(lading.contractor_price)
                })
            elif lading.ware_type == Lading.SOLD:
                sanad_items.append({
                    'bed': lading.car_income,
                    'account': DefaultAccount.get('companyAccountForTransportingSoldWare').account,
                    'explanation': get_explanation(lading.contractor_price)
                })

            if car.owner == Car.RAHMAN:
                sanad_items.append({
                    'bes': lading.car_income,
                    'account': car.incomeAccount,
                    'floatAccount': driver.floatAccount,
                    'explanation': get_explanation(lading.contractor_price)
                })

            if car.owner == Car.PARTNERSHIP:
                sanad_items.append({
                    'bes': lading.car_income,
                    'account': DefaultAccount.get('partnershipCars{}Income'.format(contract_type)).account,
                    'explanation': get_explanation(lading.contractor_price)
                })

            if car.owner == Car.OTHER:
                sanad_items.append({
                    'bes': lading.car_income,
                    'account': lading.driving.car.payableAccount,
                    'floatAccount': lading.driving.driver.floatAccount,
                    'explanation': get_explanation(lading.contractor_price)
                })

        # Tip Sanads

        explanation = "{}, {}, {}".format(str(lading.lading_date), lading.origin.name, lading.destination.name)

        # 11 & 12
        if lading.driver_tip_payer == Lading.COMPANY:
            if car.owner == Car.RAHMAN:
                sanad_items.append({
                    'bed': lading.driver_tip_price,
                    'account': car.expenseAccount,
                    'floatAccount_id': 1,
                    'explanation': explanation
                })
            else:
                sanad_items.append({
                    'bed': lading.driver_tip_price,
                    'account': DefaultAccount.get('otherDriversTipExpense').account,
                    'explanation': explanation
                })
        elif lading.driver_tip_payer == Lading.CONTRACTOR:
            sanad_items.append({
                'bed': lading.driver_tip_price,
                'account': lading.contractor,
                'explanation': explanation
            })

        sanad_items.append({
            'bes': lading.driver_tip_price,
            'account': car.payableAccount,
            'floatAccount': driver.floatAccount,
            'explanation': explanation
        })

        # Lading Difference Sanads

        # 13 & 14

        sanad_items.append({
            'bed': lading.lading_bill_difference,
            'account': lading.contractor,
            'explanation': explanation
        })

        if car.owner in (Car.RAHMAN, Car.PARTNERSHIP):
            sanad_items.append({
                'bes': lading.lading_bill_difference,
                'account': DefaultAccount.get('ladingBillDifferenceIncome').account,
                'explanation': explanation
            })
        else:
            sanad_items.append({
                'bes': lading.lading_bill_difference,
                'account': car.payableAccount,
                'floatAccount': driver.floatAccount,
                'explanation': explanation
            })

        # Lading Bill Sanads

        explanation = ""
        if lading.billNumber:
            explanation = "{} {}, {}, {}".format(
                lading.driving.driver.name,
                lading.driving.car.car_number_str,
                lading.billNumber.number,
                lading.billNumber.series.serial,
                str(lading.bill_date),
            )

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

        sanad_items.append({
            'bed': lading.lading_bill_total_value,
            'account': bed_account,
            'floatAccount': bed_float_account,
            'explanation': explanation
        })

        sanad_items.append({
            'bes': lading.bill_price,
            'account': DefaultAccount.get('cargoIncome').account,
            'explanation': explanation
        })
        sanad_items.append({
            'bes': lading.cargo_tip_price,
            'account': DefaultAccount.get('cargoEmployeePayableAccount').account,
            'explanation': explanation
        })
        sanad_items.append({
            'bes': lading.association_price,
            'account': DefaultAccount.get('associationPayableAccount').account,
            'explanation': explanation
        })

        for sanad_item in sanad_items:
            if sanad_item.get('bed', 0) == sanad_item.get('bes', 0) == 0:
                continue

            sanad.items.create(
                **sanad_item
            )


class OilCompanyLadingSanad:
    def __init__(self, oilCompanyLading: OilCompanyLading):
        self.oilCompanyLading = oilCompanyLading

    def update(self):
        oil_company_lading = self.oilCompanyLading
        car = self.oilCompanyLading.driving.car
        driver = self.oilCompanyLading.driving.driver
        contract_type = "Transportation" if car.contract_type == car.TRANSPORTATION else "OilCompany"

        sanad = self.oilCompanyLading.sanad
        if not sanad:
            sanad = Sanad.objects.create(code=newSanadCode(), financial_year=self.oilCompanyLading.financial_year,
                                         date=self.oilCompanyLading.date)
            oil_company_lading.sanad = sanad
            oil_company_lading.save()
            return
        else:
            clearSanad(sanad)
            sanad.is_auto_created = True
            sanad.save()

        explanation = "{} {}, {}, {}, {}, {}".format(
            oil_company_lading.id,
            oil_company_lading.month,
            oil_company_lading.driving.driver.name,
            str(oil_company_lading.date),
            oil_company_lading.driving.car.car_number_str,
            oil_company_lading.explanation,
        )
        sanad.explanation = explanation
        sanad.save()

        sanad_items = []

        sanad_items.append({
            'bed': oil_company_lading.total_value,
            'account': DefaultAccount.get('oilCompanyLadingAccount').account,
            'explanation': explanation
        })

        if car.owner == Car.RAHMAN:
            sanad_items.append({
                'bes': oil_company_lading.company_commission,
                'account': DefaultAccount.get(
                    'companyCommissionIncomeInRahmanOilCompany{}Cars'.format(contract_type)).account,
                'explanation': explanation
            })

        elif car.owner == Car.PARTNERSHIP:
            sanad_items.append({
                'bes': oil_company_lading.company_commission,
                'account': DefaultAccount.get(
                    'companyCommissionIncomeInPartnershipOilCompany{}Cars'.format(contract_type)).account,
                'explanation': explanation
            })

        elif car.owner == Car.EBRAHIM:
            sanad_items.append({
                'bes': oil_company_lading.company_commission,
                'account': DefaultAccount.get(
                    'companyCommissionIncomeInEbrahimOilCompany{}Cars'.format(contract_type)).account,
                'floatAccount': driver.floatAccount,
                'explanation': explanation
            })

        elif car.owner == Car.RAHIM:
            sanad_items.append({
                'bes': oil_company_lading.company_commission,
                'account': DefaultAccount.get(
                    'companyCommissionIncomeInRahimOilCompany{}Cars'.format(contract_type)).account,
                'explanation': explanation
            })

        elif car.owner == Car.OTHER:
            sanad_items.append({
                'bes': oil_company_lading.company_commission,
                'account': DefaultAccount.get(
                    'companyCommissionIncomeInOtherOilCompany{}Cars'.format(contract_type)).account,
                'explanation': explanation
            })

        sanad_items.append({
            'bes': oil_company_lading.car_income,
            'account': car.payableAccount,
            'floatAccount': driver.floatAccount,
            'explanation': explanation
        })

        sanad_items.append({
            'bes': oil_company_lading.tax_price + oil_company_lading.complication_price,
            'account': DefaultAccount.get('oilCompanyLadingTax').account,
            'explanation': explanation
        })

        for sanad_item in sanad_items:
            if sanad_item.get('bed', 0) == sanad_item.get('bes', 0) == 0:
                continue

            sanad.items.create(
                **sanad_item
            )
