import json


def test_get_assets_missing_arguments(client):
    response = client.get('/wallet_assets')
    data = json.loads(response.data)
    assert response.status_code == 400
    assert 'missing arguments' in data['error']


def test_get_assets_success(client, mocker):
    mock_query_wallet = mocker.patch('src.main.query_wallet')
    mock_query_wallet.return_value = mocker.Mock(error=False, data=mocker.Mock(items=[
        mocker.Mock(contract_display_name='TokenA', quote=100),
        mocker.Mock(contract_display_name='TokenB', quote=200),
    ]))
    response = client.get('/wallet_assets?walletAddress=wallet_address&chainName=cool_chain_name')
    data = json.loads(response.data)
    assert response.status_code == 200
    assert 'tokens' in data
    assert len(data['tokens']) == 2