from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment


def style_header(ws, row=1):
    header_fill = PatternFill("solid", fgColor="1F4E78")
    header_font = Font(bold=True, color="FFFFFF")
    for cell in ws[row]:
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center")


def auto_size_columns(ws):
    for col in ws.columns:
        max_length = 0
        column = col[0].column_letter
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except Exception:
                pass
        ws.column_dimensions[column].width = min(max_length + 2, 22)


def add_table(ws, headers, rows):
    ws.append(headers)
    for row in rows:
        ws.append(row)
    style_header(ws)
    auto_size_columns(ws)


wb = Workbook()
ws = wb.active
ws.title = "Dashboard"
ws["A1"] = "Accounting Dashboard"
ws["A1"].font = Font(size=16, bold=True)
ws["A2"] = "Currency"
ws["B2"] = "JOD"
ws["A3"] = "Tax"
ws["B3"] = 0
ws["A5"] = "Sales"
ws["B5"] = '=SUMIF(Accounts!$C$2:$C$1000,"Revenue",Accounts!$H$2:$H$1000)'
ws["A6"] = "Expenses"
ws["B6"] = '=SUMIF(Accounts!$C$2:$C$1000,"Expense",Accounts!$H$2:$H$1000)'
ws["A7"] = "Net Profit"
ws["B7"] = '=B5-B6'
ws["A8"] = "Total Assets"
ws["B8"] = '=SUMIF(Accounts!$C$2:$C$1000,"Asset",Accounts!$H$2:$H$1000)'
ws["A9"] = "Total Liabilities"
ws["B9"] = '=SUMIF(Accounts!$C$2:$C$1000,"Liability",Accounts!$H$2:$H$1000)'
ws["A10"] = "Total Equity"
ws["B10"] = '=SUMIF(Accounts!$C$2:$C$1000,"Equity",Accounts!$H$2:$H$1000)'

# Accounts sheet
ws = wb.create_sheet("Accounts")
accounts_headers = ["AccountCode", "AccountName", "AccountType", "NormalSide", "ParentGroup", "Active", "OpeningBalance", "CurrentBalance", "Notes"]
accounts_rows = [
    ["1010", "النقدية", "Asset", "Debit", "Assets", True, 0, 0, "الحساب الرئيسي للنقدية"],
    ["1020", "البنك", "Asset", "Debit", "Assets", True, 0, 0, "حساب البنك"],
    ["1030", "المدينون", "Asset", "Debit", "Assets", True, 0, 0, "حسابات العملاء"],
    ["1040", "المخزون", "Asset", "Debit", "Assets", True, 0, 0, "مخزون البضائع"],
    ["1050", "المعدات", "Asset", "Debit", "Assets", True, 0, 0, "المعدات والأجهزة"],
    ["2010", "الدائنون", "Liability", "Credit", "Liabilities", True, 0, 0, "حسابات الموردين"],
    ["2020", "ضرائب مستحقة الدفع", "Liability", "Credit", "Liabilities", True, 0, 0, "الضرائب المستحقة"],
    ["2030", "قروض طويلة الأجل", "Liability", "Credit", "Liabilities", True, 0, 0, "القروض"],
    ["3010", "رأس المال", "Equity", "Credit", "Equity", True, 0, 0, "رأس مال الشركة"],
    ["3020", "الأرباح المحتجزة", "Equity", "Credit", "Equity", True, 0, 0, "الأرباح المحتجزة"],
    ["4010", "إيرادات المبيعات", "Revenue", "Credit", "Income", True, 0, 0, "إيرادات البيع"],
    ["4020", "إيرادات الخدمات", "Revenue", "Credit", "Income", True, 0, 0, "إيرادات الخدمات"],
    ["5010", "مصروف الإيجار", "Expense", "Debit", "Expenses", True, 0, 0, "إيجار المحل"],
    ["5020", "مصروف الرواتب", "Expense", "Debit", "Expenses", True, 0, 0, "رواتب الموظفين"],
    ["5030", "مصروف المرافق", "Expense", "Debit", "Expenses", True, 0, 0, "كهرباء وماء وإنترنت"],
    ["5040", "مصروف التسويق", "Expense", "Debit", "Expenses", True, 0, 0, "مصروف التسويق"],
    ["5050", "مصروف النقل", "Expense", "Debit", "Expenses", True, 0, 0, "مصروف النقل"],
    ["5060", "مصروف إداري", "Expense", "Debit", "Expenses", True, 0, 0, "مصروفات إدارية"],
]
add_table(ws, accounts_headers, accounts_rows)

# Customers sheet
ws = wb.create_sheet("Customers")
customer_headers = ["CustomerCode", "CustomerName", "Phone", "Address", "CreditLimit", "CurrentBalance", "Active"]
customer_rows = [
    ["C-001", "أحمد علي", "0795123456", "عمان", 10000, 0, True],
    ["C-002", "فاطمة محمد", "0796654321", "الزرقاء", 5000, 0, True],
    ["C-003", "محمود سالم", "0797789456", "إربد", 8000, 0, True],
]
add_table(ws, customer_headers, customer_rows)

# Suppliers sheet
ws = wb.create_sheet("Suppliers")
supplier_headers = ["SupplierCode", "SupplierName", "Phone", "Address", "CreditLimit", "CurrentBalance", "Active"]
supplier_rows = [
    ["S-001", "شركة النور", "0788123456", "عمان", 20000, 0, True],
    ["S-002", "مؤسسة الخير", "0789654321", "الزرقاء", 15000, 0, True],
]
add_table(ws, supplier_headers, supplier_rows)

# Inventory sheet
ws = wb.create_sheet("Inventory")
inventory_headers = ["ItemCode", "ItemName", "Category", "UnitCost", "SellingPrice", "QtyInStock", "ReorderLevel", "Active"]
inventory_rows = [
    ["ITM-001", "لابتوب", "إلكترونيات", 1800, 2500, 25, 5, True],
    ["ITM-002", "هاتف ذكي", "إلكترونيات", 600, 999, 50, 10, True],
    ["ITM-003", "طابعة", "أجهزة مكتبية", 400, 650, 15, 3, True],
    ["ITM-004", "مراوح الهواء", "إلكترونيات", 150, 299, 80, 20, True],
]
add_table(ws, inventory_headers, inventory_rows)

# Journal sheet
ws = wb.create_sheet("Journal")
journal_headers = ["Date", "JournalNo", "Reference", "AccountCode", "AccountName", "Debit", "Credit", "Description", "SourceType", "Status"]
journal_rows = [
    ["2026-10-01", "JV-0001", "INV-1001", "1010", "النقدية", 50000, 0, "دفعة رأس مال من المالك", "Capital", "Posted"],
    ["2026-10-01", "JV-0001", "INV-1001", "3010", "رأس المال", 0, 50000, "دفعة رأس مال من المالك", "Capital", "Posted"],
    ["2026-10-05", "JV-0002", "INV-1002", "1010", "النقدية", 8000, 0, "بيع بضائع نقداً", "Sale", "Posted"],
    ["2026-10-05", "JV-0002", "INV-1002", "4010", "إيرادات المبيعات", 0, 8000, "بيع بضائع نقداً", "Sale", "Posted"],
    ["2026-10-06", "JV-0003", "PAY-1001", "5010", "مصروف الإيجار", 1500, 0, "دفع الإيجار الشهري", "Expense", "Posted"],
    ["2026-10-06", "JV-0003", "PAY-1001", "1010", "النقدية", 0, 1500, "دفع الإيجار الشهري", "Expense", "Posted"],
]
add_table(ws, journal_headers, journal_rows)

# Ledger sheet
ws = wb.create_sheet("Ledger")
ledger_headers = ["Date", "JournalNo", "AccountCode", "AccountName", "Debit", "Credit", "Balance", "Description"]
add_table(ws, ledger_headers, [])

# Invoices sheet
ws = wb.create_sheet("Invoices")
invoice_headers = ["InvoiceNo", "Date", "CustomerCode", "CustomerName", "Total", "Tax", "Net", "Paid", "Balance", "Status"]
invoice_rows = [
    ["INV-1001", "2026-10-05", "C-001", "أحمد علي", 8000, 0, 8000, 8000, 0, "Paid"],
    ["INV-1002", "2026-10-06", "C-002", "فاطمة محمد", 5000, 0, 5000, 0, 5000, "Unpaid"],
]
add_table(ws, invoice_headers, invoice_rows)

# Payments sheet
ws = wb.create_sheet("Payments")
payment_headers = ["PaymentNo", "Date", "AccountCode", "AccountName", "CustomerOrSupplier", "PaymentType", "Amount", "Method", "Notes"]
payment_rows = [
    ["PMT-1001", "2026-10-06", "1010", "النقدية", "مصروف الإيجار", "Rent", 1500, "Cash", "دفع الإيجار الشهري"],
    ["PMT-1002", "2026-10-06", "1010", "النقدية", "الكهرباء والماء", "Utilities", 300, "Bank Transfer", "فاتورة الكهرباء والماء"],
]
add_table(ws, payment_headers, payment_rows)

# TrialBalance sheet
ws = wb.create_sheet("TrialBalance")
trial_headers = ["AccountCode", "AccountName", "DebitTotal", "CreditTotal", "Balance"]
add_table(ws, trial_headers, [])

# IncomeStatement sheet
ws = wb.create_sheet("IncomeStatement")
income_headers = ["Category", "Value", "Notes"]
income_rows = [
    ["Revenue", 0, "إجمالي الإيرادات"],
    ["Expenses", 0, "إجمالي المصاريف"],
    ["Net Profit", 0, "صافي الربح"],
]
add_table(ws, income_headers, income_rows)

# BalanceSheet sheet
ws = wb.create_sheet("BalanceSheet")
balance_headers = ["Category", "Value", "Notes"]
balance_rows = [
    ["Assets", 0, "الأصول"],
    ["Liabilities", 0, "الالتزامات"],
    ["Equity", 0, "حقوق الملكية"],
]
add_table(ws, balance_headers, balance_rows)

# Settings sheet
ws = wb.create_sheet("Settings")
settings_headers = ["Key", "Value"]
settings_rows = [
    ["Company Name", "شركتي"],
    ["Currency", "JOD"],
    ["Fiscal Year", "2026"],
    ["Tax Rate", 0],
    ["LastJournalNo", "JV-0003"],
    ["LastInvoiceNo", "INV-1002"],
    ["LastPaymentNo", "PMT-1002"],
]
add_table(ws, settings_headers, settings_rows)

# Reports sheet
ws = wb.create_sheet("Reports")
report_headers = ["ReportName", "Description", "Status"]
report_rows = [
    ["Trial Balance", "ميزان المراجعة", "Ready"],
    ["Income Statement", "قائمة الدخل", "Ready"],
    ["Balance Sheet", "الميزانية العمومية", "Ready"],
    ["Dashboard", "لوحة التحكم", "Ready"],
]
add_table(ws, report_headers, report_rows)

# Save workbook
wb.save("Accounting_System_JOD.xlsx")
print("Accounting_System_JOD.xlsx created successfully.")
