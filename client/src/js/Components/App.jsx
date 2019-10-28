import React from 'react';
import '../../css/App.css';

import { connect } from 'react-redux';

import { BrowserRouter as Router, Switch } from "react-router-dom";
import Login from './Login';
import SignUp from './SignUp';
import DashBoard from './Dashboard';
import { get_uuid } from "../Utility/Firebase"

import { PrivateRoute, LoginRoute, SignUpRoute } from '../Utility/Routes';

class App extends React.Component {

  constructor(props) { 
    super(props)
  }
 
  render() {
    const isAuth = get_uuid() ? true : false
    return (
        <Router>
          <Switch>
            <LoginRoute authed={true} path="/login" component={Login} />
            <SignUpRoute authed={true} path="/signup" component={SignUp} />
            <PrivateRoute authed={true} path='/' component={DashBoard} />
          </Switch>
        </Router>
    )
  }
}

export default connect()(App);
