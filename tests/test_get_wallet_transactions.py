import json


def test_get_wallet_transactions_missing_arguments(client):
    response = client.get('/wallet_transactions')
    data = json.loads(response.data)
    assert response.status_code == 400
    assert 'missing arguments' in data['error']


def test_get_wallet_transactions_success(client, mocker):
    mock_get = mocker.patch('requests.get')
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.text = json.dumps({
        "data": {
            "transactions": [
                {"tx_hash": "0x1", "value": "100"},
                {"tx_hash": "0x2", "value": "200"},
            ]
        }
    })
    mock_get.return_value = mock_response
    response = client.get('/wallet_transactions?walletAddress=wallet_address&chainName=cool_chain_name&page=1')
    data = json.loads(response.data)
    assert response.status_code == 200
    assert 'transactions' in data
