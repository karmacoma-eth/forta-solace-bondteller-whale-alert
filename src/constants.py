from forta_agent import Network

ERC20_TRANSFER_ABI = '{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"}'

ZERO_ADDRESS = '0x0000000000000000000000000000000000000000'

SOLACE_TOKEN = 'SOLACE_TOKEN'
TELLER_ADDRESSES = 'TELLER_ADDRESSES'

CHAIN_CONFIG = {
    Network.MAINNET: {
        SOLACE_TOKEN: '0x501acE9c35E60f03A2af4d484f49F9B1EFde9f40',
        TELLER_ADDRESSES: {
            '0x501ACe677634Fd09A876E88126076933b686967a': 'DAI',
            '0x501ACe95141F3eB59970dD64af0405f6056FB5d8': 'ETH',
            '0x501ACE7E977e06A3Cb55f9c28D5654C9d74d5cA9': 'USDC',
            '0x501aCEF0d0c73BD103337e6E9Fd49d58c426dC27': 'WBTC',
            '0x501ACe5CeEc693Df03198755ee80d4CE0b5c55fE': 'USDT',
            '0x501ACe00FD8e5dB7C3be5e6D254ba4995e1B45b7': 'SCP',
            '0x501aCef4F8397413C33B13cB39670aD2f17BfE62': 'FRAX',
        }
    },

    'POLYGON': {
        SOLACE_TOKEN: '0x501acE9c35E60f03A2af4d484f49F9B1EFde9f40',
        TELLER_ADDRESSES: {
            '0x501ACe677634Fd09A876E88126076933b686967a': 'DAI',
            '0x501ACE7E977e06A3Cb55f9c28D5654C9d74d5cA9': 'USDC',
            '0x501aCEF0d0c73BD103337e6E9Fd49d58c426dC27': 'WBTC',
            '0x501ACe5CeEc693Df03198755ee80d4CE0b5c55fE': 'USDT',
            '0x501aCef4F8397413C33B13cB39670aD2f17BfE62': 'FRAX',
            '0x501Ace367f1865DEa154236D5A8016B80a49e8a9': 'WETH',
            '0x501aCe133452D4Df83CA68C684454fCbA608b9DD': 'MATIC',

        }
    },
}

TOKEN_THRESHOLD = 10 ** 24 # 1M SOLACE tokens, 10 ** 6 with 18 decimals
