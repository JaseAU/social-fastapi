import pytest
from app.calculations import add, subtract, multiply, divide, BankAccount, InsufficientFunds

# test_*
@pytest.fixture
def zero_bank_account():
    return BankAccount(0)


@pytest.fixture
def bank_account():
    return BankAccount(50)

@pytest.mark.parametrize("num1, num2, expected", [
    (3, 2, 5),
    (7, 1, 8),
    (12, 4, 16)
])
def test_add(num1, num2, expected):
    print("testing add function")
    assert add(num1, num2) == expected


def test_subract():
    print("testing subtract function")
    assert subtract(9, 4) == 5


def test_multiply():
    print("testing multiply function")
    assert multiply(3, 4) == 12


def test_divide():
    print("testing divide function")
    assert divide(8, 2) == 4


def test_bank_set_iniitial_amount(bank_account):
    assert bank_account.balance == 50


def test_bank_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0


def test_withdraw(bank_account):
    bank_account.withdraw(20)
    assert bank_account.balance == 30


def test_deposit(bank_account):
    bank_account.deposit(30)
    assert bank_account.balance == 80


def test_collect_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance, 6) == 55

@pytest.mark.parametrize("deposited, withdrawn, expected", [
    (200, 100, 100),
    (50, 10, 40),
    (1200, 200, 1000),
    (10, 5, 5)
])
def test_bank_transaction(zero_bank_account, deposited, withdrawn, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrawn)
    assert zero_bank_account.balance == expected



def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(200)