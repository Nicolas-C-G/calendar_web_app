import React from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom"
import './App.css';
import Login from './components/Login';
import Dashboard from "./components/Dashboard";
import Register from "./components/Register";

function App() {
  return (
    <Router>
      <Switch>
        <Route exact path="/" component={Login} />
        <Route path="/dashboard" component={Dashboard} />
        <Route path="/register" component={Register} />
      </Switch>
    </Router>
  );
}

export default App;
