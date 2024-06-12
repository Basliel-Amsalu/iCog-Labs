const vendingMachine = artifacts.require("vending_machine");

contract("vending_machine", (accounts) => {
  before(async () => {
    contractInstance = await vendingMachine.deployed();
  });

  it("maket sure that starting amount of the vending machine is 50", async () => {
    let amount = await contractInstance.getAmount();
    assert.equal(amount, 50, "initial amount should be 50");
  });
});
