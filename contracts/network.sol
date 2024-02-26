// SPDX-License-Identifier: MIT
pragma solidity 0.8.19;

contract network {
// only owner -admin

address owner;


address[] _commanders;
string [] _commandernames;
uint[] _commanderpasswords;

mapping(address=> bool) _c;


constructor(){
    owner= msg.sender;
}

modifier onlyOwner{
    require(owner==msg.sender);
    _;
}


//Admin can only-  trasaction..
function addCommanders(address wallet,string memory name,uint password) public onlyOwner {

require(!_c[wallet]);

_commanders.push(wallet);
_commandernames.push(name);
_commanderpasswords.push(password);

_c[wallet]=true;


}


// Any one can..
function login(address wallet,uint password) public view returns(bool){

require(_c[wallet]);

for(uint i=0;i<_commanders.length;i++)
{
    if(_commanders[i]==wallet && _commanderpasswords[i]==password)
    {
        return true;
    }
}

return false;

}


//Any one can...
function viewCommanders() public view returns(address[] memory ,string[] memory){

return( _commanders,_commandernames);
}


}
