"""
File: utils.py
Author: Sean Reilly
Description: Contains utily functions that are useful across multiple routes
"""
import re
from exceptions import OrderByException

def process_orderby(to_order, order_by: str):
    """
    Processes the $orderby query param so that it can be easily understood by
    SQLAlchemy

    Args:
        to_fetch: An object that maps onto the database data that's being ordered
        order_by: should have the name of the field that's being used to order
                  and optionally the order direction (asc or desc). If order
                  direction is unspecified the default is asc

    Returns:
        A SQLAlchemy expression that can be directly added to a query to order it
    """
    order_by = re.split('\s+', order_by)
    field = order_by[0]
    if field not in to_order.__table__.columns:
        column_names = str([column.name for column in to_order.__table__.columns])
        raise OrderByException(f"The field that's being ordered by must be one of {column_names}")
    field = getattr(to_order, field)
    
    direction = "asc"
    if (len(order_by) > 1):
        direction = order_by[1]
        if (direction not in ["asc", "desc"]):
            raise OrderByException("Order direction must be either ascending (asc)"
                                   " or descending (desc)")
    
    if direction == "asc":
        order_by = field.asc()
    elif direction == "desc":
        order_by = field.desc()
    
    return order_by
