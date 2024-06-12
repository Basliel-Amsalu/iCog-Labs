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

  function purchase(uint amount) public payable{
    require(msg.value >= amount * 2 ether, "2 ETH per candy");
    require(candyBarStock[address(this)] >= amount, "Not enough candies in stock");
    candyBarStock[address(this)] -= amount;
    candyBarStock[msg.sender] += amount;
  }

}
