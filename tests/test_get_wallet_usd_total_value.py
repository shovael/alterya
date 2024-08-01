import json


def test_get_wallet_usd_total_value_missing_arguments(client):
    response = client.get('/wallet_usd_total_value')
    data = json.loads(response.data)
    assert response.status_code == 400
    assert 'missing arguments' in data['error']


def test_get_wallet_usd_total_value_success(client, mocker):
    mock_query_wallet = mocker.patch('src.main.query_wallet')
    mock_query_wallet.return_value = mocker.Mock(error=False, data=mocker.Mock(items=[
        mocker.Mock(quote=100),
        mocker.Mock(quote=200),
    ]))
    response = client.get('/wallet_usd_total_value?walletAddress=wallet_address&chainName=cool_chain_name')
    data = json.loads(response.data)
    assert response.status_code == 200
    assert 'total value' in data
    assert data['total value'] == 300