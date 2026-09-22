"""
HW1 starter code.
"""

from pathlib import Path


def amortize(apr, years, balance, monthly_pmt=None):
    """
    Projects an amortization schedule for a loan with monthly payments.

    Parameters
    ----------
    apr : float
        The annual percentage rate on the loan.
    years : int
        The term of the loan, in years.
    balance : float
        The initial balance of the loan.
    monthly_pmt : float, optional
        A specific monthly payment amount. If None is provided, the monthly
        payment amount should be solved to perfectly amortize the loan at the
        end of the term.

    Returns
    -------
        An object of type dict[str, list] containing the projected values.
    """
    n = years * 12
    rate = apr / 12

    if monthly_pmt is None:
        if rate == 0:
            monthly_pmt = balance / n
        else:
            v = 1 / (1 + rate)
            ann = (1 - v**n) / rate
            monthly_pmt = balance / ann

    schedule = {
        "period": [],
        "start_bal": [],
        "interest": [],
        "bal_after_int": [],
        "pmt": [],
        "bal_after_pmt": [],
        "principal_repaid": [],
    }

    current_balance = balance
    for month in range(1, n + 1):
        start_bal = current_balance
        interest = start_bal * rate
        bal_after_int = start_bal + interest

        if month == n:
            pmt = bal_after_int
        else:
            pmt = min(monthly_pmt, bal_after_int)

        bal_after_pmt = bal_after_int - pmt
        principal_repaid = start_bal - bal_after_pmt

        schedule["period"].append(month)
        schedule["start_bal"].append(start_bal)
        schedule["interest"].append(interest)
        schedule["bal_after_int"].append(bal_after_int)
        schedule["pmt"].append(pmt)
        schedule["bal_after_pmt"].append(bal_after_pmt)
        schedule["principal_repaid"].append(principal_repaid)

        if bal_after_pmt <= 1e-10:
            break
        current_balance = bal_after_pmt

    return schedule


def write_csv(fname, amortization_schedule, round_precision=2):
    """
    Writes an amortization schedule to a file in CSV format. There's some
    assertions in here to help you check your amortization_schedule is valid.

    Parameters
    ----------
    fname : str
        The name of the file.
    amortization_schedule
        An object returned by the `amortize` function.
    round_precision : float, optional
        Number of decimals to round to, by default 2.
    """

    file = Path(fname)
    folder = file.parent
    if not folder.exists():
        raise ValueError(f"Whoops, directory '{folder}' does not exist.")

    assert isinstance(amortization_schedule, dict), (
        "amortization_schedule is not a dictionary"
    )

    lengths = set()
    columns = amortization_schedule.values()
    assert len(columns) > 0, "Dictionary has no keys!"
    for col in columns:
        lengths.add(len(col))
    assert len(lengths) == 1, "Mismatch in length of lists in amortization_schedule"

    headers = list(amortization_schedule.keys())
    length = lengths.pop()
    with open(file, "w") as f:
        f.write(",".join(headers) + "\n")
        for i in range(length):
            record = []
            for header, col in zip(headers, columns):
                value = col[i]
                if header == "period":
                    if value == 0:
                        break
                    else:
                        record.append(str(value))
                else:
                    record.append(f"{value:0.{round_precision}f}")
            f.write(",".join(record) + "\n")
