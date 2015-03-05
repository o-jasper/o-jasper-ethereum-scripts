#!/bin/bash

echo 'function createContract(key, fun) {
    transact_code(key, "0x'$(cat build/grudge-escrow.evm)'", fun);
}'
