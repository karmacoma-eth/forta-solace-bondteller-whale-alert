# Solace BondTeller Monitoring Whale Alert


## Description

This agent detects large deposits to Solace BondTeller contracts (>= 1M SOLACE tokens created)

These can happen via [deposit()](https://docs.solace.fi/docs/dev-docs/Contracts/bonds/BondTellerErc20#deposit) or [depositSigned()](https://docs.solace.fi/docs/dev-docs/Contracts/bonds/BondTellerErc20#depositsigned) and can be staked or not, but internally `_deposit()` always mints new tokens to the relevant BondTeller contract.

Therefore, this agent looks for:

1. ERC20 Transfer events
2. emitted by the SOLACE token
3. that represent mints of new tokens (`from` is the 0 address)
4. to a teller address
5. where the value is greater than 1M tokens

## Supported Chains

- Ethereum

TODO:
- Polygon

## Alerts

- SOLACEWHALE-1
  - Fired when there is a large deposit to a BondTeller
  - type: info
  - severity: info
  - metadata:
    - bond_teller_address: the address of the contract that received the deposit
    - bond_teller: a human readable name describing the principal of that bond teller (such as `ETH` or `USDC`)
    - value: the number of tokens transferred (no divided by the tokens `decimals()`)

## Test Data

This Ethereum transaction can be used to verify the detection logic:

`0x163f0fd3470898190743efd1702fbc9cce73d0a94d60a55fddd5a303885113a2`

It corresponds to a BondTeller deposit with a payout of 276k SOLACE tokens, under the threshold. As a result, running the agent prints a log message:

```
$ npm run tx 0x163f0fd3470898190743efd1702fbc9cce73d0a94d60a55fddd5a303885113a2

> forta-agent-solace-bondteller-monitoring-whale@0.0.1 tx
> forta-agent run --tx "0x163f0fd3470898190743efd1702fbc9cce73d0a94d60a55fddd5a303885113a2"

Skipping bond payout under threshold: 276197.70995
0 findings for transaction 0x163f0fd3470898190743efd1702fbc9cce73d0a94d60a55fddd5a303885113a2
```