#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
نظام محاسبي احترافي - Accounting System JOD
مصمم للشركات الصغيرة والمتوسطة بالدينار الأردني
"""

import json
import os
from datetime import datetime
from pathlib import Path

class AccountingSystem:
    def __init__(self, db_file="accounting_system.json"):
        self.db_file = db_file
        self.data = {
            "company": {
                "name": "شركتي",
                "currency": "JOD",
                "tax_rate": 0,
                "fiscal_year": 2026
            },
            "accounts": [],
            "customers": [],
            "suppliers": [],
            "inventory": [],
            "journal": [],
            "invoices": [],
            "payments": []
        }
        self.load_data()

    def load_data(self):
        """تحميل البيانات من الملف"""
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
                print("✓ تم تحميل البيانات السابقة")
            except Exception as e:
                print(f"خطأ في تحميل البيانات: {e}")
                self.initialize_accounts()
        else:
            self.initialize_accounts()

    def save_data(self):
        """حفظ البيانات إلى الملف"""
        try:
            with open(self.db_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            print("✓ تم حفظ البيانات بنجاح")
        except Exception as e:
            print(f"خطأ في حفظ البيانات: {e}")

    def initialize_accounts(self):
        """إنشاء الحسابات الافتراضية"""
        default_accounts = [
            {"code": "1010", "name": "النقدية", "type": "Asset", "normal_side": "Debit", "balance": 0},
            {"code": "1020", "name": "البنك", "type": "Asset", "normal_side": "Debit", "balance": 0},
            {"code": "1030", "name": "المدينون", "type": "Asset", "normal_side": "Debit", "balance": 0},
            {"code": "1040", "name": "المخزون", "type": "Asset", "normal_side": "Debit", "balance": 0},
            {"code": "2010", "name": "الدائنون", "type": "Liability", "normal_side": "Credit", "balance": 0},
            {"code": "3010", "name": "رأس المال", "type": "Equity", "normal_side": "Credit", "balance": 0},
            {"code": "4010", "name": "إيرادات المبيعات", "type": "Revenue", "normal_side": "Credit", "balance": 0},
            {"code": "5010", "name": "مصروف الإيجار", "type": "Expense", "normal_side": "Debit", "balance": 0},
            {"code": "5020", "name": "مصروف الرواتب", "type": "Expense", "normal_side": "Debit", "balance": 0},
            {"code": "5030", "name": "مصروف المرافق", "type": "Expense", "normal_side": "Debit", "balance": 0},
        ]
        self.data["accounts"] = default_accounts
        self.save_data()
        print("✓ تم إنشاء الحسابات الافتراضية")

    def add_account(self, code, name, acc_type, normal_side):
        """إضافة حساب جديد"""
        account = {
            "code": code,
            "name": name,
            "type": acc_type,
            "normal_side": normal_side,
            "balance": 0
        }
        self.data["accounts"].append(account)
        self.save_data()
        print(f"✓ تم إضافة الحساب: {name}")

    def add_customer(self, code, name, phone, address, credit_limit):
        """إضافة عميل جديد"""
        customer = {
            "code": code,
            "name": name,
            "phone": phone,
            "address": address,
            "credit_limit": credit_limit,
            "current_balance": 0
        }
        self.data["customers"].append(customer)
        self.save_data()
        print(f"✓ تم إضافة العميل: {name}")

    def add_supplier(self, code, name, phone, address, credit_limit):
        """إضافة مورد جديد"""
        supplier = {
            "code": code,
            "name": name,
            "phone": phone,
            "address": address,
            "credit_limit": credit_limit,
            "current_balance": 0
        }
        self.data["suppliers"].append(supplier)
        self.save_data()
        print(f"✓ تم إضافة المورد: {name}")

    def add_inventory(self, code, name, category, unit_cost, selling_price, qty):
        """إضافة صنف في المخزون"""
        item = {
            "code": code,
            "name": name,
            "category": category,
            "unit_cost": unit_cost,
            "selling_price": selling_price,
            "qty_in_stock": qty
        }
        self.data["inventory"].append(item)
        self.save_data()
        print(f"✓ تم إضافة الصنف: {name}")

    def post_journal_entry(self, date, journal_no, account_code, debit, credit, description):
        """تسجيل قيد محاسبي"""
        entry = {
            "date": date,
            "journal_no": journal_no,
            "account_code": account_code,
            "debit": debit,
            "credit": credit,
            "description": description,
            "status": "Posted"
        }
        self.data["journal"].append(entry)
        
        # تحديث رصيد الحساب
        for account in self.data["accounts"]:
            if account["code"] == account_code:
                if account["normal_side"] == "Debit":
                    account["balance"] += debit - credit
                else:
                    account["balance"] += credit - debit
                break
        
        self.save_data()
        print(f"✓ تم تسجيل القيد: {description}")

    def add_invoice(self, invoice_no, date, customer_code, total, tax=0):
        """إضافة فاتورة"""
        invoice = {
            "invoice_no": invoice_no,
            "date": date,
            "customer_code": customer_code,
            "total": total,
            "tax": tax,
            "net": total - tax,
            "paid": 0,
            "balance": total - tax,
            "status": "Unpaid"
        }
        self.data["invoices"].append(invoice)
        self.save_data()
        print(f"✓ تم إضافة الفاتورة: {invoice_no}")

    def add_payment(self, payment_no, date, account_code, amount, method):
        """إضافة دفعة"""
        payment = {
            "payment_no": payment_no,
            "date": date,
            "account_code": account_code,
            "amount": amount,
            "method": method,
            "status": "Completed"
        }
        self.data["payments"].append(payment)
        self.save_data()
        print(f"✓ تم تسجيل الدفعة: {payment_no}")

    def get_trial_balance(self):
        """الحصول على ميزان المراجعة"""
        print("\n" + "="*60)
        print("ميزان المراجعة")
        print("="*60)
        print(f"{'الحساب':<20} {'الكود':<10} {'مدين':<15} {'دائن':<15}")
        print("-"*60)
        
        total_debit = 0
        total_credit = 0
        
        for account in self.data["accounts"]:
            if account["normal_side"] == "Debit":
                debit = account["balance"] if account["balance"] > 0 else 0
                credit = abs(account["balance"]) if account["balance"] < 0 else 0
            else:
                debit = abs(account["balance"]) if account["balance"] < 0 else 0
                credit = account["balance"] if account["balance"] > 0 else 0
            
            total_debit += debit
            total_credit += credit
            
            print(f"{account['name']:<20} {account['code']:<10} {debit:<15.2f} {credit:<15.2f}")
        
        print("-"*60)
        print(f"{'المجموع':<20} {'':<10} {total_debit:<15.2f} {total_credit:<15.2f}")
        print("="*60)
        
        if abs(total_debit - total_credit) < 0.01:
            print("✓ ميزان المراجعة متوازن")
        else:
            print("⚠️ ميزان المراجعة غير متوازن!")

    def get_income_statement(self):
        """قائمة الدخل"""
        print("\n" + "="*60)
        print("قائمة الدخل")
        print("="*60)
        
        revenue = 0
        expenses = 0
        
        for account in self.data["accounts"]:
            if account["type"] == "Revenue":
                revenue += account["balance"]
            elif account["type"] == "Expense":
                expenses += abs(account["balance"])
        
        net_profit = revenue - expenses
        
        print(f"الإيرادات: {revenue:>20.2f} د.ا")
        print(f"المصاريف: {expenses:>20.2f} د.ا")
        print("-"*60)
        print(f"صافي الربح: {net_profit:>18.2f} د.ا")
        print("="*60)

    def get_balance_sheet(self):
        """الميزانية العمومية"""
        print("\n" + "="*60)
        print("الميزانية العمومية")
        print("="*60)
        
        assets = 0
        liabilities = 0
        equity = 0
        
        for account in self.data["accounts"]:
            if account["type"] == "Asset":
                assets += account["balance"]
            elif account["type"] == "Liability":
                liabilities += abs(account["balance"])
            elif account["type"] == "Equity":
                equity += account["balance"]
        
        print(f"\nالأصول: {assets:>25.2f} د.ا")
        print(f"الالتزامات: {liabilities:>20.2f} د.ا")
        print(f"حقوق الملكية: {equity:>18.2f} د.ا")
        print("-"*60)
        print(f"الالتزامات + حقوق الملكية: {liabilities + equity:>10.2f} د.ا")
        
        if abs(assets - (liabilities + equity)) < 0.01:
            print("✓ الميزانية متوازنة")
        else:
            print("⚠️ الميزانية غير متوازنة!")
        print("="*60)

    def show_menu(self):
        """عرض القائمة الرئيسية"""
        while True:
            print("\n" + "="*60)
            print("نظام المحاسبة - القائمة الرئيسية")
            print("="*60)
            print("1. إضافة حساب جديد")
            print("2. إضافة عميل جديد")
            print("3. إضافة مورد جديد")
            print("4. إضافة صنف في المخزون")
            print("5. تسجيل قيد محاسبي")
            print("6. إضافة فاتورة")
            print("7. تسجيل دفعة")
            print("8. عرض ميزان المراجعة")
            print("9. عرض قائمة الدخل")
            print("10. عرض الميزانية العمومية")
            print("11. عرض الحسابات")
            print("12. عرض العملاء")
            print("13. عرض الموردين")
            print("14. خروج")
            print("="*60)
            
            choice = input("اختر رقم العملية: ").strip()
            
            if choice == "1":
                self.menu_add_account()
            elif choice == "2":
                self.menu_add_customer()
            elif choice == "3":
                self.menu_add_supplier()
            elif choice == "4":
                self.menu_add_inventory()
            elif choice == "5":
                self.menu_post_journal()
            elif choice == "6":
                self.menu_add_invoice()
            elif choice == "7":
                self.menu_add_payment()
            elif choice == "8":
                self.get_trial_balance()
            elif choice == "9":
                self.get_income_statement()
            elif choice == "10":
                self.get_balance_sheet()
            elif choice == "11":
                self.show_accounts()
            elif choice == "12":
                self.show_customers()
            elif choice == "13":
                self.show_suppliers()
            elif choice == "14":
                print("شكراً لاستخدام النظام. وداعاً!")
                break
            else:
                print("⚠️ اختيار غير صحيح. حاول مرة أخرى.")

    def menu_add_account(self):
        """قائمة إضافة حساب"""
        print("\n--- إضافة حساب جديد ---")
        code = input("أدخل رمز الحساب: ").strip()
        name = input("أدخل اسم الحساب: ").strip()
        print("أنواع الحسابات: Asset, Liability, Equity, Revenue, Expense")
        acc_type = input("أدخل نوع الحساب: ").strip()
        normal_side = input("أدخل الجانب الطبيعي (Debit/Credit): ").strip()
        self.add_account(code, name, acc_type, normal_side)

    def menu_add_customer(self):
        """قائمة إضافة عميل"""
        print("\n--- إضافة عميل جديد ---")
        code = input("أدخل رمز العميل: ").strip()
        name = input("أدخل اسم العميل: ").strip()
        phone = input("أدخل رقم الهاتف: ").strip()
        address = input("أدخل العنوان: ").strip()
        credit_limit = float(input("أدخل حد الائتمان: "))
        self.add_customer(code, name, phone, address, credit_limit)

    def menu_add_supplier(self):
        """قائمة إضافة مورد"""
        print("\n--- إضافة مورد جديد ---")
        code = input("أدخل رمز المورد: ").strip()
        name = input("أدخل اسم المورد: ").strip()
        phone = input("أدخل رقم الهاتف: ").strip()
        address = input("أدخل العنوان: ").strip()
        credit_limit = float(input("أدخل حد الائتمان: "))
        self.add_supplier(code, name, phone, address, credit_limit)

    def menu_add_inventory(self):
        """قائمة إضافة صنف"""
        print("\n--- إضافة صنف في المخزون ---")
        code = input("أدخل رمز الصنف: ").strip()
        name = input("أدخل اسم الصنف: ").strip()
        category = input("أدخل الفئة: ").strip()
        unit_cost = float(input("أدخل تكلفة الوحدة: "))
        selling_price = float(input("أدخل سعر البيع: "))
        qty = float(input("أدخل الكمية: "))
        self.add_inventory(code, name, category, unit_cost, selling_price, qty)

    def menu_post_journal(self):
        """قائمة تسجيل قيد"""
        print("\n--- تسجيل قيد محاسبي ---")
        date = input("أدخل التاريخ (YYYY-MM-DD): ").strip()
        journal_no = input("أدخل رقم القيد: ").strip()
        account_code = input("أدخل رمز الحساب: ").strip()
        debit = float(input("أدخل المبلغ المدين (أو 0): "))
        credit = float(input("أدخل المبلغ الدائن (أو 0): "))
        description = input("أدخل وصف القيد: ").strip()
        self.post_journal_entry(date, journal_no, account_code, debit, credit, description)

    def menu_add_invoice(self):
        """قائمة إضافة فاتورة"""
        print("\n--- إضافة فاتورة ---")
        invoice_no = input("أدخل رقم الفاتورة: ").strip()
        date = input("أدخل التاريخ (YYYY-MM-DD): ").strip()
        customer_code = input("أدخل رمز العميل: ").strip()
        total = float(input("أدخل المبلغ الإجمالي: "))
        tax = float(input("أدخل الضريبة (أو 0): "))
        self.add_invoice(invoice_no, date, customer_code, total, tax)

    def menu_add_payment(self):
        """قائمة تسجيل دفعة"""
        print("\n--- تسجيل دفعة ---")
        payment_no = input("أدخل رقم الدفعة: ").strip()
        date = input("أدخل التاريخ (YYYY-MM-DD): ").strip()
        account_code = input("أدخل رمز الحساب: ").strip()
        amount = float(input("أدخل المبلغ: "))
        method = input("أدخل طريقة الدفع (Cash/Bank): ").strip()
        self.add_payment(payment_no, date, account_code, amount, method)

    def show_accounts(self):
        """عرض الحسابات"""
        print("\n" + "="*80)
        print("الحسابات")
        print("="*80)
        print(f"{'الكود':<10} {'الاسم':<25} {'النوع':<15} {'الرصيد':<15}")
        print("-"*80)
        for account in self.data["accounts"]:
            print(f"{account['code']:<10} {account['name']:<25} {account['type']:<15} {account['balance']:<15.2f}")
        print("="*80)

    def show_customers(self):
        """عرض العملاء"""
        print("\n" + "="*80)
        print("العملاء")
        print("="*80)
        print(f"{'الكود':<10} {'الاسم':<25} {'الهاتف':<15} {'الرصيد':<15}")
        print("-"*80)
        for customer in self.data["customers"]:
            print(f"{customer['code']:<10} {customer['name']:<25} {customer['phone']:<15} {customer['current_balance']:<15.2f}")
        print("="*80)

    def show_suppliers(self):
        """عرض الموردين"""
        print("\n" + "="*80)
        print("الموردين")
        print("="*80)
        print(f"{'الكود':<10} {'الاسم':<25} {'الهاتف':<15} {'الرصيد':<15}")
        print("-"*80)
        for supplier in self.data["suppliers"]:
            print(f"{supplier['code']:<10} {supplier['name']:<25} {supplier['phone']:<15} {supplier['current_balance']:<15.2f}")
        print("="*80)


def main():
    print("\n" + "="*60)
    print("مرحباً بك في نظام المحاسبة - JOD")
    print("="*60 + "\n")
    
    system = AccountingSystem()
    system.show_menu()


if __name__ == "__main__":
    main()
