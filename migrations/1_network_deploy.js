const network = artifacts.require('network');

module.exports= function(deployer){
    deployer.deploy(network);
}