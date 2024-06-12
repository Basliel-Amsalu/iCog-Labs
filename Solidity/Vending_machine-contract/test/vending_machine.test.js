const vendingMachine = artifacts.require("vending_machine");

contract("vending_machine", (accounts) => {
  before(async () => {
    contractInstance = await vendingMachine.deployed();
  });

  it("makes sure that starting amount of the vending machine is 50", async () => {
    let amount = await contractInstance.getAmount();
    assert.equal(amount, 50, "initial amount should be 50");
  });

  it("allows purcahse", async () => {
    await contractInstance.purchase(1, {
      from: accounts[0],
      value: web3.utils.toWei("5", "ether"),
    });
    let amount = await contractInstance.getAmount();
    assert.equal(amount, 49, "amount should be 49 after purchase");
  });

  it("can restock", async () => {
    await contractInstance.restock(50);
    let amount = await contractInstance.getAmount();
    assert.equal(amount, 99, "amount should be 99 after restock");
  });
});
