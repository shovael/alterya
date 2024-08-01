from covalent import CovalentClient


def query_wallet(convalent_api_key, chain_name, wallet_address, **args):
    covalent_client = CovalentClient(convalent_api_key)
    balance = covalent_client.balance_service.get_token_balances_for_wallet_address(
        chain_name=chain_name, wallet_address=wallet_address, **args
    )
    return balance
