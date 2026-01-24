from typing import Optional, Union, Tuple, List

from .base_service import _BaseService
from ..utils.request_builder import RequestBuilder
from ..enums import Network, CryptoCurrency, StaticWalletStatus
from ..utils.schemas import WalletScheme
from ..data_classes import Wallet


class StaticWalletService(_BaseService):
    """
    Service for managing static wallets
    """

    def __init__(self, request_builder: RequestBuilder):
        super().__init__(request_builder=request_builder)

    async def test_webhook(self,
                           url_callback: str,
                           currency: Union[CryptoCurrency, str],
                           network: Union[Network, str],
                           status: StaticWalletStatus = StaticWalletStatus.PAID,
                           uuid: Optional[str] = None,
                           order_id: Optional[str] = None,
                           ) -> List:
        """
        To ensure that you are correctly receiving webhooks and can validate the signature,
        you should use this method to test webhooks for payment.

        :param url_callback: URL to which webhooks with payment status will be sent (*)
        :param currency: Invoice crypro currency code (*)
        :param network: Invoice network code (*)
        :param status: Static wallet status (*)
        :param uuid: UUID of the invoice
        :param order_id: Order ID of the invoice

        :return: Empty list on successful processing
        """
        return await self._create_test_webhook(
            "/test-webhook/wallet",
            url_callback=url_callback,
            currency=currency,
            network=network,
            status=status,
            uuid=uuid,
            order_id=order_id
        )

    async def create_wallet(self,
                            currency: Union[CryptoCurrency, str],
                            network: Union[Network, str],
                            order_id: str,
                            url_callback: Optional[str] = None,
                            from_referral_code: Optional[str] = None
                            ) -> Wallet:
        """
        Creating a Static wallet

        Args:
            currency (Union[CryptoCurrency, str]): Currency code (*)
            network (Union[Network, str]): Blockchain network code (*)
            order_id (str): Order ID in your system. The parameter should be a string consisting of alphabetic characters,
                numbers, underscores, and dashes. It should not contain any spaces or special characters. (*)
            url_callback (Optional[str]): URL, to which the webhook will be sent after each top-up of the wallet
            from_referral_code (Optional[str]): The merchant who makes the request connects to a referrer by code.
                For example, you are an application that generates invoices via the Heleket API and your customers
                are other stores. They enter their api key and merchant id in your application, and you send
                requests with their credentials and passing your referral code. Thus,
                your clients become referrals on your Heleket account and you will receive income from their turnover.

        Returns:
            Wallet object
        """
        request_data = {
            "currency": currency,
            "order_id": order_id,
            "network": network,
            "url_callback": url_callback,
            "from_referral_code": from_referral_code
        }
        WalletScheme.model_validate(request_data)
        result = await self._get_result_data("POST", "/wallet", request_data)
        return Wallet(**result)

    async def block_wallet(self,
                           uuid: Union[str, None] = None,
                           order_id: Union[str, None] = None,
                           is_force_refund: bool = False
                           ) -> Tuple[str, StaticWalletStatus]:
        """
        Block static wallet.

        When you need to block your clients static wallet, all the further payments will not be credited to
        his balance. You can make a refund of this funds only once. The funds will be returned to
        the addresses from which they came.

        (! You need to pass one of the required parameters, if you pass both, the account will be identified by order_id)

        :param uuid: uuid of a static wallet
        :param order_id: Order ID of a static wallet
        :param is_force_refund: Refund all incoming payments to sender’s address

        :return: A tuple where the first element is the wallet UUID and the second is its status.
        """
        if uuid is None and order_id is None:
            raise ValueError("Required parameter not passed: uuid or order_id")
        if uuid is not None and order_id is not None:
            raise ValueError("one of the parameters must be passed: uuid or order_id")

        request_data = {
            "uuid": uuid,
            "order_id": order_id,
            "is_force_refund": is_force_refund
        }
        result = await self._get_result_data("POST", "/wallet/block-address", request_data)
        wallet_uuid = result.get("uuid")
        wallet_status = result.get("status")

        return wallet_uuid, wallet_status

    async def generate_qr_code(self, wallet_uuid: str) -> str:
        """
        Generate a QR-code for the static wallet address

        :param wallet_uuid: uuid of a static wallet

        :return: Base64 encode QR-code image
        """
        request_data = {
            "wallet_address_uuid": wallet_uuid
        }
        return await self._get_qr_image_base64("/wallet/qr", request_data)

    async def blocked_address_refund(self,
                                     refund_address: str,
                                     uuid: Union[str, None] = None,
                                     order_id: Union[str, None] = None
                                     ) -> Tuple[str, str]:
        """
        Refund payments on blocked address.

        You can make a refund only once.

        (! To refund payments you need to pass either uuid or ``order_id``, if you pass both, the static wallet will be identified by ``uuid``)

        :param refund_address: Refund all blocked funds to this address (*)
        :param uuid: uuid of a static wallet (*)
        :param order_id: Order ID of a static wallet (*)

        :return: A tuple where the first element is the refund commission and the second is its amount of refund.
        """
        if uuid is None and order_id is None:
            raise ValueError("Required parameter not passed: uuid or order_id")
        if uuid is not None and order_id is not None:
            raise ValueError("one of the parameters must be passed: uuid or order_id")

        request_data = {
            "uuid": uuid,
            "order_id": order_id,
            "address": refund_address
        }
        result = await self._get_result_data("POST", "/wallet/blocked-address-refund", request_data)
        refund_commission = result.get("commission")
        refund_amount = result.get("amount")

        return refund_commission, refund_amount

