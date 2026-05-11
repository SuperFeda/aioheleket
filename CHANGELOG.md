# Release 1.3.0

- Reworked HTTP request handling and added `RequestConfig` to configure it.
- `HeleketClient` can now be used with `async with`.
- All data classes have been rewritten to use `pydantic.BaseModel`.
- Added the `PaymentService.resend_webhook()` method.
- Docstrings now include links to the original Heleket API documentation.

# Release 1.2.0

- Added docstrings.
- Changed error messages.
- Added methods: `PayoutService.payout_history()` for retrieving payout history and `PaymentService.payment_history()` for payment history.
- The `test_webhook()` method for creating a test webhook was added to the `StaticWalletService` and `PayoutService` services.
- Renamed methods:
  - `HeleketClient.payment()` => `HeleketClient.payment_service()`
  - `HeleketClient.payout()` => `HeleketClient.payout_service()`
  - `HeleketClient.static_wallet()` => `HeleketClient.static_wallet_service()`
  - `HeleketClient.finance()` => `HeleketClient.finance_service()`
  - `PaymentService.info()` => `PaymentService.payment_info()`
  - `PaymentService.refund()` => `PaymentService.refund_payment()`
  - `PayoutService.get_info()` => `PayoutService.payout_info()`
  - `StaticWalletService.block()` => `StaticWalletService.block_wallet()`
  - `StaticWalletService.create()` => `StaticWalletService.create_wallet()`
- Renamed the `Currency` Enum to `CryptoCurrency`.
- The `FinanceService.balance()` method was changed; it now returns a single `Balance` object containing `user` and `merchant` balance data.
- Added a base parent class for all services - `_BaseService`.
- Added the alias `Currency` (`aioheleket.Currency`) to indicate that an argument can accept values for both fiat currency and cryptocurrency.
- Refactoring.
- The README was slightly modified and a Russian translation was added.

# Release 1.1.0

- Added FiatCurrency enum
- Removed installing setuptools lib with aioheleket

# Release 1.0.0

init
