import pandas as pd
from datetime import datetime
from io import BytesIO


# ─── TAX CALCULATOR ──────────────────────────────────────────────────────────

def calculate_tax(gross_revenue: float, declared_expenses: float = 0.0, presumptive_44ad: bool = False) -> dict:
    """
    Calculate taxable income and tax liability.

    Parameters:
        gross_revenue (float): Total turnover for the financial year.
        declared_expenses (float): Actual expenses (ignored if presumptive_44ad=True).
        presumptive_44ad (bool): If True, uses 6% deemed profit under Section 44AD.

    Returns:
        dict: {
            "taxable_income": float,
            "income_tax": float,
            "cess": float,
            "total_tax_liability": float,
            "method_note": str
        }
    """
    if presumptive_44ad:
        taxable_income = gross_revenue * 0.06
        note = "Presumptive taxation under Section 44AD (6% of turnover)."
    else:
        taxable_income = max(0, gross_revenue - declared_expenses)
        note = "Normal book‑accounting method (actual profit)."

    # Income tax slabs (FY 2025‑26, excluding cess)
    if taxable_income <= 700000:
        tax = 0
    elif taxable_income <= 1000000:
        tax = (taxable_income - 700000) * 0.10
    elif taxable_income <= 1200000:
        tax = 30000 + (taxable_income - 1000000) * 0.15
    elif taxable_income <= 1500000:
        tax = 60000 + (taxable_income - 1200000) * 0.20
    else:
        tax = 120000 + (taxable_income - 1500000) * 0.30

    cess = tax * 0.04
    total_tax = tax + cess

    return {
        "taxable_income": round(taxable_income, 2),
        "income_tax": round(tax, 2),
        "cess": round(cess, 2),
        "total_tax_liability": round(total_tax, 2),
        "method_note": note
    }


# ─── PORTFOLIO MANAGEMENT ────────────────────────────────────────────────────

def get_default_portfolio() -> pd.DataFrame:
    """Return a sample client portfolio DataFrame."""
    return pd.DataFrame([
        {"Client ID": "SA-01", "Client Name": "FutureHQ Node A",
         "Entity Type": "Proprietorship", "Service Stream": "ITR & Tax Audit",
         "FY 2025-26 Turnover (₹)": 1800000, "Estimated Tax Liability (₹)": 45000,
         "Filing Deadline": "2026-07-31", "Workflow Status": "Document Verification"},
        {"Client ID": "SA-02", "Client Name": "CarryMe Logistics",
         "Entity Type": "LLP / Startup", "Service Stream": "GST Reconciliation",
         "FY 2025-26 Turnover (₹)": 4200000, "Estimated Tax Liability (₹)": 756000,
         "Filing Deadline": "2026-06-25", "Workflow Status": "Pending Upload"}
    ])


def batch_calculate_tax(portfolio_df: pd.DataFrame, use_presumptive: bool = False) -> pd.DataFrame:
    """
    Add a 'Calculated Tax (₹)' column to the portfolio.

    Expects a column named 'FY 2025-26 Turnover (₹)'.
    Optionally uses 'Operational Deductions (₹)' if present (ignored under presumptive).
    """
    result = portfolio_df.copy()
    deductions_col = "Operational Deductions (₹)" if "Operational Deductions (₹)" in result.columns else None

    taxes = []
    for _, row in result.iterrows():
        revenue = row["FY 2025-26 Turnover (₹)"]
        expenses = row[deductions_col] if deductions_col and not use_presumptive else 0
        calc = calculate_tax(revenue, expenses, use_presumptive)
        taxes.append(calc["total_tax_liability"])

    result["Calculated Tax (₹)"] = taxes
    return result


# ─── IMPORT / EXPORT ─────────────────────────────────────────────────────────

def portfolio_to_excel(portfolio_df: pd.DataFrame) -> BytesIO:
    """Export portfolio to an in‑memory Excel file."""
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        portfolio_df.to_excel(writer, index=False, sheet_name="Self_Assist_Portfolio")
    output.seek(0)
    return output


def portfolio_to_csv(portfolio_df: pd.DataFrame) -> bytes:
    """Export portfolio to CSV bytes."""
    return portfolio_df.to_csv(index=False).encode("utf-8")


def load_portfolio_from_excel(file_bytes: bytes) -> pd.DataFrame:
    """Load portfolio from Excel bytes."""
    return pd.read_excel(BytesIO(file_bytes), engine="openpyxl")


def load_portfolio_from_csv(file_bytes: bytes) -> pd.DataFrame:
    """Load portfolio from CSV bytes."""
    return pd.read_csv(BytesIO(file_bytes))


# ─── CLI EXAMPLE USAGE ──────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Self Assist Tax Engine CLI ===\n")

    # Example 1: Single client
    rev = 24_00_000
    exp = 8_00_000
    normal = calculate_tax(rev, exp, presumptive_44ad=False)
    presumptive = calculate_tax(rev, presumptive_44ad=True)

    print(f"Turnover: ₹{rev:,} | Expenses: ₹{exp:,}\n")
    print("--- Normal Accounting ---")
    print(f"Taxable Income: ₹{normal['taxable_income']:,.2f}")
    print(f"Total Tax: ₹{normal['total_tax_liability']:,.2f}\n")

    print("--- Section 44AD (Presumptive) ---")
    print(f"Taxable Income: ₹{presumptive['taxable_income']:,.2f}")
    print(f"Total Tax: ₹{presumptive['total_tax_liability']:,.2f}\n")

    # Example 2: Batch processing
    portfolio = get_default_portfolio()
    updated = batch_calculate_tax(portfolio, use_presumptive=True)
    print("--- Portfolio (with tax) ---")
    print(updated[["Client Name", "FY 2025-26 Turnover (₹)", "Calculated Tax (₹)"]])
