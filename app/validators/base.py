from abc import ABC, abstractmethod
from typing import Dict, Any, List


class ValidationResult:
    """
    Represents the result of a validation rule.
    """
    
    def __init__(self, rule_name: str, passed: bool = True):
        """
        Initialize a validation result.
        
        Args:
            rule_name: Name of the validation rule
            passed: Whether the validation passed
        """
        self.rule_name = rule_name
        self.passed = passed
        self.issues: List[Dict[str, Any]] = []
        self.suggested_fixes: List[str] = []
        self.info_messages: List[str] = []
        self.fetched_data: Dict[str, Any] = {}  # For OrderFetcher to store formatted data
    
    def add_issue(self, message: str, severity: str = 'error', details: Dict[Any, Any] = None) -> None:
        """
        Add an issue to the validation result.
        
        Args:
            message: Description of the issue
            severity: 'error' or 'warning'
            details: Additional details about the issue
        """
        self.passed = False
        self.issues.append({
            'rule': self.rule_name,
            'message': message,
            'severity': severity,
            'details': details or {}
        })
    
    def add_suggested_fix(self, fix: str) -> None:
        """
        Add a suggested fix to the validation result.
        
        Args:
            fix: Description of the suggested fix
        """
        self.suggested_fixes.append(fix)
    
    def add_info(self, message: str) -> None:
        """
        Add an informational message to the validation result.
        
        Args:
            message: Informational message (not an error or warning)
        """
        self.info_messages.append(message)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert validation result to dictionary.
        
        Returns:
            Dictionary representation of the validation result
        """
        return {
            'rule': self.rule_name,
            'passed': self.passed,
            'issues': self.issues,
            'suggested_fixes': self.suggested_fixes,
            'info_messages': self.info_messages
        }


class BaseValidator(ABC):
    """
    Abstract base class for all validation rules.
    """
    
    def __init__(self, rule_name: str):
        """
        Initialize the base validator.
        
        Args:
            rule_name: Name of the validation rule
        """
        self.rule_name = rule_name
    
    @abstractmethod
    def validate(self, order_data: Dict[Any, Any]) -> ValidationResult:
        """
        Validate the order data.
        
        Args:
            order_data: Complete sales order data from InFlow
        
        Returns:
            ValidationResult object containing validation results
        """
        pass
    
    def _get_line_items(self, order_data: Dict[Any, Any]) -> List[Dict[Any, Any]]:
        """
        Extract line items from order data.
        
        Args:
            order_data: Sales order data
        
        Returns:
            List of line items
        """
        # InFlow API returns 'lines', not 'lineItems'
        return order_data.get('lines', order_data.get('lineItems', []))
    
    def _find_line_item_by_name(self, order_data: Dict[Any, Any], name_pattern: str, case_sensitive: bool = False) -> List[Dict[Any, Any]]:
        """
        Find line items matching a name pattern.
        
        Args:
            order_data: Sales order data
            name_pattern: Pattern to search for in product name
            case_sensitive: Whether the search should be case-sensitive
        
        Returns:
            List of matching line items
        """
        line_items = self._get_line_items(order_data)
        matching_items = []
        
        for item in line_items:
            product_name = item.get('product', {}).get('name', '')
            product_sku = item.get('product', {}).get('sku', '')
            
            if not case_sensitive:
                product_name = product_name.lower()
                product_sku = product_sku.lower()
                name_pattern = name_pattern.lower()
            
            if name_pattern in product_name or name_pattern in product_sku:
                matching_items.append(item)
        
        return matching_items

