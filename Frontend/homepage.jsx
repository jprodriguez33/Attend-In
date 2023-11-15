import './homepage.css';
import React, { useState, useEffect, useRef } from 'react';

function App() {
  return (
    <Navbar>
      <div className = "home_title"> Attend-In </div>
      <NavItem icon= "Menu">
        <DropdownMenu></DropdownMenu>
      </NavItem>
    </Navbar>
  );
}

function Navbar(props) {
  return (
    <nav className="navbar">
      <ul className="navbar-nav">{props.children}</ul>
    </nav>
  );
}

function NavItem(props) {
  const [open, setOpen] = useState(false);

  return (
    <li className="nav-item">
      <a href="#" className="icon-button" onClick={() => setOpen(!open)}>
        {props.icon}
      </a>

      {open && props.children}
    </li>
  );
}

function DropdownMenu() {
  const [activeMenu, setActiveMenu] = useState('main');

  function DropdownItem(props) {
    return (
      <a href="#" className="menu-item" onClick={() => props.goToMenu && setActiveMenu(props.goToMenu)}>
        <span className="icon-left">{props.leftIcon}</span>
        {props.children}
        <span className="icon-right">{props.rightIcon}</span>
      </a>
    );
  }

  return (
    <div className="dropdown"
        in={activeMenu === 'main'}
        timeout={500}
        classNames="menu-primary"
        unmountOnExit>

        <div className="menu">
          <DropdownItem>Attendance</DropdownItem>
          <DropdownItem>Assignments</DropdownItem>
          <DropdownItem>Log Out</DropdownItem>
           
        </div>
    </div>
    );
}

export default App;