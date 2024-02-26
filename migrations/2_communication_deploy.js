const communication = artifacts.require('communication');

module.exports= function(deployer){
    deployer.deploy(communication);
}