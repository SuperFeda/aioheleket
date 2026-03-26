from typing import Optional, Union, List, Dict
from datetime import datetime

from .base_service import _BaseService
from aioheleket.request_builder import RequestBuilder
from aioheleket.validation.fields import order_id128_adapter
from aioheleket.validation.schemas import (
    CreatePayment,
    Payment,
    Discount,
    Service,
    CreatePaymentRefund,
    History
)
from aioheleket.enums import PaymentStatus, CourseSource
from aioheleket.types.aliases import (
    NetworkStr,
    CryptoCurrencyStr,
    PaymentStatusStr,
    CourseSourceStr
)


class PaymentService(_BaseService):
    """
    Service for interacting with payments.
    """

    def __init__(self, request_builder: RequestBuilder):
        super().__init__(request_builder=request_builder)

    async def test_webhook(self,
                           url_callback: str,
                           currency: CryptoCurrencyStr,
                           network: NetworkStr,
                           status: PaymentStatusStr = PaymentStatus.PAID,
                           uuid: Optional[str] = None,
                           order_id: Optional[str] = None,
                           ) -> List:
        """
        To ensure that you are correctly receiving webhooks and can validate the signature,
        you should use this method to test webhooks for payment.

        doc https://doc.heleket.com/methods/payments/testing-webhook#testing_payment

        :param url_callback: URL to which webhooks with payment status will be sent (*)
        :param currency: Invoice crypro currency code (*)
        :param network: Invoice network code (*)
        :param status: Payment status (*)
        :param uuid: UUID of the invoice
        :param order_id: Order ID of the invoice

        :return: Empty list on successful processing
        """
        return await self._create_test_webhook(
            "/test-webhook/payment",
            url_callback=url_callback,
            currency=currency,
            network=network,
            status=status,
            uuid=uuid,
            order_id=order_id
        )

    async def resend_webhook(self, uuid: Union[str, None] = None, order_id: Union[str, None] = None) -> List:
        """
        Resend the webhook by invoice. You can resend the webhook only for finalized invoices,
        that is, invoices in statuses: ``wrong_amount``, ``paid``, ``paid_over``.

        To resend the webhook on the invoice, the url_callback must be specified at the time of invoice creation.

        (You need to pass one of the required parameters, if you pass both, the account will be identified by ``order_id``)

        doc https://doc.heleket.com/ru/methods/payments/resend-webhook

        :param uuid: Invoice uuid
        :param order_id: Invoice order ID

        :return: Empty list on successful processing
        """
        if uuid is None and order_id is None:
            raise ValueError("Required parameter not passed: uuid or order_id")

        if order_id:
            order_id128_adapter.validate_python(order_id)

        request_data = {
            "uuid": uuid,
            "order_id": order_id
        }
        result = await self._get_result_data("POST", "/payment/resend", request_data)
        return result

    async def create_invoice(self,
                             amount: str,
                             currency: CryptoCurrencyStr,
                             order_id: str,
                             lifetime: Optional[int] = 3600,
                             network: Optional[NetworkStr] = None,
                             url_callback: Optional[str] = None,
                             url_return: Optional[str] = None,
                             url_success: Optional[str] = None,
                             is_payment_multiple: bool = True,
                             to_currency: Optional[CryptoCurrencyStr] = None,
                             subtract: int = 0,
                             accuracy_payment_percent: int = 0,
                             additional_data: Optional[str] = None,
                             currencies: Optional[List[Dict[str, str]]] = None,
                             except_currencies: Optional[List[Dict[str, str]]] = None,
                             course_source: Optional[CourseSourceStr] = None,
                             from_referral_code: Optional[str] = None,
                             discount_percent: Optional[int] = None,
                             is_refresh: bool = False,
                             payer_email: Optional[str] = None
                             ) -> Payment:
        """
        Create new payment.

        doc https://doc.heleket.com/methods/payments/creating-invoice

        Args:
            amount (str): Amount to be paid. If there are pennies in the amount, then send
                them with a separator "``.``". Example: ``10.28``. (*)
            currency (Union[CryptoCurrency, str]): Currency code. (*)
            order_id (str): Order ID in your system. The parameter should be a string consisting of alphabetic characters,
                numbers, underscores, and dashes. It should not contain any spaces or special characters. (*)
            lifetime (Optional[int]): The lifespan of the issued invoice (in seconds).
            network (Optional[Union[Network, str]]): Blockchain network code.
            url_callback (Optional[str]): URL to which webhooks with payment status will be sent.
            url_return (Optional[str]): Before paying, the user can click on the button on the payment form and
                return to the store page at this URL.
            url_success (Optional[str]): After successful payment, the user can click on the button on
                the payment form and return to this URL.
            is_payment_multiple (bool): Whether the user is allowed to pay the remaining amount.
                This is useful when the user has not paid the entire amount of the invoice for one transaction,
                and you want to allow him to pay up to the full amount. If you disable this feature, the invoice will
                finalize after receiving the first payment and you will receive funds to your balance.
            to_currency (Optional[Union[CryptoCurrency, str]]): The parameter is used to specify the target currency
                for converting the invoice amount. When creating an invoice, you provide an amount and currency,
                and the API will convert that amount to the equivalent value in the ``to_currency``.
                (!! The ``to_currency`` should always be the cryptocurrency code, not a fiat currency code.)
            subtract (int): Percentage of the payment commission charged to the client. If you have a rate of 1%,
                then if you create an invoice for 100 USDT with subtract = 100 (the client pays 100% commission),
                the client will have to pay 101 USDT.
            accuracy_payment_percent (int): Acceptable inaccuracy in payment. For example, if you pass the value 5,
                the invoice will be marked as Paid even if the client has paid only 95% of the amount.
                The actual payment amount will be credited to the balance.
            additional_data (Optional[str]): Additional information for you (not shown to the client).
            currencies (Optional[List[Dict[str, str]]]): List of allowed currencies for payment.
                (Format: [{"currency": "USDT", "network": "ETH"}, {"currency": "USDC", "network": "POLYGON"}, ...]. Network is optional param.)
            except_currencies (Optional[List[Dict[str, str]]]): List of excluded currencies for payment.
                (Format: [{"currency": "USDT", "network": "ETH"}, {"currency": "USDC", "network": "POLYGON"}, ...]. Network is optional param.)
            course_source (Optional[CourseSource]): The service from which the exchange rates are taken for
                conversion in the invoice. If not passed, Heleket exchange rates are used.
            from_referral_code (Optional[str]): The merchant who makes the request connects to a referrer by code.
                For example, you are an application that generates invoices via the Heleket API and your customers
                are other stores. They enter their api key and merchant id in your application, and you send requests
                with their credentials and passing your referral code. Thus, your clients become referrals on your
                Heleket account and you will receive income from their turnover.
            discount_percent (Optional[int]): Positive numbers: Allows you to set a discount.
                To set a 5% discount for the payment, you should pass a value: 5;
                Negative numbers: Allows you to set custom additional commission.
                To set an additional commission of 10% for the payment, you should pass a value: -10.
            is_refresh (bool): Using this parameter, you can update the lifetime and get a new address for
                the invoice if the lifetime has expired. To do that, you need to pass all required parameters,
                and the invoice with passed order_id will be refreshed.
                (!! Only address, payment_status and expired_at are changed. No other fields are changed, regardless of the parameters passed.)
            payer_email (Optional[str]): Payer's email.

        Returns:
            Payment object.
        """
        payment_data = CreatePayment(
            amount=amount,
            currency=currency,
            order_id=order_id,
            lifetime=lifetime,
            network=network,
            url_callback=url_callback,
            url_return=url_return,
            url_success=url_success,
            is_payment_multiple=is_payment_multiple,
            to_currency=to_currency,
            subtract=subtract,
            accuracy_payment_percent=accuracy_payment_percent,
            additional_data=additional_data,
            currencies=currencies,
            except_currencies=except_currencies,
            course_source=course_source,
            from_referral_code=from_referral_code,
            discount_percent=discount_percent,
            is_refresh=is_refresh,
            payer_email=payer_email
        )
        request_data = payment_data.model_dump(exclude_none=False)
        result = await self._get_result_data("POST", "/payment", request_data)
        return Payment.model_validate(result)

    async def payment_info(self, *, uuid: Union[str, None] = None, order_id: Union[str, None] = None) -> Payment:
        """
        Get a payment info.

        To get the invoice status you need to pass one of the required parameters, if you pass both,
        the account will be identified by ``order_id``.

        doc https://doc.heleket.com/methods/payments/payment-information

        :param uuid: Invoice uuid
        :param order_id: Invoice order ID

        :return: payment object
        """
        if uuid is None and order_id is None:
            raise ValueError("Required parameter not passed: uuid or order_id")

        if order_id:
            order_id128_adapter.validate_python(order_id)

        request_data = {
            "uuid": uuid,
            "order_id": order_id
        }
        result = await self._get_result_data("POST", "/payment/info", request_data)
        return Payment.model_validate(result)

    async def generate_qr_code(self, payment_uuid: str) -> str:
        """
        Generate a QR-code for the invoice address

        doc https://doc.heleket.com/methods/payments/qr-code-pay-form

        :param payment_uuid: Invoice uuid

        :return: Base64 encode QR-code image
        """
        request_data = {
            "merchant_payment_uuid": payment_uuid
        }
        return await self._get_qr_image_base64("/payment/qr", request_data)

    async def refund_payment(self,
                             refund_address: str,
                             is_subtract: bool,
                             uuid: Union[str, None] = None,
                             order_id: Union[str, None] = None,
                             amount: Optional[str] = None
                             ) -> List:
        """
        Refund a payment

        (Invoice is identified by ``order_id`` or ``uuid``, if you pass both, the account will be identified by ``uuid``)

        doc https://doc.heleket.com/methods/payments/refund

        :param refund_address: The address to which the refund should be made (*)
        :param is_subtract: (*)
        :param uuid: Invoice uuid (*)
        :param order_id: Invoice order ID (*)
        :param amount: Refund amount

        :return: Empty list on successful processing
        """
        if uuid is None and order_id is None:
            raise ValueError("Required parameter not passed: uuid or order_id")

        if order_id:
            order_id128_adapter.validate_python(order_id)

        request_data = {
            "address": refund_address,
            "is_subtract": is_subtract,
            "uuid": uuid,
            "order_id": order_id,
            "amount": amount
        }
        CreatePaymentRefund.model_validate(request_data)
        result = await self._get_result_data("POST", "/payment/refund", request_data)
        return result

    async def payment_history(self,
                              date_from: Optional[datetime] = None,
                              date_to: Optional[datetime] = None
                              ) -> History:
        """
        Getting a payment history.

        doc https://doc.heleket.com/methods/payments/payment-history

        :param date_from: Filtering by creation date, from.
        :param date_to: Filtering by creation date, to.

        :return: History object
        """
        result = await self._get_history_data("/payment/list", date_from=date_from, date_to=date_to)
        return History.model_validate(result)

    async def services_info(self) -> List[Service]:
        """
        Returns a list of available payment services.
        Payment services store settings that are taken into account when creating an invoice.
        For example. currencies, networks, minimum and maximum limits, commissions.

        doc https://doc.heleket.com/methods/payments/list-of-services
        """
        return await self._get_services_info("/payment/services")

    async def discount_list(self) -> List[Discount]:
        """
        Getting discount data as a list

        doc https://doc.heleket.com/other/discount-payment/list-of-discounts
        """
        discount_data = await self._get_result_data("POST", "/payment/discount/list")
        return [Discount.model_validate(disc) for disc in discount_data]

    async def set_discount(self,
                           currency: CryptoCurrencyStr,
                           network: NetworkStr,
                           discount_percent: int
                           ) -> Discount:
        """
        Set discount to payment method.

        Positive Numbers (>0). Gives buyers a discount for paying with a coin.
        Good promotional tool if you want to give extra support to a particular coin.

        Negative Numbers (<0). Adds a certain percentage (padding) for paying with a coin. This could be used to
        cover your crypto/fiat conversion costs, make adjustments to match your local exchange, etc.

        doc https://doc.heleket.com/other/discount-payment/set-discount-to-payment-method

        :param currency: Currency code (*)
        :param network: Blockchain network code (*)
        :param discount_percent: Discount percent (*)

        :return: Discount object
        """
        request_data = {
            "network": network,
            "currency": currency,
            "discount_percent": discount_percent
        }
        Discount.model_validate(request_data)
        result = await self._get_result_data("POST", "/payment/discount/set", request_data)
        return Discount.model_validate(result)

