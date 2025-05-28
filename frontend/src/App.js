import React from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom"
import './App.css';
import Login from './components/Login';
import Dashboard from "./components/Dashboard";

function App() {
  return (
    <Router>
      <Switch>
        <Route exact path="/" component={Login} />
        <Route path="/dashboard" component={Dashboard} />
      </Switch>
    </Router>
  );
}

export default App;
