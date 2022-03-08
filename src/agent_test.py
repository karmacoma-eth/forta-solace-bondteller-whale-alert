from unittest.mock import Mock
from .constants import ZERO_ADDRESS, SOLACE_TOKEN, TELLER_ADDRESSES, TOKEN_THRESHOLD, CHAIN_CONFIG
from forta_agent import create_transaction_event, Network
from .agent import handle_transaction
from dataclasses import dataclass, field

ETH_TELLER_ADDRESS='0x501ACe95141F3eB59970dD64af0405f6056FB5d8'
chain_config = CHAIN_CONFIG[Network.MAINNET]

def transfer_args(_from=ZERO_ADDRESS, _to=ETH_TELLER_ADDRESS, _value=TOKEN_THRESHOLD):
    return {
        'from': _from,
        'to': _to,
        'value': _value,
    }

@dataclass
class TransferEvent:
    address: str = chain_config[SOLACE_TOKEN]
    blockNumber: int = 42
    args: dict = field(default_factory=transfer_args)

mock_tx_event = create_transaction_event({})
mock_tx_event.filter_log = Mock()

class TestBondTellerWhales:
    def test_finds_bond_whale(self):
        # the default event satisfies all the criteria
        mock_tx_event.filter_log.return_value = [TransferEvent()]

        findings = handle_transaction(mock_tx_event)
        assert len(findings) == 1


    def test_multiple_findings_multiple_events(self):
        event1 = TransferEvent()
        event1.args['value'] = 2 * TOKEN_THRESHOLD

        event2 = TransferEvent()
        event2.args['value'] = 3 * TOKEN_THRESHOLD

        mock_tx_event.filter_log.return_value = [event1, event2]

        findings = handle_transaction(mock_tx_event)
        assert len(findings) == 2
        assert findings[0].metadata['value'] == event1.args['value']
        assert findings[1].metadata['value'] == event2.args['value']


    def test_no_findings_wrong_token(self):
        mock_tx_event.filter_log.return_value = [TransferEvent(address=ZERO_ADDRESS)]

        findings = handle_transaction(mock_tx_event)
        assert len(findings) == 0


    def test_no_findings_wrong_to_address(self):
        mock_tx_event.filter_log.return_value = [
            TransferEvent(args=transfer_args(_to=ZERO_ADDRESS))
        ]

        findings = handle_transaction(mock_tx_event)
        assert len(findings) == 0


    def test_no_findings_wrong_from_address(self):
        mock_tx_event.filter_log.return_value = [
            TransferEvent(args=transfer_args(_from=ETH_TELLER_ADDRESS))
        ]

        findings = handle_transaction(mock_tx_event)
        assert len(findings) == 0


    def test_no_findings_value_under_threshold(self):
        mock_tx_event.filter_log.return_value = [
            TransferEvent(args=transfer_args(_value=TOKEN_THRESHOLD / 2))
        ]

        findings = handle_transaction(mock_tx_event)
        assert len(findings) == 0
