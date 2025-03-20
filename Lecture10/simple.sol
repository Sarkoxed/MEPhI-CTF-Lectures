// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.8.25;

contract nameSys{
    struct nameEntry{
        address payable owner;
        uint256 value;
    }
    address payable public owner;
    mapping (bytes32 => nameEntry) data;

    event Register(address indexed sender, bytes32 indexed name, uint256 amount);
    event Update(address indexed newowner, bytes32 indexed name, uint256 amount);
    event Revoked(bytes32 indexed name);

    constructor(){
        owner = payable(msg.sender);
    }

    function nameNew(bytes32 name) public payable{
        require(data[name].owner == address(0), "Name already registered");
        require(msg.value >= 100, "Insufficient value sent");
        data[name].owner = payable(msg.sender);
        data[name].value = msg.value;
        // owner.transfer(msg.value);
        emit Register(msg.sender, name, msg.value);
    }

    function nameUpdate(bytes32 name, address newOwner) public payable{
        require(data[name].owner == msg.sender, "Not the name owner");
        require(msg.value >= 10, "Insufficient value sent");

        address payable previousOwner = data[name].owner;
        data[name].value += msg.value;
        data[name].owner = payable(newOwner);

        previousOwner.transfer(msg.value);
        emit Update(newOwner, name, data[name].value);
    }

    function revokeName(bytes32 name) public payable{
        require(data[name].owner == msg.sender, "Not the name owner");
        uint256 valueToSend = data[name].value;

        address payable previousOwner = data[name].owner;
        data[name].value = 0;
        data[name].owner = payable(address(0));
        previousOwner.transfer(valueToSend);
        emit Revoked(name);
    }

    function lookup(bytes32 name) public view returns (nameEntry memory){
        return data[name];
    }

    function get_owner() public view returns (address){
        return owner;
    }
}
