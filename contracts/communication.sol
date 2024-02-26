// SPDX-License-Identifier: MIT
pragma solidity 0.8.19;

contract communication {


string[] _messages;
address[] from_message;
address[] to_message;



address[]  from_file;
string[]  _filehash;
address[][] _owners; //to whom...

mapping(string =>bool) _f;



function sendMessage(address from,address to,string memory message) public{

_messages.push(message);
from_message.push(from);
to_message.push(to);


}

function viewMessages()public view returns(string[] memory,address[] memory,address[] memory){

return(_messages,from_message,to_message);
}



function sendFiles(address wallet,string memory filehash,address[] memory to) public{

require(!_f[filehash]);

from_file.push(wallet);
_filehash.push(filehash);
_owners.push(to);

_f[filehash]=true;

}

function viewFiles() public view returns(address[] memory, string [] memory, address[][] memory)
{

return (from_file,_filehash,_owners);

}


}
