from rental.models import Invoice, CustomerProperty
from django.core.exceptions import ObjectDoesNotExist


# calculate_latest_electricity_unit_reading


def calculate_elr(myproperty, customer):
    try:
        latest_customer_property = CustomerProperty.objects.filter(
            is_terminated=False, myproperty=myproperty).latest('created_date')
    except ObjectDoesNotExist:
        latest_customer_property = None

    try:
        latest_invoice = Invoice.objects.filter(
            customer=customer, myproperty=myproperty).latest('created_date')
    except ObjectDoesNotExist:
        latest_invoice = None

    # Determine the latest electricity_unit_reading based on the latest record
    latest_reading = None

    if latest_customer_property and latest_invoice:
        if latest_customer_property.created_date > latest_invoice.created_date:
            latest_reading = latest_customer_property.electricity_unit_reading
        else:
            latest_reading = latest_invoice.current_electricity_unit_reading
    elif latest_customer_property:
        latest_reading = latest_customer_property.electricity_unit_reading
    elif latest_invoice:
        latest_reading = latest_invoice.current_electricity_unit_reading

    return latest_reading
