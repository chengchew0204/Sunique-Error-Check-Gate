"""
Validators package for InFlow Error Check Gate.
Exports all validator classes for easy importing.
"""

# Import validators using importlib to handle filenames with hyphens
import importlib.util
import os

# Get the directory of this __init__.py file
_validators_dir = os.path.dirname(__file__)

# Import OrderFetcher from rule-0-order_fetcher.py
_spec_0 = importlib.util.spec_from_file_location(
    "rule_0_order_fetcher",
    os.path.join(_validators_dir, "rule-0-order_fetcher.py")
)
_rule_0_module = importlib.util.module_from_spec(_spec_0)
_spec_0.loader.exec_module(_rule_0_module)
OrderFetcher = _rule_0_module.OrderFetcher

# Import DiscountValidator from rule-1-discount.py
_spec_1 = importlib.util.spec_from_file_location(
    "rule_1_discount",
    os.path.join(_validators_dir, "rule-1-discount.py")
)
_rule_1_module = importlib.util.module_from_spec(_spec_1)
_spec_1.loader.exec_module(_rule_1_module)
DiscountValidator = _rule_1_module.DiscountValidator

# Import CreditCardFeeValidator from rule-2-credit_card.py
_spec_2 = importlib.util.spec_from_file_location(
    "rule_2_credit_card",
    os.path.join(_validators_dir, "rule-2-credit_card.py")
)
_rule_2_module = importlib.util.module_from_spec(_spec_2)
_spec_2.loader.exec_module(_rule_2_module)
CreditCardFeeValidator = _rule_2_module.CreditCardFeeValidator

# Import AssemblyFeeValidator from rule-3-assembly_fee.py
_spec_3 = importlib.util.spec_from_file_location(
    "rule_3_assembly_fee",
    os.path.join(_validators_dir, "rule-3-assembly_fee.py")
)
_rule_3_module = importlib.util.module_from_spec(_spec_3)
_spec_3.loader.exec_module(_rule_3_module)
AssemblyFeeValidator = _rule_3_module.AssemblyFeeValidator

# Import DeliveryFeeValidator from rule-4-delivery_fee.py
_spec_4 = importlib.util.spec_from_file_location(
    "rule_4_delivery_fee",
    os.path.join(_validators_dir, "rule-4-delivery_fee.py")
)
_rule_4_module = importlib.util.module_from_spec(_spec_4)
_spec_4.loader.exec_module(_rule_4_module)
DeliveryFeeValidator = _rule_4_module.DeliveryFeeValidator

# Import DiscountRemarkValidator from rule-5-discount_remark.py
_spec_5 = importlib.util.spec_from_file_location(
    "rule_5_discount_remark",
    os.path.join(_validators_dir, "rule-5-discount_remark.py")
)
_rule_5_module = importlib.util.module_from_spec(_spec_5)
_spec_5.loader.exec_module(_rule_5_module)
DiscountRemarkValidator = _rule_5_module.DiscountRemarkValidator

# Import ReturnReasonValidator from rule-6-return_reason.py
_spec_6 = importlib.util.spec_from_file_location(
    "rule_6_return_reason",
    os.path.join(_validators_dir, "rule-6-return_reason.py")
)
_rule_6_module = importlib.util.module_from_spec(_spec_6)
_spec_6.loader.exec_module(_rule_6_module)
ReturnReasonValidator = _rule_6_module.ReturnReasonValidator

# Import other validators
# TODO: Add other validator imports as they are implemented

__all__ = ['OrderFetcher', 'DiscountValidator', 'CreditCardFeeValidator', 'AssemblyFeeValidator', 'DeliveryFeeValidator', 'DiscountRemarkValidator', 'ReturnReasonValidator']

