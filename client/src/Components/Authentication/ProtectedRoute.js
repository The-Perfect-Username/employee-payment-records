import React from 'react';
import { Redirect, Route } from 'react-router-dom';

export default class ProtectedRoute extends Route {
    /**
     * @example <AuthRequiredRoute path="/" component={Products}>
     */
      render() {
          // call some method/function that will validate if user is logged in
          if(!localStorage.getItem("token")){
              return <Redirect to="/login"></Redirect>
          }else{
            return <this.props.component />
          }
      }
  }