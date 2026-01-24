from datetime import datetime
from typing import Optional, Union, List

from .base_service import _BaseService
from ..types.aliases import Currency
from ..utils.request_builder import RequestBuilder
from ..enums import (
    Network,
    CryptoCurrency,
    CourseSource,
    Priority,
    PayoutStatus
)
from ..utils.schemas import PayoutScheme
from ..data_classes import (
    Service,
    Payout,
    Transfer,
    PayoutConvert,
    PayoutSum,
    History,
    Pagination,
    PayoutDataInHistory
)


class PayoutService(_BaseService):
    """
    Service for managing payouts
    """

    def __init__(self, request_builder: RequestBuilder):
        super().__init__(request_builder=request_builder)

    async def test_webhook(self,
                           url_callback: str,
                           currency: Union[CryptoCurrency, str],
                           network: Union[Network, str],
                           status: PayoutStatus = PayoutStatus.PAID,
                           uuid: Optional[str] = None,
                           order_id: Optional[str] = None,
                           ) -> List:
        """
        To ensure that you are correctly receiving webhooks and can validate the signature,
        you should use this method to test webhooks for payout.

        :param url_callback: URL to which webhooks with payment status will be sent (*)
        :param currency: Invoice crypro currency code (*)
        :param network: Invoice network code (*)
        :param status: payout status (*)
        :param uuid: UUID of the invoice
        :param order_id: Order ID of the invoice

        :return: Empty list on successful processing
        """
        return await self._create_test_webhook(
            "/test-webhook/payout",
            url_callback=url_callback,
            currency=currency,
            network=network,
            status=status,
            uuid=uuid,
            order_id=order_id
        )

    async def create_invoice(self,
                             amount: str,
                             currency: Currency,
                             order_id: str,
                             address: str,
                             is_subtract: bool,
                             network: Union[Network, str],
                             url_callback: Optional[str] = None,
                             to_currency: Optional[CryptoCurrency] = None,
                             course_source: Optional[CourseSource] = None,
                             from_currency: Optional[str] = None,
                             priority: Optional[Priority] = Priority.RECOMMENDED,
                             memo: Optional[str] = None
                             ) -> Payout:
        """
        Creating a payout.

        The payouts through API are made only from your business wallets balances.

        Payouts can be made in different ways:

        1) You can choose to receive the payout in a specific cryptocurrency and the payout will then be
        automatically processed in that specific cryptocurrency. To do so, ensure that
        you have sufficient balance in that particular currency to cover all associated fees.

        2) Alternatively, you have the option to specify the payout amount in a fiat currency. In this case,
        the amount will be automatically converted to a specific cryptocurrency from your available balance. For instance,
        if you request a payout of 20 USD in LTC, the equivalent value will be deducted from your LTC balance.
        It is important to have enough funds in the corresponding cryptocurrency to cover all applicable fees.

        3) Another possibility is to specify the payout amount in a fiat currency, which will be automatically converted
        to a specific cryptocurrency using your USDT balance. This option is particularly useful when you have
        autoconvert enabled, as funds from your invoices are automatically converted to USDT. For example,
        if you want to make a payout of 20 USD in LTC but only have a balance in USDT, make sure you have
        sufficient USDT funds to cover all fees.

        4) Additionally, you can choose to specify the payout amount in any cryptocurrency of your preference.
        The payout will then be automatically processed in that specific cryptocurrency,
        utilizing your available USDT balance. It is crucial to have enough USDT balance to cover all associated fees.

        Args:
            amount (str): Payout amount
            currency (Currency): Currency code for the payout. If Currency if fiat, the to_currency parameter is required.
            network (Union[Network, str]): Blockchain network code. Not required when the currency/to_currency is a cryptocurrency
                and has only one network, for example BTC
            order_id (str): Order ID in your system. The parameter should be a string consisting of alphabetic characters,
                numbers, underscores, and dashes. It should not contain any spaces or special characters.
            address: The address of the wallet to which the withdrawal will be made
            is_subtract (bool): Defines where the withdrawal fee will be deducted:
                ``True`` - from your balance;
                ``False`` - from payout amount, the payout amount will be decreased
            url_callback (Optional[str]): URL to which webhooks with payout status will be sent
            course_source (Optional[CourseSource]): The service from which the exchange rates are taken for
                conversion in the invoice. The parameter is applied only if the currency is fiat,
                otherwise the default value is taken from the merchant's settings.
            priority (Optional[Priority]): The parameter for selecting the withdrawal priority.
                The cost of the withdrawal fee  depends on the selected parameter.
                This parameter is applied only in case of using the BTC, ETH, POLYGON, and BSC networks.
            to_currency (Optional[CryptoCurrency]): Cryptocurrency code in which the payout will be made.
                It is used when the currency parameter is fiat.
            from_currency (Optional[str]): Allows to automatically convert the withdrawal amount and
                use the from_currency balance. Only USDT is available.
            memo (Optional[str]): Additional identifier for TON, used to specify a particular recipient or target

        Returns:
            Payout object
        """
        request_data = {
            "amount": amount,
            "currency": currency,
            "order_id": order_id,
            "address": address,
            "is_subtract": is_subtract,
            "network": network,
            "url_callback": url_callback,
            "to_currency": to_currency,
            "course_source": course_source,
            "from_currency": from_currency,
            "priority": priority,
            "memo": memo,
        }
        PayoutScheme.model_validate(request_data)
        result = await self._get_result_data("POST", "/payout", request_data)

        convert_data = result.get("convert", None)
        if convert_data is not None:
            convert_data = PayoutConvert(**convert_data)
            result.pop("convert")

        return Payout(convert=convert_data, **result)

    async def calc(self,
                   amount: str,
                   address: str,
                   currency: Currency,
                   is_subtract: bool,
                   to_currency: Optional[str],
                   network: Optional[Union[Network, str]],
                   course_source: Optional[Union[CourseSource, str]],
                   priority: Optional[Union[Priority, str]] = Priority.RECOMMENDED
                   ) -> PayoutSum:
        """
        Calculation of the withdrawal amount.

        Args:
            amount (str): Payout amount. (*)
            address (str): The address of the wallet to which the withdrawal will be made. (*)
            network (Optional[Union[Network, str]]): Blockchain network code.
                Not required when the currency/to_currency is a cryptocurrency and has only one network,
                for example BTC. (*)
            is_subtract (bool): Defines where the withdrawal fee will be deducted:
                ``True`` - from your balance;
                ``False`` - from payout amount, the payout amount will be decreased; (*)
            currency (Currency): Currency code for the payout. If Currency if fiat, the to_currency parameter is required.
            to_currency (Optional[str]): Cryptocurrency code in which the payout will be made.
                It is used when the currency parameter is fiat.
            course_source (Optional[Union[CourseSource, str]]): The service from which the exchange rates are taken for conversion in the invoice.
                The parameter is applied only if the currency is fiat,
                otherwise the default value is taken from the merchant's settings.
            priority (Optional[Union[Priority, str]]): The parameter for selecting the withdrawal priority. The cost of the withdrawal fee depends
                on the selected parameter. This parameter is applied only in case of using
                the BTC, ETH, POLYGON, and BSC networks.

        Returns:
            Sum object
        """
        request_data = {
            "amount": amount,
            "address": address,
            "currency": currency,
            "is_subtract": is_subtract,
            "to_currency": to_currency,
            "network": network,
            "course_source": course_source,
            "priority": priority
        }
        result = await self._get_result_data("POST", "/payout/calc", request_data)

        return PayoutSum(**result)

    async def transfer_to_personal_wallet(self, amount: str, currency: Union[CryptoCurrency, str]) -> Transfer:
        """
        Transfer to personal wallet.

        :param amount: Amount to transfer
        :param currency: Currency code. **Only cryptocurrency code is allowed**.

        :return: Transfer object
        """
        return await self._transfer(amount=amount, currency=currency, endpoint="/transfer/to-personal")

    async def transfer_to_business_wallet(self, amount: str, currency: Union[CryptoCurrency, str]) -> Transfer:
        """
        Transfer to business wallet.

        :param amount: Amount to transfer
        :param currency: Currency code. **Only cryptocurrency code is allowed**.

        :return: Transfer object
        """
        return await self._transfer(amount=amount, currency=currency, endpoint="/transfer/to-business")

    async def _transfer(self, *, amount: str, currency: Union[CryptoCurrency, str], endpoint: str) -> Transfer:
        request_data = {
            "amount": amount,
            "currency": currency
        }
        result = await self._get_result_data("POST", endpoint, request_data)
        return Transfer(**result)

    async def payout_info(self, *, uuid: Union[str, None] = None, order_id: Union[str, None] = None) -> Payout:
        """
        Get a payout info.

        (! To get the payout information you need to pass one of the parameters, if you pass both, the payout will be identified by ``order_id``)

        :param uuid: Invoice uuid
        :param order_id: Invoice order ID

        :return: payout object
        """
        if uuid is None and order_id is None:
            raise ValueError("Required parameter not passed: uuid or order_id")
        if uuid is not None and order_id is not None:
            raise ValueError("one of the parameters must be passed: uuid or order_id")

        request_data = {
            "uuid": uuid,
            "order_id": order_id
        }
        result = await self._get_result_data("POST", "/payout/info", request_data)

        return Payout(**result)

    async def payout_history(self,
                              date_from: Optional[Union[str, datetime]] = None,
                              date_to: Optional[Union[str, datetime]] = None
                              ) -> History:
        """
        Getting a payout history.

        :param date_from: Filtering by creation date, from.
        :param date_to: Filtering by creation date, to.

        Date format: YYYY-MM-DD H:mm:ss

        :return: History object
        """
        result = await self._get_history_data("/payout/list", date_from=date_from, date_to=date_to)
        paginate = Pagination(**result.pop("paginate"))

        payouts = []
        for payout_data in result.get("items"):
            created_at_data = payout_data.pop("created_at")
            updated_at_data = payout_data.pop("updated_at")
            payouts.append(PayoutDataInHistory(
                created_at=datetime.fromisoformat(created_at_data),
                updated_at=datetime.fromisoformat(updated_at_data),
                **payout_data
            ))

        return History(paginate=paginate, items=payouts)

    async def services_info(self) -> List[Service]:
        """
        Returns a list of available payout services.
        Payout services store settings that are taken into account when creating a payout.
        For example. currencies, networks, minimum and maximum limits, commissions.
        """
        return await self._get_services_info("/payout/services")

