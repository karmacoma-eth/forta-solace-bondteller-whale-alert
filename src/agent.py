from forta_agent import Finding, FindingType, FindingSeverity, get_web3_provider

from .constants import ERC20_TRANSFER_ABI, SOLACE_TOKEN_ADDRESS, ZERO_ADDRESS, TELLER_ADDRESSES, TOKEN_THRESHOLD


MEDIUM_GAS_THRESHOLD = 1000000
HIGH_GAS_THRESHOLD = 3000000
CRITICAL_GAS_THRESHOLD = 7000000


def handle_transaction(transaction_event):
    '''
    BondTeller Monitoring Whale Alert, listens for large deposits (>= 1M SOLACE tokens created)

    Looks for:
    1. ERC20 Transfer events
    2. emitted by the SOLACE token
    3. that represent mints of new tokens (from is the 0 address)
    4. to a teller address
    5. where the value is greater than 1M tokens
    '''
    findings = []

    # 1. ERC20 Transfer events
    transfers = transaction_event.filter_log(ERC20_TRANSFER_ABI)

    web3 = get_web3_provider()
    for transfer in transfers:

        # 2. emitted by the SOLACE token
        if web3.toChecksumAddress(transfer.address) != SOLACE_TOKEN_ADDRESS:
            continue

        # 3. that represent mints of new tokens (from is the 0 address)
        if transfer.args['from'] != ZERO_ADDRESS:
            continue

        # 4. to a teller address
        if web3.toChecksumAddress(transfer.args['to']) not in TELLER_ADDRESSES:
            continue

        # 5. where the value is greater than 1M tokens
        if transfer.args['value'] < TOKEN_THRESHOLD:
            print('Skipping bond payout under threshold:', transfer.args['value'] / 10 ** 18)
            continue

        findings.append(Finding({
            'name': 'BondTeller Monitoring Whale Alert',
            'description': f'Large deposit in a BondTeller contract detected',
            'alert_id': 'SOLACEWHALE-1',
            'type': FindingType.Info,
            'severity': FindingSeverity.Info,
            'metadata': {
                'bond_teller_address': transfer.args['to'],
                'bond_teller': TELLER_ADDRESSES[transfer.args['to']],
                'value': transfer.args['value'],
            }
        }))

    return findings
