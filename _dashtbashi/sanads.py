from rest_framework.exceptions import ValidationError

from _dashtbashi.models import Lading, Car, OilCompanyLading
from accounts.defaultAccounts.models import DefaultAccount
from helpers.functions import sanad_exp
from sanads.models import clearSanad, Sanad, newSanadCode


class LadingSanad:
    def __init__(self, lading: Lading):
        self.lading = lading

    def update(self):
        lading = self.lading
        car = self.lading.driving.car
        driver = self.lading.driving.driver

        contract_type = "Transportation" if car.contract_type == car.TRANSPORTATION else "OilCompany"

        sanad = self.lading.sanad
        if not sanad:
            sanad = Sanad.objects.create(code=newSanadCode(), financial_year=self.lading.financial_year,
                                         date=self.lading.sanad_date or self.lading.bill_date)
            lading.sanad = sanad
            lading.save()
            return
        else:
            clearSanad(sanad)
            sanad.is_auto_created = True
            sanad.save()

        sanad_items = []

        explanation = ''
        if Lading.LADING in lading.type:
            explanation += sanad_exp(
                "بابت عطف",
                lading.local_id,
                "به شماره بارگیری",
                lading.lading_number,
                "توسط",
                driver.name,
                "-",
                lading.ware.name,
                "به وزن",
                lading.destination_amount,
                "از",
                lading.origin.name,
                "به",
                lading.destination.name,
                lading.lading_explanation
            )

            bed_explanation = sanad_exp(explanation, "با نرخ", lading.contractor_price)
            commission_bes_explanation = sanad_exp(explanation, "با نرخ", lading.commission_price)
            fare_bes_explanation = sanad_exp(explanation, "با نرخ", lading.fare_price)

            if lading.remittance_payment_method == Lading.TO_COMPANY:
                if lading.contractor_type == Lading.OTHER:
                    # 1 & 2 & 3 & 4 & 5 & 6
                    sanad_items.append({
                        'bed': lading.lading_total_value,
                        'account': lading.contractor,
                        'explanation': bed_explanation
                    })

                    if car.owner == Car.RAHMAN:
                        sanad_items.append({
                            'bes': lading.company_commission_income,
                            'account': DefaultAccount.get(
                                'companyCommissionIncomeInRahman{}Cars'.format(contract_type)).account,
                            'explanation': commission_bes_explanation
                        })
                        sanad_items.append({
                            'bes': lading.car_income,
                            'account': car.incomeAccount,
                            'floatAccount': driver.floatAccount,
                            'explanation': fare_bes_explanation
                        })

                    elif car.owner == Car.PARTNERSHIP:
                        sanad_items.append({
                            'bes': lading.company_commission_income,
                            'account': DefaultAccount.get(
                                'companyCommissionIncomeInPartnership{}Cars'.format(contract_type)).account,
                            'explanation': commission_bes_explanation
                        })
                        sanad_items.append({
                            'bes': lading.car_income,
                            'account': car.incomeAccount,
                            'floatAccount': driver.floatAccount,
                            'explanation': fare_bes_explanation
                        })

                    elif car.owner == Car.EBRAHIM:
                        sanad_items.append({
                            'bes': lading.lading_total_value,
                            'account': car.payableAccount,
                            'floatAccount': driver.floatAccount,
                            'explanation': bed_explanation
                        })

                    elif car.owner == Car.RAHIM:
                        sanad_items.append({
                            'bes': lading.company_commission_income,
                            'account': DefaultAccount.get(
                                'companyCommissionIncomeInRahim{}Cars'.format(contract_type)).account,
                            'explanation': commission_bes_explanation
                        })
                        sanad_items.append({
                            'bes': lading.car_income,
                            'account': car.payableAccount,
                            'floatAccount': driver.floatAccount,
                            'explanation': fare_bes_explanation
                        })

                    elif car.owner == Car.OTHER:
                        sanad_items.append({
                            'bes': lading.company_commission_income,
                            'account': DefaultAccount.get(
                                'companyCommissionIncomeInOther{}Cars'.format(contract_type)).account,
                            'explanation': commission_bes_explanation
                        })
                        sanad_items.append({
                            'bes': lading.car_income,
                            'account': car.payableAccount,
                            'floatAccount': driver.floatAccount,
                            'explanation': fare_bes_explanation
                        })

            elif lading.remittance_payment_method == Lading.TO_COMPANY_AND_DRIVER:
                # 7 & 8
                sanad_items.append({
                    'bed': lading.company_commission_income,
                    'account': lading.contractor,
                    'explanation': bed_explanation
                })

                if car.owner == Car.OTHER:
                    sanad_items.append({
                        'bes': lading.company_commission_income,
                        'account': DefaultAccount.get(
                            'companyCommissionIncomeInOther{}Cars'.format(contract_type)).account,
                        'explanation': commission_bes_explanation
                    })

                if car.owner == Car.EBRAHIM:
                    sanad_items.append({
                        'bes': lading.company_commission_income,
                        'account': DefaultAccount.get(
                            'companyCommissionIncomeInEbrahim{}Cars'.format(contract_type)).account,
                        'explanation': commission_bes_explanation
                    })

            elif lading.remittance_payment_method == Lading.COMPANY_PAYS and lading.contractor_type == Lading.COMPANY:
                # 9 & 10
                if lading.ware_type == Lading.BOUGHT:
                    sanad_items.append({
                        'bed': lading.car_income,
                        'account': DefaultAccount.get('companyAccountForTransportingBoughtWare').account,
                        'explanation': bed_explanation
                    })
                elif lading.ware_type == Lading.SOLD:
                    sanad_items.append({
                        'bed': lading.car_income,
                        'account': DefaultAccount.get('companyAccountForTransportingSoldWare').account,
                        'explanation': bed_explanation
                    })

                if car.owner == Car.RAHMAN:
                    sanad_items.append({
                        'bes': lading.car_income,
                        'account': car.incomeAccount,
                        'floatAccount': driver.floatAccount,
                        'explanation': bed_explanation
                    })

                if car.owner == Car.PARTNERSHIP:
                    sanad_items.append({
                        'bes': lading.car_income,
                        'account': DefaultAccount.get('partnershipCars{}Income'.format(contract_type)).account,
                        'explanation': bed_explanation
                    })

                if car.owner == Car.OTHER:
                    sanad_items.append({
                        'bes': lading.car_income,
                        'account': lading.driving.car.payableAccount,
                        'floatAccount': lading.driving.driver.floatAccount,
                        'explanation': bed_explanation
                    })

            # Tip Sanads

            tip_explanation = sanad_exp(
                "بابت انعام شماره عطف",
                lading.local_id,
                "به شماره بارگیری",
                lading.lading_number,
                "توسط"
            )
            tip_bed_explanation = sanad_exp(
                tip_explanation,
                driver.name
            )
            tip_bes_explanation = sanad_exp(
                tip_explanation,
                car.car_number_str
            )

            # 11 & 12
            if lading.driver_tip_payer == Lading.COMPANY:
                if car.owner in (Car.RAHMAN, Car.PARTNERSHIP):
                    sanad_items.append({
                        'bed': lading.driver_tip_price,
                        'account': car.expenseAccount,
                        'floatAccount_id': 1,
                        'explanation': tip_bed_explanation
                    })
                else:
                    sanad_items.append({
                        'bed': lading.driver_tip_price,
                        'account': DefaultAccount.get('otherDriversTipExpense').account,
                        'explanation': tip_bed_explanation
                    })
            elif lading.driver_tip_payer == Lading.CONTRACTOR:
                sanad_items.append({
                    'bed': lading.driver_tip_price,
                    'account': lading.contractor,
                    'explanation': tip_bed_explanation
                })

            sanad_items.append({
                'bes': lading.driver_tip_price,
                'account': car.payableAccount,
                'floatAccount': driver.floatAccount,
                'explanation': tip_bes_explanation
            })

            # Lading Difference Sanads

            # 13 & 14

            lading_difference_bed_explanation = sanad_exp(
                "بابت اختلاف بارنامه شماره عطف",
                lading.local_id,
                "به شماره بارگیری",
                lading.lading_number,
                "توسط",
                driver.name
            )

            if car.owner in (Car.RAHIM, Car.EBRAHIM, Car.OTHER):
                lading_difference_bes_explanation = sanad_exp(
                    "بابت اختلاف بارنامه شماره عطف",
                    lading.local_id,
                    "به شماره بارگیری",
                    lading.lading_number,
                )
            else:
                lading_difference_bes_explanation = sanad_exp(
                    "بابت شماره عطف",
                    lading.local_id,
                    "به شماره بارگیری",
                    lading.lading_number,
                    "توسط",
                    driver.name
                )

            sanad_items.append({
                'bed': lading.lading_bill_difference,
                'account': lading.contractor,
                'explanation': lading_difference_bed_explanation
            })

            if car.owner in (Car.RAHMAN, Car.PARTNERSHIP):
                sanad_items.append({
                    'bes': lading.lading_bill_difference,
                    'account': DefaultAccount.get('ladingBillDifferenceIncome').account,
                    'explanation': lading_difference_bes_explanation
                })
            else:
                sanad_items.append({
                    'bes': lading.lading_bill_difference,
                    'account': car.payableAccount,
                    'floatAccount': driver.floatAccount,
                    'explanation': lading_difference_bes_explanation
                })

        # Lading Bill Sanads
        if Lading.BILL in lading.type:

            if explanation:
                explanation = sanad_exp(explanation, "و صدور بارنامه دولتی شماره")
            else:
                explanation = "بابت صدور بارنامه دولتی شماره"
            explanation = sanad_exp(
                explanation,
                lading.billNumber.number,
                "/",
                lading.billNumber.series.serial,
                "به صورت",
                lading.get_receive_type_display(),
                lading.bill_explanation
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

            if lading.receive_type in (Lading.CASH, Lading.POS):
                bed_explanation = sanad_exp(
                    "بابت دریافت جهت صدور بارنامه دولتی شماره",
                    lading.billNumber.number,
                    "/",
                    lading.billNumber.series.serial,
                    "از",
                    driver.name
                )
            elif lading.receive_type == Lading.CREDIT:
                if car.owner == Car.OTHER:
                    bed_explanation = sanad_exp(
                        "بابت خرید بارنامه دولتی شماره",
                        lading.billNumber.number,
                        "/",
                        lading.billNumber.series.serial,
                    )
                else:
                    bed_explanation = sanad_exp(
                        "بابت صدور بارنامه دولتی شماره",
                        lading.billNumber.number,
                        "/",
                        lading.billNumber.series.serial,
                        "برای",
                        driver.name
                    )
            else:
                raise ValidationError("نوع دریافت معتبر نیست")

            cargo_income_bes_explanation = sanad_exp(
                "بابت فروش بارنامه دولتی شماره",
                lading.billNumber.number,
                "/",
                lading.billNumber.series.serial,
                "برای",
                driver.name
            )
            cargo_employee_bes_explanation = sanad_exp(
                "بابت پرداخت انعام توسط",
                driver.name
            )
            association_bes_explanation = sanad_exp(
                "بابت صدور بارنامه دولتی شماره",
                lading.billNumber.number,
                "/",
                lading.billNumber.series.serial,
                "برای",
                driver.name
            )

            sanad_items.append({
                'bed': lading.lading_bill_total_value,
                'account': bed_account,
                'floatAccount': bed_float_account,
                'explanation': bed_explanation
            })

            sanad_items.append({
                'bes': lading.bill_price,
                'account': DefaultAccount.get('cargoIncome').account,
                'explanation': cargo_income_bes_explanation
            })
            sanad_items.append({
                'bes': lading.cargo_tip_price,
                'account': DefaultAccount.get('cargoEmployeePayableAccount').account,
                'explanation': cargo_employee_bes_explanation
            })
            sanad_items.append({
                'bes': lading.association_price,
                'account': DefaultAccount.get('associationPayableAccount').account,
                'explanation': association_bes_explanation
            })

        for sanad_item in sanad_items:
            if sanad_item.get('bed', 0) == sanad_item.get('bes', 0) == 0:
                continue

            sanad.items.create(
                **sanad_item
            )

        sanad.explanation = explanation
        sanad.save()
        sanad.update_values()


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
                    'companyCommissionIncomeInRahman{}Cars'.format(contract_type)).account,
                'explanation': explanation
            })

        elif car.owner == Car.PARTNERSHIP:
            sanad_items.append({
                'bes': oil_company_lading.company_commission,
                'account': DefaultAccount.get(
                    'companyCommissionIncomeInPartnership{}Cars'.format(contract_type)).account,
                'explanation': explanation
            })

        elif car.owner == Car.EBRAHIM:
            sanad_items.append({
                'bes': oil_company_lading.company_commission,
                'account': DefaultAccount.get(
                    'companyCommissionIncomeInEbrahim{}Cars'.format(contract_type)).account,
                'floatAccount': driver.floatAccount,
                'explanation': explanation
            })

        elif car.owner == Car.RAHIM:
            sanad_items.append({
                'bes': oil_company_lading.company_commission,
                'account': DefaultAccount.get(
                    'companyCommissionIncomeInRahim{}Cars'.format(contract_type)).account,
                'explanation': explanation
            })

        elif car.owner == Car.OTHER:
            sanad_items.append({
                'bes': oil_company_lading.company_commission,
                'account': DefaultAccount.get(
                    'companyCommissionIncomeInOther{}Cars'.format(contract_type)).account,
                'explanation': explanation
            })

        if car.owner in (Car.EBRAHIM, Car.RAHIM, Car.OTHER):
            sanad_items.append({
                'bes': oil_company_lading.car_income,
                'account': car.payableAccount,
                'floatAccount': driver.floatAccount,
                'explanation': explanation
            })
        else:
            sanad_items.append({
                'bes': oil_company_lading.car_income,
                'account': car.incomeAccount,
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

        sanad.update_values()
