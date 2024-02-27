// SPDX-License-Identifier: MIT
pragma solidity 0.8.19;

contract network {

    address owner;

    address[] _commanders;
    string[] _quantumtokens;
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

    function addCommanders(address wallet,string memory name,uint password,string memory token) public onlyOwner {

        require(!_c[wallet]);

        _commanders.push(wallet);
        _commandernames.push(name);
        _commanderpasswords.push(password);
        _quantumtokens.push(token);
        _c[wallet]=true;
    }

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

    function viewCommanders() public view returns(address[] memory ,string[] memory,uint[] memory,string[] memory){
        return( _commanders,_commandernames,_commanderpasswords,_quantumtokens);
    }

    function verifyToken(address wallet,string memory token) public view returns(bool){
        uint i;

        for(i=0;i<_quantumtokens.length;i++){
            if(wallet==_commanders[i] && (keccak256(abi.encodePacked(token)) == keccak256(abi.encodePacked(_quantumtokens[i])))){
                return true;
            }
        }
        return false;
    }

}