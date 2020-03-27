import React from 'react';
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import logo from './logo.svg';
import './App.css';

import LibraryRequest from './LibraryRequest';
import ReaderRequest from './ReaderRequest';
import AuthorRequest from './AuthorRequest';

import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import AppBar from '@material-ui/core/AppBar';

function App() {
  return (
    <div className="App">
      <div>Library Management System</div>
      <Router>
        <div className="navigation-bar">
          <Tabs variant="fullWidth">
            <Tab color="primary" label="Library" component={Link} to="/library"></Tab>
            <Tab color="primary" label="Reader" component={Link} to="/reader"></Tab>
            <Tab color="primary" label="Author" component={Link} to="/author"></Tab>
          </Tabs>
        </div>
        <div className="App">
          <div className="grid">
            <Route exact path="/library" component={LibraryRequest} />
            <Route exact path="/reader" component={ReaderRequest} />
            <Route exact path="/author" component={AuthorRequest} />
          </div>
        </div>
      </Router>
    </div>
  );
}

export default App;
