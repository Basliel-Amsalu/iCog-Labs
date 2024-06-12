// SPDX-License-Identifier: MIT
pragma solidity ^0.5.11;

contract vending_machine {
  address public owner;
  mapping (address => uint) public candyBarStock;

  constructor() public {
    owner = msg.sender;
    candyBarStock[address(this)] = 50;
  }

  function getAmount() public view returns (uint){
    return candyBarStock[address(this)];
  }
  


