const vending_machine = artifacts.require("vending_machine");

module.exports = function (deployer) {
  deployer.deploy(vending_machine);
};
