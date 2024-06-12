// SPDX-License-Identifier: MIT
pragma solidity ^0.8.11;

contract vending_machine {
  address public owner;
  mapping (address => uint) public candyBarStock;

  constructor() {
    owner = msg.sender;
    candyBarStock[address(this)] = 50;
  }

}
